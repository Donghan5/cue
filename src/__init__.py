"""
AI-Agentic Content Recommendation System

A system that solves "45-minute decision fatigue" by analyzing mood, context,
and subscriptions to provide personalized content recommendations.
"""

__version__ = "1.0.0"
__author__ = "AI Detective Team"

from .agents import AIDetective
from .models import (
    Mood,
    ContentType,
    Context,
    Subscription,
    UserProfile,
    Recommendation,
    RecommendationResponse
)

__all__ = [
    'AIDetective',
    'Mood',
    'ContentType',
    'Context',
    'Subscription',
    'UserProfile',
    'Recommendation',
    'RecommendationResponse'
]
