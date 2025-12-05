"""
Subscription Analyzer Agent - Analyzes available subscriptions and content
"""
from typing import Dict, List, Set
from ..models.data_models import Subscription, ContentType


class SubscriptionAnalyzer:
    """Analyzes user subscriptions to determine available content sources"""
    
    def __init__(self):
        # Knowledge base of popular services and their content
        self.service_catalog = {
            "netflix": {
                "content_types": [ContentType.MOVIE, ContentType.TV_SHOW],
                "strengths": ["original series", "movies", "documentaries"],
                "typical_duration": {"movie": 120, "tv_show": 45}
            },
            "spotify": {
                "content_types": [ContentType.MUSIC, ContentType.PODCAST],
                "strengths": ["music streaming", "podcasts", "playlists"],
                "typical_duration": {"music": 3, "podcast": 45}
            },
            "youtube_premium": {
                "content_types": [ContentType.VIDEO, ContentType.MUSIC],
                "strengths": ["videos", "music", "creators content"],
                "typical_duration": {"video": 15, "music": 3}
            },
            "amazon_prime": {
                "content_types": [ContentType.MOVIE, ContentType.TV_SHOW, ContentType.MUSIC],
                "strengths": ["movies", "tv shows", "amazon originals"],
                "typical_duration": {"movie": 120, "tv_show": 45}
            },
            "disney_plus": {
                "content_types": [ContentType.MOVIE, ContentType.TV_SHOW],
                "strengths": ["family content", "marvel", "star wars"],
                "typical_duration": {"movie": 120, "tv_show": 30}
            },
            "hbo_max": {
                "content_types": [ContentType.MOVIE, ContentType.TV_SHOW],
                "strengths": ["premium series", "movies", "hbo originals"],
                "typical_duration": {"movie": 120, "tv_show": 60}
            },
            "hulu": {
                "content_types": [ContentType.MOVIE, ContentType.TV_SHOW],
                "strengths": ["current tv shows", "movies", "originals"],
                "typical_duration": {"movie": 120, "tv_show": 45}
            },
            "apple_music": {
                "content_types": [ContentType.MUSIC, ContentType.PODCAST],
                "strengths": ["music streaming", "podcasts"],
                "typical_duration": {"music": 3, "podcast": 45}
            },
            "audible": {
                "content_types": [ContentType.BOOK, ContentType.PODCAST],
                "strengths": ["audiobooks", "podcasts", "original audio"],
                "typical_duration": {"book": 480, "podcast": 45}
            },
            "kindle_unlimited": {
                "content_types": [ContentType.BOOK],
                "strengths": ["ebooks", "magazines"],
                "typical_duration": {"book": 360}
            }
        }
    
    def _normalize_service_name(self, service_name: str) -> str:
        """
        Normalize service name for consistent lookup
        
        Args:
            service_name: Original service name
            
        Returns:
            Normalized service name (lowercase with underscores)
        """
        return service_name.lower().replace(" ", "_")
    
    def analyze_subscriptions(self, subscriptions: List[Subscription]) -> Dict:
        """
        Analyze user subscriptions to determine available content
        
        Args:
            subscriptions: List of user subscriptions
            
        Returns:
            Dictionary containing subscription analysis
        """
        active_subs = [sub for sub in subscriptions if sub.is_active]
        
        # Aggregate available content types
        available_content_types: Set[ContentType] = set()
        available_services = []
        service_details = []
        
        for sub in active_subs:
            available_content_types.update(sub.content_types)
            available_services.append(sub.service_name)
            
            service_info = self.service_catalog.get(self._normalize_service_name(sub.service_name), {})
            service_details.append({
                "name": sub.service_name,
                "content_types": [ct.value for ct in sub.content_types],
                "strengths": service_info.get("strengths", []),
                "preferences": sub.preferences or {}
            })
        
        return {
            "total_subscriptions": len(active_subs),
            "available_content_types": list(available_content_types),
            "available_services": available_services,
            "service_details": service_details,
            "content_diversity": len(available_content_types),
            "analysis": self._generate_subscription_analysis(active_subs, available_content_types),
            "recommendations_per_service": self._distribute_recommendations(service_details)
        }
    
    def _generate_subscription_analysis(self, subscriptions: List[Subscription], content_types: Set[ContentType]) -> str:
        """Generate human-readable subscription analysis"""
        if not subscriptions:
            return "No active subscriptions found. Recommendations will be limited to free content."
        
        service_names = [sub.service_name for sub in subscriptions]
        
        if len(subscriptions) == 1:
            analysis = f"You have {service_names[0]} available. "
        elif len(subscriptions) == 2:
            analysis = f"You have {service_names[0]} and {service_names[1]} available. "
        else:
            analysis = f"You have {len(subscriptions)} active subscriptions ({', '.join(service_names[:3])}{'...' if len(service_names) > 3 else ''}). "
        
        content_variety = len(content_types)
        if content_variety >= 5:
            analysis += "Excellent variety of content available across your subscriptions!"
        elif content_variety >= 3:
            analysis += "Good variety of content types available."
        else:
            analysis += "Limited content variety - consider diversifying your subscriptions."
        
        return analysis
    
    def _distribute_recommendations(self, service_details: List[Dict]) -> Dict[str, int]:
        """
        Distribute recommendation slots across services
        Ensures variety in recommendations
        """
        if not service_details:
            return {}
        
        total_recommendations = 5
        equal_distribution = total_recommendations // len(service_details)
        remainder = total_recommendations % len(service_details)
        
        distribution = {}
        for i, service in enumerate(service_details):
            base_count = equal_distribution
            # Give remainder to first services
            if i < remainder:
                base_count += 1
            distribution[service["name"]] = max(1, base_count)
        
        return distribution
    
    def get_service_for_content_type(self, content_type: ContentType, subscriptions: List[Subscription]) -> List[str]:
        """
        Get list of services that provide a specific content type
        
        Args:
            content_type: Type of content
            subscriptions: User subscriptions
            
        Returns:
            List of service names that provide the content type
        """
        matching_services = []
        for sub in subscriptions:
            if sub.is_active and content_type in sub.content_types:
                matching_services.append(sub.service_name)
        return matching_services
    
    def get_subscription_value_score(self, subscriptions: List[Subscription]) -> float:
        """
        Calculate a score representing the value/diversity of subscriptions
        Higher score = more content options = more confident recommendations
        """
        if not subscriptions:
            return 0.3
        
        active_subs = [sub for sub in subscriptions if sub.is_active]
        content_types = set()
        for sub in active_subs:
            content_types.update(sub.content_types)
        
        # Score based on number and diversity
        base_score = min(len(active_subs) * 0.2, 0.6)
        diversity_score = min(len(content_types) * 0.1, 0.4)
        
        return min(base_score + diversity_score, 1.0)
