"""
Data models for the AI-Agentic Recommendation System
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class Mood(str, Enum):
    """User mood states"""
    HAPPY = "happy"
    SAD = "sad"
    ENERGETIC = "energetic"
    TIRED = "tired"
    STRESSED = "stressed"
    RELAXED = "relaxed"
    BORED = "bored"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    CALM = "calm"


class ContentType(str, Enum):
    """Types of content available"""
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    MUSIC = "music"
    PODCAST = "podcast"
    BOOK = "book"
    ARTICLE = "article"
    VIDEO = "video"
    GAME = "game"


class Context(BaseModel):
    """User's current context"""
    time_of_day: str = Field(description="Current time of day (morning/afternoon/evening/night)")
    day_of_week: str = Field(description="Current day of the week")
    available_time: int = Field(description="Available time in minutes", ge=0)
    location: Optional[str] = Field(default="home", description="Current location context")
    social_context: str = Field(default="alone", description="Alone, with_friends, with_family, etc.")
    device: str = Field(default="mobile", description="Device being used")


class Subscription(BaseModel):
    """User's subscription information"""
    service_name: str = Field(description="Name of the service (Netflix, Spotify, etc.)")
    content_types: List[ContentType] = Field(description="Types of content available")
    is_active: bool = Field(default=True, description="Whether subscription is active")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="User preferences for this service")


class UserProfile(BaseModel):
    """Complete user profile"""
    user_id: str = Field(description="Unique user identifier")
    current_mood: Mood = Field(description="Current mood state")
    context: Context = Field(description="Current context")
    subscriptions: List[Subscription] = Field(description="Active subscriptions")
    viewing_history: Optional[List[str]] = Field(default=None, description="Recently consumed content")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="User preferences")


class Recommendation(BaseModel):
    """A single content recommendation"""
    title: str = Field(description="Title of the content")
    content_type: ContentType = Field(description="Type of content")
    service: str = Field(description="Service/platform where content is available")
    duration: int = Field(description="Duration in minutes")
    match_score: float = Field(description="How well this matches the user (0-100)", ge=0, le=100)
    reasoning: str = Field(description="Why this was recommended")
    genre: Optional[List[str]] = Field(default=None, description="Content genres")
    mood_alignment: str = Field(description="How this aligns with current mood")


class RecommendationResponse(BaseModel):
    """Complete recommendation response"""
    recommendations: List[Recommendation] = Field(description="List of recommendations")
    decision_time: float = Field(description="Time taken to generate recommendations in seconds")
    analysis: str = Field(description="Overall analysis of user's situation")
    confidence: float = Field(description="Confidence in recommendations (0-100)", ge=0, le=100)
    timestamp: datetime = Field(default_factory=datetime.now)
