"""
Model Evaluation Utilities
Calculates metrics and generates performance reports
"""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error, 
    mean_squared_error, 
    r2_score, 
    accuracy_score, 
    f1_score, 
    classification_report
)
from typing import Dict, Any
from loguru import logger


class ModelEvaluator:
    """
    Evaluates ML models and generates performance reports
    """
    
    @staticmethod
    def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Evaluate regression model (Timeline Predictor)
        """
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        # Calculate Mean Absolute Percentage Error (MAPE)
        # Avoid division by zero
        mask = y_true != 0
        if np.any(mask):
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        else:
            mape = 0.0
        
        metrics = {
            'mse': float(mse),
            'rmse': float(rmse),
            'mae': float(mae),
            'r2': float(r2),
            'mape': float(mape)
        }
        
        logger.info(f"📊 Regression Metrics: RMSE={rmse:.2f}, R2={r2:.2f}")
        return metrics

    @staticmethod
    def evaluate_classification(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Evaluate classification model (Sentiment/Burnout)
        """
        accuracy = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred, average='weighted')
        
        metrics = {
            'accuracy': float(accuracy),
            'f1_score': float(f1)
        }
        
        logger.info(f"📊 Classification Metrics: Acc={accuracy:.2f}, F1={f1:.2f}")
        try:
            logger.debug(f"\n{classification_report(y_true, y_pred)}")
        except:
            pass
        return metrics

    @staticmethod
    def analyze_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """
        Analyze prediction errors to find bias
        """
        residuals = y_true - y_pred
        
        analysis = {
            'mean_residual': float(np.mean(residuals)),
            'std_residual': float(np.std(residuals)),
            'skewness': float(pd.Series(residuals).skew()),
            'outliers_count': int(np.sum(np.abs(residuals) > 2 * np.std(residuals)))
        }
        
        if analysis['mean_residual'] > 0:
            bias = "Underestimating (Optimistic)"
        else:
            bias = "Overestimating (Pessimistic)"
            
        logger.info(f"📉 Residual Analysis: Bias={bias}, MeanErr={analysis['mean_residual']:.2f}")
        return analysis
