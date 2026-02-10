"""
Data Preparation for ML Training
Extracts historical project data and prepares for model training
"""

import numpy as np
import pandas as pd
from pathlib import Path
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from loguru import logger
import sys
from datetime import datetime, timedelta

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config.settings import settings


class DataPreparator:
    """
    Prepare training data from historical projects
    """
    
    def __init__(self, output_dir: str = "./src/data/datasets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("📊 Data Preparator initialized")
    
    async def fetch_historical_projects(self, db: AsyncSession, min_projects: int = 50):
        """
        Fetch completed projects from database
        
        **Required data:**
        - Project completion time (actual)
        - Team size
        - Story points
        - Velocity history
        - Blockers encountered
        - Task complexity
        """
        logger.info("🔍 Fetching historical project data from database...")
        
        query = text("""
            SELECT 
                p.id as project_id,
                p.name as project_name,
                p.created_at,
                p.completed_at,
                EXTRACT(EPOCH FROM (p.completed_at - p.created_at)) / (7 * 24 * 3600) as actual_weeks_taken,
                
                -- Story points
                (SELECT COALESCE(SUM(story_points), 0) 
                 FROM tasks 
                 WHERE project_id = p.id) as total_story_points,
                
                -- Team size
                (SELECT COUNT(DISTINCT assignee_id) 
                 FROM tasks 
                 WHERE project_id = p.id 
                   AND assignee_id IS NOT NULL) as team_size,
                
                -- Blockers
                (SELECT COUNT(*) 
                 FROM tasks 
                 WHERE project_id = p.id 
                   AND metadata->>'is_blocked' = 'true') as blocked_tasks_count,
                
                -- High complexity tasks
                (SELECT COUNT(*) 
                 FROM tasks 
                 WHERE project_id = p.id 
                   AND (metadata->>'complexity_score')::float > 0.7) as high_complexity_count
            
            FROM projects p
            WHERE p.completed_at IS NOT NULL
              AND p.created_at IS NOT NULL
              AND EXTRACT(EPOCH FROM (p.completed_at - p.created_at)) > 0
            ORDER BY p.completed_at DESC
            LIMIT 200
        """)
        
        result = await db.execute(query)
        rows = result.fetchall()
        
        logger.info(f"✅ Found {len(rows)} completed projects in database")
        
        return rows
    
    async def calculate_velocity_metrics(self, db: AsyncSession, project_id: str):
        """
        Calculate velocity statistics for a project
        """
        query = text("""
            SELECT 
                DATE_TRUNC('week', updated_at) as week,
                SUM(story_points) as points_completed
            FROM tasks
            WHERE project_id = :project_id
              AND status = 'done'
              AND updated_at IS NOT NULL
            GROUP BY week
            ORDER BY week
        """)
        
        result = await db.execute(query, {'project_id': project_id})
        rows = result.fetchall()
        
        if not rows:
            return {
                'avg_weekly_velocity': 10.0,
                'velocity_std': 2.0
            }
        
        velocities = [row[1] for row in rows if row[1] is not None]
        
        return {
            'avg_weekly_velocity': float(np.mean(velocities)) if velocities else 10.0,
            'velocity_std': float(np.std(velocities)) if len(velocities) > 1 else 2.0
        }
    
    def generate_synthetic_data(self, n_samples: int = 100):
        """
        Generate synthetic training data
        
        **Use when historical data is insufficient**
        """
        logger.info(f"🎲 Generating {n_samples} synthetic training samples...")
        
        np.random.seed(42)
        
        data = []
        
        for i in range(n_samples):
            # Random project parameters
            team_size = np.random.randint(2, 12)
            remaining_points = np.random.randint(20, 200)
            velocity = np.random.uniform(5, 30)
            velocity_std = velocity * np.random.uniform(0.1, 0.4)
            blocked_tasks = np.random.randint(0, 10)
            high_complexity = np.random.randint(0, 8)
            avg_task_age = np.random.uniform(0, 30)
            team_experience = np.random.uniform(0.3, 0.9)
            
            # Calculate actual weeks (with some randomness)
            base_weeks = remaining_points / velocity
            risk_multiplier = 1.0 + (blocked_tasks * 0.1) + (high_complexity * 0.05)
            actual_weeks = base_weeks * risk_multiplier * np.random.uniform(0.8, 1.2)
            
            data.append({
                'project_id': f'synthetic_{i}',
                'remaining_story_points': remaining_points,
                'avg_weekly_velocity': velocity,
                'velocity_std': velocity_std,
                'team_size': team_size,
                'blocked_tasks_count': blocked_tasks,
                'high_complexity_count': high_complexity,
                'avg_task_age_days': avg_task_age,
                'team_experience_score': team_experience,
                'actual_weeks_taken': actual_weeks
            })
        
        logger.success(f"✅ Generated {n_samples} synthetic samples")
        
        return pd.DataFrame(data)
    
    async def prepare_training_dataset(self):
        """
        Main function to prepare complete training dataset
        """
        logger.info("\n" + "="*60)
        logger.info("📊 PREPARING TRAINING DATASET")
        logger.info("="*60 + "\n")
        
        # Try to fetch from database
        try:
            # Create async engine
            database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            engine = create_async_engine(database_url, echo=False)
            
            AsyncSessionLocal = sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            async with AsyncSessionLocal() as db:
                # Fetch historical projects
                historical_rows = await self.fetch_historical_projects(db)
                
                if len(historical_rows) < 10:
                    logger.warning("⚠️  Insufficient historical data, using synthetic data")
                    df = self.generate_synthetic_data(100)
                else:
                    # Convert to dataframe
                    data = []
                    
                    for row in historical_rows:
                        # Calculate velocity metrics
                        velocity_metrics = await self.calculate_velocity_metrics(db, row[0])
                        
                        # Estimate remaining points at project start
                        remaining_points = float(row[5]) if row[5] else 0
                        
                        data.append({
                            'project_id': row[0],
                            'project_name': row[1],
                            'remaining_story_points': remaining_points,
                            'avg_weekly_velocity': velocity_metrics['avg_weekly_velocity'],
                            'velocity_std': velocity_metrics['velocity_std'],
                            'team_size': int(row[6]) if row[6] else 1,
                            'blocked_tasks_count': int(row[7]) if row[7] else 0,
                            'high_complexity_count': int(row[8]) if row[8] else 0,
                            'avg_task_age_days': 10.0,  # Estimated
                            'team_experience_score': 0.6,  # Default
                            'actual_weeks_taken': float(row[4]) if row[4] else 1.0
                        })
                    
                    df = pd.DataFrame(data)
                    
                    # If still not enough, add synthetic data
                    if len(df) < 50:
                        logger.info("📈 Augmenting with synthetic data...")
                        synthetic_df = self.generate_synthetic_data(50)
                        df = pd.concat([df, synthetic_df], ignore_index=True)
        
        except Exception as e:
            logger.warning(f"⚠️  Database fetch failed: {e}")
            logger.info("📈 Using synthetic data instead")
            df = self.generate_synthetic_data(100)
        
        # Clean data
        logger.info("🧹 Cleaning dataset...")
        
        # Remove outliers (projects > 52 weeks or < 1 week)
        df = df[(df['actual_weeks_taken'] >= 1) & (df['actual_weeks_taken'] <= 52)]
        
        # Ensure no negative values
        numeric_cols = [
            'remaining_story_points', 'avg_weekly_velocity', 'velocity_std',
            'team_size', 'blocked_tasks_count', 'high_complexity_count',
            'avg_task_age_days'
        ]
        
        for col in numeric_cols:
            df[col] = df[col].clip(lower=0)
        
        # Ensure team_size >= 1
        df['team_size'] = df['team_size'].clip(lower=1)
        
        # Ensure velocity > 0
        df['avg_weekly_velocity'] = df['avg_weekly_velocity'].clip(lower=0.1)
        
        logger.info(f"✅ Final dataset: {len(df)} samples")
        
        # Print statistics
        logger.info("\n📊 DATASET STATISTICS:")
        logger.info("="*60)
        logger.info(df.describe().to_string())
        logger.info("="*60 + "\n")
        
        # Save to CSV
        output_path = self.output_dir / "historical_projects.csv"
        df.to_csv(output_path, index=False)
        
        logger.success(f"✅ Training data saved to {output_path}")
        
        # Also save train/val/test splits
        from sklearn.model_selection import train_test_split
        
        train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)
        train_df, val_df = train_test_split(train_df, test_size=0.176, random_state=42)
        
        train_df.to_csv(self.output_dir / "train.csv", index=False)
        val_df.to_csv(self.output_dir / "val.csv", index=False)
        test_df.to_csv(self.output_dir / "test.csv", index=False)
        
        logger.success(f"✅ Split datasets saved:")
        logger.info(f"   - Train: {len(train_df)} samples")
        logger.info(f"   - Val:   {len(val_df)} samples")
        logger.info(f"   - Test:  {len(test_df)} samples\n")
        
        return df


async def main():
    """Main function"""
    preparator = DataPreparator()
    df = await preparator.prepare_training_dataset()
    
    logger.info("="*60)
    logger.info("🎉 DATA PREPARATION COMPLETE!")
    logger.info("="*60)
    logger.info("Next step: Run train_timeline.py to train the model")
    logger.info("="*60 + "\n")
    
    return df


if __name__ == "__main__":
    asyncio.run(main())
