"""API v1 endpoints package initialization"""
from src.api.v1.endpoints import (
    predictions,
    skills,
    simulations,
    sentiment,
    health,
    insights
)

__all__ = [
    'predictions',
    'skills',
    'simulations',
    'sentiment',
    'health',
    'insights'
]
