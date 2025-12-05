"""
Unit tests for the AI-Agentic Recommendation System
"""
import unittest
from src.models.data_models import (
    Mood, ContentType, Context, Subscription, UserProfile
)
from src.agents.mood_analyzer import MoodAnalyzer
from src.agents.context_analyzer import ContextAnalyzer
from src.agents.subscription_analyzer import SubscriptionAnalyzer
from src.agents.ai_detective import AIDetective


class TestMoodAnalyzer(unittest.TestCase):
    """Test the Mood Analyzer component"""
    
    def setUp(self):
        self.analyzer = MoodAnalyzer()
    
    def test_happy_mood_analysis(self):
        """Test analysis of happy mood"""
        result = self.analyzer.analyze_mood(Mood.HAPPY)
        self.assertEqual(result["mood"], "happy")
        self.assertEqual(result["energy_level"], "high")
        self.assertIn("comedy", result["preferred_genres"])
        self.assertIn("horror", result["avoid_genres"])
    
    def test_stressed_mood_analysis(self):
        """Test analysis of stressed mood"""
        result = self.analyzer.analyze_mood(Mood.STRESSED)
        self.assertEqual(result["mood"], "stressed")
        self.assertEqual(result["energy_level"], "low")
        self.assertIn("calming", result["preferred_tone"])
    
    def test_mood_weight_priority(self):
        """Test that stressed moods get higher priority"""
        stressed_weight = self.analyzer.get_mood_weight(Mood.STRESSED)
        happy_weight = self.analyzer.get_mood_weight(Mood.HAPPY)
        self.assertGreater(stressed_weight, happy_weight)
    
    def test_all_moods_have_mapping(self):
        """Test that all mood states have content mappings"""
        for mood in Mood:
            result = self.analyzer.analyze_mood(mood)
            self.assertIn("mood", result)
            self.assertIn("energy_level", result)
            self.assertIn("analysis", result)


class TestContextAnalyzer(unittest.TestCase):
    """Test the Context Analyzer component"""
    
    def setUp(self):
        self.analyzer = ContextAnalyzer()
    
    def test_evening_context(self):
        """Test evening context analysis"""
        context = Context(
            time_of_day="evening",
            day_of_week="Friday",
            available_time=90,
            social_context="alone"
        )
        result = self.analyzer.analyze_context(context)
        self.assertEqual(result["time_of_day"], "evening")
        self.assertEqual(result["energy_phase"], "winding_down")
        self.assertIn("analysis", result)
    
    def test_morning_context(self):
        """Test morning context analysis"""
        context = Context(
            time_of_day="morning",
            day_of_week="Monday",
            available_time=30,
            social_context="alone"
        )
        result = self.analyzer.analyze_context(context)
        self.assertIn("podcast", result["suitable_content_types"])
    
    def test_duration_constraints(self):
        """Test that duration recommendations respect available time"""
        context = Context(
            time_of_day="evening",
            day_of_week="Friday",
            available_time=45,
            social_context="alone"
        )
        result = self.analyzer.analyze_context(context)
        min_dur, max_dur = result["recommended_duration_range"]
        self.assertLessEqual(max_dur, 45)
        self.assertGreater(min_dur, 0)
    
    def test_content_appropriateness(self):
        """Test content type appropriateness for context"""
        morning_context = Context(
            time_of_day="morning",
            day_of_week="Monday",
            available_time=30,
            social_context="alone"
        )
        # Podcasts are appropriate in the morning
        self.assertTrue(
            self.analyzer.is_content_appropriate(ContentType.PODCAST, morning_context)
        )
    
    def test_urgency_factor(self):
        """Test urgency calculation based on available time"""
        # Very little time = high urgency
        high_urgency = self.analyzer.get_urgency_factor(10)
        low_urgency = self.analyzer.get_urgency_factor(120)
        self.assertGreater(high_urgency, low_urgency)


class TestSubscriptionAnalyzer(unittest.TestCase):
    """Test the Subscription Analyzer component"""
    
    def setUp(self):
        self.analyzer = SubscriptionAnalyzer()
    
    def test_single_subscription(self):
        """Test analysis with one subscription"""
        subscriptions = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
                is_active=True
            )
        ]
        result = self.analyzer.analyze_subscriptions(subscriptions)
        self.assertEqual(result["total_subscriptions"], 1)
        self.assertIn("Netflix", result["available_services"])
        self.assertEqual(result["content_diversity"], 2)
    
    def test_multiple_subscriptions(self):
        """Test analysis with multiple subscriptions"""
        subscriptions = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
                is_active=True
            ),
            Subscription(
                service_name="Spotify",
                content_types=[ContentType.MUSIC, ContentType.PODCAST],
                is_active=True
            )
        ]
        result = self.analyzer.analyze_subscriptions(subscriptions)
        self.assertEqual(result["total_subscriptions"], 2)
        self.assertEqual(result["content_diversity"], 4)
    
    def test_inactive_subscriptions_ignored(self):
        """Test that inactive subscriptions are filtered out"""
        subscriptions = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE],
                is_active=True
            ),
            Subscription(
                service_name="Hulu",
                content_types=[ContentType.TV_SHOW],
                is_active=False
            )
        ]
        result = self.analyzer.analyze_subscriptions(subscriptions)
        self.assertEqual(result["total_subscriptions"], 1)
        self.assertNotIn("Hulu", result["available_services"])
    
    def test_no_subscriptions(self):
        """Test behavior with no subscriptions"""
        result = self.analyzer.analyze_subscriptions([])
        self.assertEqual(result["total_subscriptions"], 0)
        self.assertIn("No active subscriptions", result["analysis"])
    
    def test_subscription_value_score(self):
        """Test value score calculation"""
        no_subs_score = self.analyzer.get_subscription_value_score([])
        
        one_sub = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE],
                is_active=True
            )
        ]
        one_sub_score = self.analyzer.get_subscription_value_score(one_sub)
        
        self.assertGreater(one_sub_score, no_subs_score)


class TestAIDetective(unittest.TestCase):
    """Test the main AI Detective coordinator"""
    
    def setUp(self):
        self.detective = AIDetective()
    
    def test_basic_investigation(self):
        """Test basic recommendation flow"""
        context = Context(
            time_of_day="evening",
            day_of_week="Friday",
            available_time=90,
            social_context="alone"
        )
        
        subscriptions = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
                is_active=True
            )
        ]
        
        user_profile = UserProfile(
            user_id="test_user",
            current_mood=Mood.RELAXED,
            context=context,
            subscriptions=subscriptions
        )
        
        response = self.detective.investigate(user_profile)
        
        # Verify response structure
        self.assertIsNotNone(response)
        self.assertGreater(len(response.recommendations), 0)
        self.assertGreater(response.confidence, 0)
        self.assertLess(response.decision_time, 1.0)  # Should be fast!
        self.assertIsNotNone(response.analysis)
    
    def test_recommendations_count(self):
        """Test that we get the right number of recommendations"""
        user_profile = self._create_test_profile()
        response = self.detective.investigate(user_profile)
        self.assertLessEqual(len(response.recommendations), 5)
    
    def test_recommendation_quality(self):
        """Test that recommendations have required fields"""
        user_profile = self._create_test_profile()
        response = self.detective.investigate(user_profile)
        
        for rec in response.recommendations:
            self.assertIsNotNone(rec.title)
            self.assertIsNotNone(rec.service)
            self.assertGreater(rec.duration, 0)
            self.assertGreaterEqual(rec.match_score, 0)
            self.assertLessEqual(rec.match_score, 100)
            self.assertIsNotNone(rec.reasoning)
    
    def test_stressed_mood_recommendations(self):
        """Test that stressed mood gets calming content"""
        context = Context(
            time_of_day="night",
            day_of_week="Monday",
            available_time=45,
            social_context="alone"
        )
        
        subscriptions = [
            Subscription(
                service_name="Spotify",
                content_types=[ContentType.MUSIC, ContentType.PODCAST],
                is_active=True
            )
        ]
        
        user_profile = UserProfile(
            user_id="stressed_user",
            current_mood=Mood.STRESSED,
            context=context,
            subscriptions=subscriptions
        )
        
        response = self.detective.investigate(user_profile)
        
        # Should recommend calming content
        self.assertGreater(len(response.recommendations), 0)
        # Analysis should mention unwinding or stress relief
        self.assertTrue(
            "unwind" in response.analysis.lower() or "stress" in response.analysis.lower(),
            "Analysis should mention stress relief"
        )
    
    def test_no_subscriptions_handling(self):
        """Test that system handles users with no subscriptions"""
        context = Context(
            time_of_day="evening",
            day_of_week="Friday",
            available_time=60,
            social_context="alone"
        )
        
        user_profile = UserProfile(
            user_id="free_user",
            current_mood=Mood.HAPPY,
            context=context,
            subscriptions=[]
        )
        
        response = self.detective.investigate(user_profile)
        
        # Should still provide recommendations (free content)
        self.assertGreater(len(response.recommendations), 0)
    
    def test_performance(self):
        """Test that recommendations are generated quickly"""
        user_profile = self._create_test_profile()
        response = self.detective.investigate(user_profile)
        
        # Should be under 1 second (solving 45-minute decision fatigue!)
        self.assertLess(response.decision_time, 1.0)
    
    def _create_test_profile(self):
        """Helper to create a standard test profile"""
        context = Context(
            time_of_day="evening",
            day_of_week="Friday",
            available_time=90,
            social_context="alone"
        )
        
        subscriptions = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
                is_active=True
            ),
            Subscription(
                service_name="Spotify",
                content_types=[ContentType.MUSIC, ContentType.PODCAST],
                is_active=True
            )
        ]
        
        return UserProfile(
            user_id="test_user",
            current_mood=Mood.RELAXED,
            context=context,
            subscriptions=subscriptions
        )


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_flow(self):
        """Test complete flow from user input to recommendations"""
        # Simulate user input
        context = Context(
            time_of_day="evening",
            day_of_week="Saturday",
            available_time=120,
            social_context="with_friends"
        )
        
        subscriptions = [
            Subscription(
                service_name="Netflix",
                content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
                is_active=True
            ),
            Subscription(
                service_name="Disney Plus",
                content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
                is_active=True
            )
        ]
        
        user_profile = UserProfile(
            user_id="integration_test",
            current_mood=Mood.EXCITED,
            context=context,
            subscriptions=subscriptions
        )
        
        # Get recommendations
        detective = AIDetective()
        response = detective.investigate(user_profile)
        
        # Verify complete response
        self.assertIsNotNone(response)
        self.assertGreater(len(response.recommendations), 0)
        self.assertGreater(response.confidence, 0)
        self.assertIsNotNone(response.analysis)
        self.assertIsNotNone(response.timestamp)
        
        # Verify recommendations match context
        for rec in response.recommendations:
            # Should be from available services
            self.assertIn(rec.service, ["Netflix", "Disney Plus"])
            # Should respect time constraint
            self.assertLessEqual(rec.duration, 120)


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
