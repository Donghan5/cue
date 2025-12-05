"""
Mood Analyzer Agent - Analyzes user mood and its impact on content preferences
"""
from typing import Dict, List
from ..models.data_models import Mood, ContentType


class MoodAnalyzer:
    """Analyzes user mood to determine appropriate content recommendations"""
    
    def __init__(self):
        # Mapping of moods to preferred content characteristics
        self.mood_content_mapping = {
            Mood.HAPPY: {
                "energy_level": "high",
                "tone": ["uplifting", "fun", "lighthearted"],
                "genres": ["comedy", "adventure", "upbeat music"],
                "avoid": ["drama", "horror"]
            },
            Mood.SAD: {
                "energy_level": "low",
                "tone": ["comforting", "emotional", "cathartic"],
                "genres": ["drama", "documentary", "acoustic music"],
                "avoid": ["horror", "intense action"]
            },
            Mood.ENERGETIC: {
                "energy_level": "very_high",
                "tone": ["exciting", "fast-paced", "dynamic"],
                "genres": ["action", "thriller", "rock music", "dance"],
                "avoid": ["slow-paced", "documentary"]
            },
            Mood.TIRED: {
                "energy_level": "very_low",
                "tone": ["relaxing", "easy-watching", "simple"],
                "genres": ["sitcom", "nature documentary", "ambient music"],
                "avoid": ["complex plots", "intense"]
            },
            Mood.STRESSED: {
                "energy_level": "low",
                "tone": ["calming", "escapist", "soothing"],
                "genres": ["comedy", "nature", "meditation", "chill music"],
                "avoid": ["thriller", "horror", "intense drama"]
            },
            Mood.RELAXED: {
                "energy_level": "medium",
                "tone": ["pleasant", "enjoyable", "comfortable"],
                "genres": ["romance", "slice-of-life", "jazz", "indie"],
                "avoid": ["horror", "heavy drama"]
            },
            Mood.BORED: {
                "energy_level": "medium",
                "tone": ["engaging", "interesting", "stimulating"],
                "genres": ["mystery", "sci-fi", "documentary", "variety"],
                "avoid": ["predictable", "repetitive"]
            },
            Mood.EXCITED: {
                "energy_level": "high",
                "tone": ["thrilling", "adventurous", "new"],
                "genres": ["action", "adventure", "new releases"],
                "avoid": ["slow-paced", "familiar"]
            },
            Mood.ANXIOUS: {
                "energy_level": "medium",
                "tone": ["comforting", "predictable", "gentle"],
                "genres": ["familiar favorites", "feel-good", "soft music"],
                "avoid": ["suspense", "thriller", "unpredictable"]
            },
            Mood.CALM: {
                "energy_level": "medium",
                "tone": ["peaceful", "thoughtful", "balanced"],
                "genres": ["drama", "documentary", "classical", "indie"],
                "avoid": ["action", "horror"]
            }
        }
    
    def analyze_mood(self, mood: Mood) -> Dict:
        """
        Analyze the mood and return content preferences
        
        Args:
            mood: Current user mood
            
        Returns:
            Dictionary containing content preferences based on mood
        """
        preferences = self.mood_content_mapping.get(mood, {})
        
        return {
            "mood": mood.value,
            "energy_level": preferences.get("energy_level", "medium"),
            "preferred_tone": preferences.get("tone", []),
            "preferred_genres": preferences.get("genres", []),
            "avoid_genres": preferences.get("avoid", []),
            "analysis": self._generate_mood_analysis(mood, preferences)
        }
    
    def _generate_mood_analysis(self, mood: Mood, preferences: Dict) -> str:
        """Generate human-readable mood analysis"""
        energy = preferences.get("energy_level", "medium")
        tone = ", ".join(preferences.get("tone", [])[:2])
        
        analysis_templates = {
            Mood.HAPPY: f"You're feeling great! Perfect time for {tone} content.",
            Mood.SAD: f"You might benefit from {tone} content that helps process emotions.",
            Mood.ENERGETIC: f"Your high energy is perfect for {tone} experiences!",
            Mood.TIRED: f"You need something {tone} that won't require too much effort.",
            Mood.STRESSED: f"Let's find something {tone} to help you unwind.",
            Mood.RELAXED: f"Enjoy this peaceful moment with {tone} content.",
            Mood.BORED: f"Time for something {tone} to capture your interest!",
            Mood.EXCITED: f"Your excitement calls for {tone} new experiences!",
            Mood.ANXIOUS: f"Let's ease your mind with {tone} content.",
            Mood.CALM: f"Maintain this peace with {tone} selections."
        }
        
        return analysis_templates.get(mood, "Let's find something that matches your vibe.")
    
    def get_mood_weight(self, mood: Mood) -> float:
        """
        Return the weight/importance of mood in the recommendation
        Some moods require stronger consideration than others
        """
        high_priority_moods = [Mood.STRESSED, Mood.ANXIOUS, Mood.SAD]
        return 1.5 if mood in high_priority_moods else 1.0
