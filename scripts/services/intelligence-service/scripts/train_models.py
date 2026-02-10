"""
Master Training Script
Trains all ML models for the Intelligence Service
"""

import sys
import os
from loguru import logger

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ml.training.train_timeline import train_timeline_model


def train_all_models():
    """Train all ML models for the Intelligence Service"""
    
    print("\n" + "=" * 70)
    print("🤖 Intelligence Service - ML Model Training")
    print("=" * 70)
    
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    # Define model save path
    save_path = os.path.join(
        os.path.dirname(__file__),
        "../../src/data/models"
    )
    os.makedirs(save_path, exist_ok=True)
    
    trained_models = []
    
    # Train Timeline Predictor
    try:
        logger.info("\n📊 [1/1] Training Timeline Prediction Model...")
        timeline_model = train_timeline_model(save_path=save_path)
        trained_models.append("✅ Timeline Predictor")
        logger.success("✅ Timeline model trained successfully\n")
    except Exception as e:
        logger.error(f"❌ Failed to train timeline model: {e}")
        trained_models.append("❌ Timeline Predictor (failed)")
    
    # Skill Extraction and Sentiment Analysis use pre-trained models (spaCy, transformers)
    # They don't require custom training
    logger.info("ℹ️  Skill Extraction uses spaCy pre-trained models (no training needed)")
    logger.info("ℹ️  Sentiment Analysis uses Transformers pre-trained models (no training needed)")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Training Summary")
    print("=" * 70)
    for model in trained_models:
        print(f"  {model}")
    
    print("\n📁 Models saved to:", os.path.abspath(save_path))
    print("\n🚀 Next Steps:")
    print("  1. Restart the Intelligence Service")
    print("  2. Models will automatically load from src/data/models/")
    print("  3. Test predictions at: http://localhost:4002/docs")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    train_all_models()
