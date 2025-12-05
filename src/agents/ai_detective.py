"""
AI Detective Agent - The main coordinator that solves the 45-minute decision fatigue
"""
import time
from typing import List, Dict
from datetime import datetime

from .mood_analyzer import MoodAnalyzer
from .context_analyzer import ContextAnalyzer
from .subscription_analyzer import SubscriptionAnalyzer
from ..models.data_models import (
    UserProfile,
    Recommendation,
    RecommendationResponse,
    ContentType
)


class AIDetective:
    """
    The AI Detective that solves "45-minute decision fatigue" by quickly analyzing
    mood, context, and subscriptions to provide personalized recommendations.
    
    This agent acts as the central coordinator for all analysis components.
    """
    
    def __init__(self):
        self.mood_analyzer = MoodAnalyzer()
        self.context_analyzer = ContextAnalyzer()
        self.subscription_analyzer = SubscriptionAnalyzer()
        
        # Sample content database (in production, this would be a real database)
        self.content_database = self._initialize_content_database()
    
    def investigate(self, user_profile: UserProfile) -> RecommendationResponse:
        """
        Main investigation method - analyzes user and returns recommendations
        
        Args:
            user_profile: Complete user profile with mood, context, and subscriptions
            
        Returns:
            RecommendationResponse with personalized recommendations
        """
        start_time = time.time()
        
        # Step 1: Analyze mood
        mood_analysis = self.mood_analyzer.analyze_mood(user_profile.current_mood)
        
        # Step 2: Analyze context
        context_analysis = self.context_analyzer.analyze_context(user_profile.context)
        
        # Step 3: Analyze subscriptions
        subscription_analysis = self.subscription_analyzer.analyze_subscriptions(
            user_profile.subscriptions
        )
        
        # Step 4: Generate recommendations using all analyses
        recommendations = self._generate_recommendations(
            user_profile,
            mood_analysis,
            context_analysis,
            subscription_analysis
        )
        
        # Step 5: Calculate confidence score
        confidence = self._calculate_confidence(
            mood_analysis,
            context_analysis,
            subscription_analysis
        )
        
        # Step 6: Generate overall analysis
        overall_analysis = self._generate_overall_analysis(
            mood_analysis,
            context_analysis,
            subscription_analysis
        )
        
        decision_time = time.time() - start_time
        
        return RecommendationResponse(
            recommendations=recommendations,
            decision_time=decision_time,
            analysis=overall_analysis,
            confidence=confidence,
            timestamp=datetime.now()
        )
    
    def _generate_recommendations(
        self,
        user_profile: UserProfile,
        mood_analysis: Dict,
        context_analysis: Dict,
        subscription_analysis: Dict
    ) -> List[Recommendation]:
        """Generate personalized recommendations based on all analyses"""
        
        recommendations = []
        available_services = subscription_analysis.get("available_services", [])
        
        if not available_services:
            # No subscriptions - provide generic recommendations
            return self._generate_free_recommendations(mood_analysis, context_analysis)
        
        # Get duration constraints
        min_duration, max_duration = context_analysis["recommended_duration_range"]
        
        # Filter content based on mood and context
        preferred_genres = mood_analysis.get("preferred_genres", [])
        avoid_genres = mood_analysis.get("avoid_genres", [])
        
        # Search through content database
        candidates = []
        for content in self.content_database:
            # Check if content is available on user's subscriptions
            if content["service"] not in available_services:
                continue
            
            # Check duration fit
            if not (min_duration <= content["duration"] <= max_duration):
                continue
            
            # Check if content type is appropriate for context
            if not self.context_analyzer.is_content_appropriate(
                content["content_type"],
                user_profile.context
            ):
                continue
            
            # Calculate match score
            score = self._calculate_match_score(
                content,
                mood_analysis,
                context_analysis,
                user_profile
            )
            
            candidates.append((content, score))
        
        # Sort by score and take top 5
        candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = candidates[:5]
        
        # Create Recommendation objects
        for content, score in top_candidates:
            reasoning = self._generate_reasoning(
                content,
                mood_analysis,
                context_analysis,
                user_profile.current_mood
            )
            
            mood_alignment = self._get_mood_alignment(
                content,
                mood_analysis
            )
            
            recommendations.append(Recommendation(
                title=content["title"],
                content_type=content["content_type"],
                service=content["service"],
                duration=content["duration"],
                match_score=score,
                reasoning=reasoning,
                genre=content.get("genre", []),
                mood_alignment=mood_alignment
            ))
        
        return recommendations
    
    def _calculate_match_score(
        self,
        content: Dict,
        mood_analysis: Dict,
        context_analysis: Dict,
        user_profile: UserProfile
    ) -> float:
        """Calculate how well content matches user's current state"""
        
        score = 50.0  # Base score
        
        # Mood matching
        preferred_genres = mood_analysis.get("preferred_genres", [])
        avoid_genres = mood_analysis.get("avoid_genres", [])
        content_genres = content.get("genre", [])
        
        for genre in content_genres:
            if any(pg.lower() in genre.lower() for pg in preferred_genres):
                score += 15
            if any(ag.lower() in genre.lower() for ag in avoid_genres):
                score -= 20
        
        # Duration matching
        min_dur, max_dur = context_analysis["recommended_duration_range"]
        if min_dur <= content["duration"] <= max_dur:
            score += 10
        
        # Viewing history (avoid recently watched)
        if user_profile.viewing_history:
            if content["title"] in user_profile.viewing_history:
                score -= 30
        
        # Energy level matching
        energy_level = mood_analysis.get("energy_level")
        if energy_level in ["very_low", "low"] and content["duration"] < 60:
            score += 10
        elif energy_level in ["high", "very_high"] and content["duration"] > 60:
            score += 10
        
        # Ensure score is between 0 and 100
        return max(0, min(100, score))
    
    def _generate_reasoning(
        self,
        content: Dict,
        mood_analysis: Dict,
        context_analysis: Dict,
        mood
    ) -> str:
        """Generate human-readable reasoning for recommendation"""
        
        reasons = []
        
        # Mood-based reasoning
        if mood_analysis.get("energy_level") in ["very_low", "low"]:
            reasons.append("perfect for your current energy level")
        elif mood_analysis.get("energy_level") in ["high", "very_high"]:
            reasons.append("matches your high energy")
        
        # Genre matching
        preferred = mood_analysis.get("preferred_genres", [])
        content_genres = content.get("genre", [])
        matching_genres = [g for g in content_genres if any(pg.lower() in g.lower() for pg in preferred)]
        if matching_genres:
            reasons.append(f"aligns with your mood through its {matching_genres[0]} elements")
        
        # Time-based reasoning
        if context_analysis["available_time"] <= 45:
            reasons.append("fits your available time perfectly")
        
        # Default reasoning
        if not reasons:
            reasons.append("well-suited for your current situation")
        
        return "This is recommended because it's " + " and ".join(reasons) + "."
    
    def _get_mood_alignment(self, content: Dict, mood_analysis: Dict) -> str:
        """Generate mood alignment description"""
        tone = mood_analysis.get("preferred_tone", ["balanced"])
        return f"Aligns with your need for {tone[0]} content"
    
    def _calculate_confidence(
        self,
        mood_analysis: Dict,
        context_analysis: Dict,
        subscription_analysis: Dict
    ) -> float:
        """Calculate confidence in recommendations"""
        
        # Base confidence
        confidence = 70.0
        
        # Subscription diversity increases confidence
        diversity = subscription_analysis.get("content_diversity", 0)
        confidence += min(diversity * 3, 15)
        
        # Clear context increases confidence
        if context_analysis.get("available_time", 0) > 0:
            confidence += 5
        
        # Having subscriptions increases confidence
        if subscription_analysis.get("total_subscriptions", 0) > 0:
            confidence += 10
        
        return min(confidence, 100.0)
    
    def _generate_overall_analysis(
        self,
        mood_analysis: Dict,
        context_analysis: Dict,
        subscription_analysis: Dict
    ) -> str:
        """Generate overall analysis of the situation"""
        
        parts = [
            mood_analysis.get("analysis", ""),
            context_analysis.get("analysis", ""),
            subscription_analysis.get("analysis", "")
        ]
        
        analysis = " ".join(filter(None, parts))
        
        # Add decision fatigue solution message
        conclusion = (
            " I've analyzed your mood, context, and available subscriptions to solve your "
            "decision fatigue - here are my top recommendations curated just for you!"
        )
        
        return analysis + conclusion
    
    def _generate_free_recommendations(
        self,
        mood_analysis: Dict,
        context_analysis: Dict
    ) -> List[Recommendation]:
        """Generate recommendations for free content when no subscriptions are available"""
        
        free_content = [
            {
                "title": "YouTube Trending Videos",
                "content_type": ContentType.VIDEO,
                "service": "YouTube (Free)",
                "duration": 15,
                "genre": ["various"]
            },
            {
                "title": "Free Podcasts",
                "content_type": ContentType.PODCAST,
                "service": "Podcast Platforms (Free)",
                "duration": 30,
                "genre": ["various"]
            },
            {
                "title": "Public Domain Books",
                "content_type": ContentType.BOOK,
                "service": "Project Gutenberg",
                "duration": 120,
                "genre": ["classic literature"]
            }
        ]
        
        recommendations = []
        for content in free_content[:3]:
            recommendations.append(Recommendation(
                title=content["title"],
                content_type=content["content_type"],
                service=content["service"],
                duration=content["duration"],
                match_score=60.0,
                reasoning="Free content that matches your general preferences.",
                genre=content.get("genre", []),
                mood_alignment=mood_analysis.get("analysis", "Suitable for your mood")
            ))
        
        return recommendations
    
    def _initialize_content_database(self) -> List[Dict]:
        """Initialize sample content database"""
        # This is a sample database. In production, this would be a real database with thousands of items
        return [
            # Netflix content
            {"title": "Stranger Things", "content_type": ContentType.TV_SHOW, "service": "Netflix", 
             "duration": 50, "genre": ["sci-fi", "thriller", "drama"]},
            {"title": "The Crown", "content_type": ContentType.TV_SHOW, "service": "Netflix",
             "duration": 60, "genre": ["drama", "historical"]},
            {"title": "Queer Eye", "content_type": ContentType.TV_SHOW, "service": "Netflix",
             "duration": 45, "genre": ["reality", "feel-good", "lifestyle"]},
            {"title": "Our Planet", "content_type": ContentType.TV_SHOW, "service": "Netflix",
             "duration": 50, "genre": ["documentary", "nature"]},
            {"title": "The Office", "content_type": ContentType.TV_SHOW, "service": "Netflix",
             "duration": 22, "genre": ["comedy", "sitcom"]},
            
            # Amazon Prime content
            {"title": "The Marvelous Mrs. Maisel", "content_type": ContentType.TV_SHOW, "service": "Amazon Prime",
             "duration": 55, "genre": ["comedy", "drama"]},
            {"title": "Jack Ryan", "content_type": ContentType.TV_SHOW, "service": "Amazon Prime",
             "duration": 50, "genre": ["action", "thriller"]},
            
            # Disney+ content
            {"title": "The Mandalorian", "content_type": ContentType.TV_SHOW, "service": "Disney Plus",
             "duration": 40, "genre": ["sci-fi", "action", "adventure"]},
            {"title": "Encanto", "content_type": ContentType.MOVIE, "service": "Disney Plus",
             "duration": 102, "genre": ["animation", "family", "musical"]},
            
            # HBO Max content
            {"title": "Succession", "content_type": ContentType.TV_SHOW, "service": "HBO Max",
             "duration": 60, "genre": ["drama"]},
            {"title": "Last Week Tonight", "content_type": ContentType.TV_SHOW, "service": "HBO Max",
             "duration": 30, "genre": ["comedy", "news"]},
            
            # Hulu content
            {"title": "The Bear", "content_type": ContentType.TV_SHOW, "service": "Hulu",
             "duration": 35, "genre": ["drama", "comedy"]},
            {"title": "Only Murders in the Building", "content_type": ContentType.TV_SHOW, "service": "Hulu",
             "duration": 35, "genre": ["comedy", "mystery"]},
            
            # Music content
            {"title": "Chill Vibes Playlist", "content_type": ContentType.MUSIC, "service": "Spotify",
             "duration": 60, "genre": ["chill", "ambient"]},
            {"title": "Workout Energy Mix", "content_type": ContentType.MUSIC, "service": "Spotify",
             "duration": 45, "genre": ["electronic", "upbeat"]},
            {"title": "Acoustic Evening", "content_type": ContentType.MUSIC, "service": "Apple Music",
             "duration": 40, "genre": ["acoustic", "indie"]},
            
            # Podcasts
            {"title": "How I Built This", "content_type": ContentType.PODCAST, "service": "Spotify",
             "duration": 45, "genre": ["business", "entrepreneurship"]},
            {"title": "Calm Sleep Stories", "content_type": ContentType.PODCAST, "service": "Spotify",
             "duration": 30, "genre": ["relaxation", "sleep"]},
            
            # Books/Audiobooks
            {"title": "Atomic Habits", "content_type": ContentType.BOOK, "service": "Audible",
             "duration": 320, "genre": ["self-help", "productivity"]},
            {"title": "The Midnight Library", "content_type": ContentType.BOOK, "service": "Audible",
             "duration": 540, "genre": ["fiction", "philosophical"]},
        ]
