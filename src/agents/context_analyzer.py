"""
Context Analyzer Agent - Analyzes user's current context to refine recommendations
"""
from typing import Dict, List
from ..models.data_models import Context, ContentType


class ContextAnalyzer:
    """Analyzes user context to determine appropriate content recommendations"""
    
    def __init__(self):
        self.time_preferences = {
            "morning": {
                "energy": "building",
                "suitable": ["podcast", "news", "short videos", "upbeat music"],
                "duration_range": (15, 45)
            },
            "afternoon": {
                "energy": "peak",
                "suitable": ["movies", "tv shows", "gaming", "any content"],
                "duration_range": (30, 120)
            },
            "evening": {
                "energy": "winding_down",
                "suitable": ["tv shows", "movies", "music", "reading"],
                "duration_range": (30, 90)
            },
            "night": {
                "energy": "low",
                "suitable": ["light content", "music", "podcasts", "short videos"],
                "duration_range": (15, 60)
            }
        }
        
        self.social_context_preferences = {
            "alone": {
                "suitable": ["personal favorites", "exploring new content", "any genre"],
                "avoid": []
            },
            "with_friends": {
                "suitable": ["popular content", "comedy", "action", "multiplayer games"],
                "avoid": ["very personal", "niche"]
            },
            "with_family": {
                "suitable": ["family-friendly", "mainstream", "wholesome"],
                "avoid": ["mature content", "controversial"]
            },
            "with_partner": {
                "suitable": ["romance", "comedy", "drama", "shared interests"],
                "avoid": ["solo activities"]
            }
        }
    
    def analyze_context(self, context: Context) -> Dict:
        """
        Analyze the context and return recommendations parameters
        
        Args:
            context: Current user context
            
        Returns:
            Dictionary containing context-based preferences
        """
        time_prefs = self.time_preferences.get(context.time_of_day, self.time_preferences["afternoon"])
        social_prefs = self.social_context_preferences.get(context.social_context, self.social_context_preferences["alone"])
        
        # Adjust duration based on available time
        max_duration = min(context.available_time, time_prefs["duration_range"][1])
        min_duration = min(time_prefs["duration_range"][0], max_duration)
        
        return {
            "time_of_day": context.time_of_day,
            "day_of_week": context.day_of_week,
            "available_time": context.available_time,
            "recommended_duration_range": (min_duration, max_duration),
            "energy_phase": time_prefs["energy"],
            "suitable_content_types": time_prefs["suitable"],
            "social_context": context.social_context,
            "social_preferences": social_prefs,
            "location": context.location,
            "device": context.device,
            "analysis": self._generate_context_analysis(context, time_prefs, social_prefs, max_duration)
        }
    
    def _generate_context_analysis(self, context: Context, time_prefs: Dict, social_prefs: Dict, max_duration: int) -> str:
        """Generate human-readable context analysis"""
        time_desc = time_prefs.get("energy", "active")
        social_desc = context.social_context
        
        if context.available_time <= 30:
            time_msg = "You have limited time, so let's focus on shorter content."
        elif context.available_time <= 90:
            time_msg = "You have moderate time for a TV episode or short movie."
        else:
            time_msg = "You have plenty of time to dive into longer content!"
        
        social_msg = f"Since you're {social_desc}, " + (
            "we'll find something perfect for your solo time." if social_desc == "alone"
            else f"we'll focus on content great for {social_desc}."
        )
        
        return f"{time_msg} {social_msg} It's {context.time_of_day}, a {time_desc} phase."
    
    def is_content_appropriate(self, content_type: ContentType, context: Context) -> bool:
        """
        Check if a content type is appropriate for the current context
        
        Args:
            content_type: Type of content to check
            context: Current context
            
        Returns:
            Boolean indicating if content is appropriate
        """
        time_prefs = self.time_preferences.get(context.time_of_day, self.time_preferences["afternoon"])
        suitable = time_prefs.get("suitable", [])
        
        # Map content types to suitable categories
        content_mapping = {
            ContentType.MOVIE: ["movies", "any content"],
            ContentType.TV_SHOW: ["tv shows", "any content"],
            ContentType.MUSIC: ["music", "upbeat music", "any content"],
            ContentType.PODCAST: ["podcast", "podcasts", "any content"],
            ContentType.BOOK: ["reading", "any content"],
            ContentType.ARTICLE: ["reading", "news", "any content"],
            ContentType.VIDEO: ["short videos", "videos", "any content"],
            ContentType.GAME: ["gaming", "multiplayer games", "any content"]
        }
        
        content_categories = content_mapping.get(content_type, ["any content"])
        return any(cat in suitable for cat in content_categories)
    
    def get_urgency_factor(self, available_time: int) -> float:
        """
        Calculate urgency factor based on available time
        Less time = higher urgency = more weight on quick decisions
        """
        if available_time <= 15:
            return 2.0  # Very urgent
        elif available_time <= 45:
            return 1.5  # Moderately urgent
        else:
            return 1.0  # Normal
