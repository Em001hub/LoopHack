"""
Data Transformers
Custom Scikit-Learn transformers for ML pipelines
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Dict, Union
from loguru import logger


class LogTransformer(BaseEstimator, TransformerMixin):
    """
    Logarithm transformer for skewed data (e.g., velocity, lines of code)
    Handles zeros by adding 1 (log1p)
    """
    def __init__(self, columns: List[str] = None):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        if isinstance(X_new, pd.DataFrame):
            cols = self.columns if self.columns else X_new.select_dtypes(include=[np.number]).columns
            for col in cols:
                # Ensure non-negative
                X_new[col] = np.log1p(np.maximum(X_new[col], 0))
        else:
            X_new = np.log1p(np.maximum(X_new, 0))
        return X_new


class CyclicalEncoder(BaseEstimator, TransformerMixin):
    """
    Encodes cyclical features (day of week, hour, month) using Sin/Cos
    """
    def __init__(self, period: int):
        self.period = period

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_new = X.copy()
        if isinstance(X_new, pd.DataFrame):
            # Assuming single column input for DataFrame
            vals = X_new.iloc[:, 0].values
        else:
            vals = X_new

        sin_trans = np.sin(2 * np.pi * vals / self.period)
        cos_trans = np.cos(2 * np.pi * vals / self.period)
        
        return np.column_stack([sin_trans, cos_trans])


class OutlierClipper(BaseEstimator, TransformerMixin):
    """
    Clips outliers to specific percentiles (Winsorizing)
    """
    def __init__(self, lower_percentile: int = 1, upper_percentile: int = 99):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.limits_ = {}

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            for col in X.select_dtypes(include=[np.number]).columns:
                self.limits_[col] = (
                    np.percentile(X[col], self.lower_percentile),
                    np.percentile(X[col], self.upper_percentile)
                )
        return self

    def transform(self, X):
        X_new = X.copy()
        if isinstance(X_new, pd.DataFrame):
            for col, (low, high) in self.limits_.items():
                if col in X_new.columns:
                    X_new[col] = np.clip(X_new[col], low, high)
        return X_new
