"""
Model Evaluation Utilities
Comprehensive model performance evaluation
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from loguru import logger


class ModelEvaluator:
    """
    Evaluate ML model performance with comprehensive metrics
    """
    
    def __init__(self):
        self.metrics = {}
    
    def evaluate_regression(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str = "Model"
    ) -> Dict:
        """
        Evaluate regression model
        
        **Metrics:**
        - R² Score
        - MAE (Mean Absolute Error)
        - RMSE (Root Mean Squared Error)
        - MAPE (Mean Absolute Percentage Error)
        - Accuracy within thresholds
        """
        logger.info(f"📊 Evaluating {model_name}...")
        
        # Basic metrics
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        
        # MAPE
        mape = np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1e-10))) * 100
        
        # Accuracy within thresholds
        errors = np.abs(y_true - y_pred)
        within_thresholds = {
            'within_5_pct': np.mean(errors / np.maximum(y_true, 1e-10) <= 0.05) * 100,
            'within_10_pct': np.mean(errors / np.maximum(y_true, 1e-10) <= 0.10) * 100,
            'within_20_pct': np.mean(errors / np.maximum(y_true, 1e-10) <= 0.20) * 100
        }
        
        metrics = {
            'model_name': model_name,
            'r2_score': r2,
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape,
            **within_thresholds
        }
        
        self.metrics[model_name] = metrics
        
        # Print results
        self._print_regression_results(metrics)
        
        return metrics
    
    def _print_regression_results(self, metrics: Dict):
        """Pretty print regression metrics"""
        logger.info("\n" + "="*60)
        logger.info(f"📊 {metrics['model_name']} - EVALUATION RESULTS")
        logger.info("="*60)
        logger.info(f"R² Score:               {metrics['r2_score']:.4f}")
        logger.info(f"Mean Absolute Error:    {metrics['mae']:.2f}")
        logger.info(f"Root Mean Squared Error: {metrics['rmse']:.2f}")
        logger.info(f"Mean Absolute % Error:  {metrics['mape']:.2f}%")
        logger.info("\n📈 ACCURACY WITHIN THRESHOLDS:")
        logger.info(f"Within ±5%:             {metrics['within_5_pct']:.1f}%")
        logger.info(f"Within ±10%:            {metrics['within_10_pct']:.1f}%")
        logger.info(f"Within ±20%:            {metrics['within_20_pct']:.1f}%")
        logger.info("="*60 + "\n")
    
    def evaluate_classification(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str = "Model",
        class_names: Optional[List[str]] = None
    ) -> Dict:
        """
        Evaluate classification model
        
        **Metrics:**
        - Accuracy
        - Precision
        - Recall
        - F1 Score
        - Confusion Matrix
        """
        logger.info(f"📊 Evaluating {model_name}...")
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        
        # For multiclass, use weighted average
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        metrics = {
            'model_name': model_name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm
        }
        
        self.metrics[model_name] = metrics
        
        # Print results
        self._print_classification_results(metrics, class_names)
        
        return metrics
    
    def _print_classification_results(self, metrics: Dict, class_names: Optional[List[str]]):
        """Pretty print classification metrics"""
        logger.info("\n" + "="*60)
        logger.info(f"📊 {metrics['model_name']} - EVALUATION RESULTS")
        logger.info("="*60)
        logger.info(f"Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall:    {metrics['recall']:.4f}")
        logger.info(f"F1 Score:  {metrics['f1_score']:.4f}")
        logger.info("\n📊 CONFUSION MATRIX:")
        logger.info(str(metrics['confusion_matrix']))
        logger.info("="*60 + "\n")
    
    def compare_models(
        self,
        models_metrics: Dict[str, Dict]
    ) -> pd.DataFrame:
        """
        Compare multiple models side-by-side
        
        **Returns:**
        DataFrame with comparison
        """
        logger.info("📊 Comparing models...")
        
        comparison_data = []
        
        for model_name, metrics in models_metrics.items():
            row = {'Model': model_name}
            
            # Add relevant metrics
            if 'r2_score' in metrics:
                row['R² Score'] = f"{metrics['r2_score']:.4f}"
                row['MAE'] = f"{metrics['mae']:.2f}"
                row['RMSE'] = f"{metrics['rmse']:.2f}"
            
            if 'accuracy' in metrics:
                row['Accuracy'] = f"{metrics['accuracy']:.4f}"
                row['F1 Score'] = f"{metrics['f1_score']:.4f}"
            
            comparison_data.append(row)
        
        df = pd.DataFrame(comparison_data)
        
        logger.info("\n" + "="*60)
        logger.info("📊 MODEL COMPARISON")
        logger.info("="*60)
        logger.info("\n" + df.to_string(index=False))
        logger.info("\n" + "="*60 + "\n")
        
        return df
    
    def plot_learning_curve(
        self,
        train_sizes: np.ndarray,
        train_scores: np.ndarray,
        val_scores: np.ndarray,
        title: str = "Learning Curve"
    ):
        """
        Plot learning curve showing training vs validation performance
        """
        plt.figure(figsize=(10, 6))
        
        # Calculate mean and std
        train_mean = np.mean(train_scores, axis=1)
        train_std = np.std(train_scores, axis=1)
        val_mean = np.mean(val_scores, axis=1)
        val_std = np.std(val_scores, axis=1)
        
        # Plot
        plt.plot(train_sizes, train_mean, 'o-', label='Training score', linewidth=2)
        plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.2)
        
        plt.plot(train_sizes, val_mean, 'o-', label='Validation score', linewidth=2)
        plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.2)
        
        plt.xlabel('Training Set Size', fontsize=12)
        plt.ylabel('Score', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('learning_curve.png', dpi=300, bbox_inches='tight')
        logger.success("✅ Learning curve saved to learning_curve.png")
        plt.close()
    
    def plot_confusion_matrix(
        self,
        cm: np.ndarray,
        class_names: List[str],
        title: str = "Confusion Matrix"
    ):
        """
        Plot confusion matrix heatmap
        """
        plt.figure(figsize=(10, 8))
        
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names,
            cbar_kws={'label': 'Count'}
        )
        
        plt.xlabel('Predicted', fontsize=12)
        plt.ylabel('Actual', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        logger.success("✅ Confusion matrix saved to confusion_matrix.png")
        plt.close()
