"""
Model Performance Viewer
Displays training metrics and feature importance
"""
import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich import box
from rich.progress import track
import time
import pickle
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

def display_performance():
    console = Console()
    
    # Check for model file (relative to script location)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(base_dir, "src", "data", "models", "timeline_model.pkl")
    
    if not os.path.exists(model_path):
        console.print(f"[bold red]Error:[/] Model not found at {model_path}")
        console.print("Run [cyan]python -m src.ml.training.train_timeline[/] first.")
        # Create mock data for demonstration
        data = {
            'metrics': {'rmse': 1.25, 'mae': 0.85, 'r2': 0.82},
            'trained_at': '2024-02-09T14:00:00',
            'features': [
                'remaining_points', 'velocity', 'team_size', 
                'blockers', 'complexity', 'task_age'
            ],
            # Mock feature importance
            'model': type('MockModel', (), {
                'feature_importances_': [0.45, 0.25, 0.10, 0.08, 0.07, 0.05]
            })()
        }
    else:
        with open(model_path, 'rb') as f:
            data = pickle.load(f)

    # Header
    console.print("\n[bold magenta]🤖 ML Model Performance Report[/]", justify="center")
    console.print(f"[dim]Model: Timeline Predictor | Trained: {data['trained_at']}[/]\n")
    
    # Metrics Table
    metrics_table = Table(title="Evaluation Metrics", box=box.HEAVY_EDGE)
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Value", style="green", justify="right")
    metrics_table.add_column("Interpretation", style="italic")
    
    m = data['metrics']
    metrics_table.add_row("R² Score", f"{m['r2']:.3f}", "Good fit (>0.8)" if m['r2'] > 0.8 else "Moderate fit")
    metrics_table.add_row("RMSE", f"{m['rmse']:.3f} wks", "Avg error magnitude")
    metrics_table.add_row("MAE", f"{m['mae']:.3f} wks", "Avg absolute error")
    
    console.print(metrics_table, justify="center")
    console.print()
    
    # Feature Importance
    tree = Tree("[bold blue]Feature Importance[/] (What drives predictions?)")
    
    features = data.get('features', [])
    model = data.get('model')
    
    if hasattr(model, 'feature_importances_'):
        importances = zip(features, model.feature_importances_)
        sorted_features = sorted(importances, key=lambda x: x[1], reverse=True)
        
        if sorted_features:
            max_imp = sorted_features[0][1]
            
            for feat, imp in sorted_features:
                # Create a simple bar chart using blocks
                bar_len = int((imp / max_imp) * 20)
                bar = "█" * bar_len
                pct = f"{imp:.1%}"
                
                if imp > 0.3:
                    color = "bold green"
                elif imp > 0.1:
                    color = "yellow"
                else:
                    color = "dim white"
                    
                tree.add(f"[{color}]{feat:<25} {bar} {pct}[/]")
    else:
        tree.add("[yellow]Model does not support feature importance[/]")
        
    console.print(tree)
    console.print()

if __name__ == "__main__":
    display_performance()
