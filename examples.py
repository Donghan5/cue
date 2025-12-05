"""
Example usage of the AI-Agentic Recommendation System API
"""
from src.models.data_models import (
    Mood, ContentType, Context, Subscription, UserProfile
)
from src.agents.ai_detective import AIDetective


def quick_recommendation_example():
    """Quick example of getting recommendations"""
    
    # Create the AI Detective
    detective = AIDetective()
    
    # Define user context
    context = Context(
        time_of_day="evening",
        day_of_week="Friday",
        available_time=90,
        social_context="alone"
    )
    
    # Define user subscriptions
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
    
    # Create user profile
    user_profile = UserProfile(
        user_id="example_user",
        current_mood=Mood.RELAXED,
        context=context,
        subscriptions=subscriptions
    )
    
    # Get recommendations
    response = detective.investigate(user_profile)
    
    # Display results
    print("\n" + "="*70)
    print("AI DETECTIVE RECOMMENDATION REPORT")
    print("="*70)
    print(f"\nDecision Time: {response.decision_time:.3f} seconds")
    print(f"Confidence: {response.confidence:.1f}%")
    print(f"\nAnalysis:\n{response.analysis}")
    print(f"\nTop Recommendations:")
    
    for i, rec in enumerate(response.recommendations, 1):
        print(f"\n{i}. {rec.title}")
        print(f"   Service: {rec.service} | Duration: {rec.duration}min | Score: {rec.match_score:.0f}/100")
        print(f"   {rec.reasoning}")
    
    print("\n" + "="*70 + "\n")
    
    return response


def stressed_user_example():
    """Example for a stressed user needing to unwind"""
    
    detective = AIDetective()
    
    context = Context(
        time_of_day="night",
        day_of_week="Monday",
        available_time=45,
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
    
    user_profile = UserProfile(
        user_id="stressed_user",
        current_mood=Mood.STRESSED,
        context=context,
        subscriptions=subscriptions
    )
    
    response = detective.investigate(user_profile)
    
    print("\n" + "="*70)
    print("STRESSED USER SCENARIO")
    print("="*70)
    print(f"\nAnalysis:\n{response.analysis}")
    print(f"\nRecommendations to help you unwind:")
    
    for rec in response.recommendations[:3]:
        print(f"\n• {rec.title} ({rec.service})")
        print(f"  {rec.reasoning}")
    
    print("\n" + "="*70 + "\n")
    
    return response


def energetic_user_example():
    """Example for an energetic user with lots of time"""
    
    detective = AIDetective()
    
    context = Context(
        time_of_day="afternoon",
        day_of_week="Saturday",
        available_time=150,
        social_context="with_friends"
    )
    
    subscriptions = [
        Subscription(
            service_name="Disney Plus",
            content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
            is_active=True
        ),
        Subscription(
            service_name="HBO Max",
            content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
            is_active=True
        )
    ]
    
    user_profile = UserProfile(
        user_id="energetic_user",
        current_mood=Mood.ENERGETIC,
        context=context,
        subscriptions=subscriptions
    )
    
    response = detective.investigate(user_profile)
    
    print("\n" + "="*70)
    print("ENERGETIC USER SCENARIO")
    print("="*70)
    print(f"\nAnalysis:\n{response.analysis}")
    print(f"\nHigh-energy recommendations:")
    
    for rec in response.recommendations[:3]:
        print(f"\n• {rec.title} ({rec.service})")
        print(f"  Duration: {rec.duration} min | Score: {rec.match_score:.0f}/100")
    
    print("\n" + "="*70 + "\n")
    
    return response


if __name__ == "__main__":
    print("\n🔍 AI DETECTIVE - Example Usage\n")
    print("Running example scenarios...\n")
    
    # Run examples
    print("\n--- Example 1: Quick Recommendation ---")
    quick_recommendation_example()
    
    print("\n--- Example 2: Stressed User ---")
    stressed_user_example()
    
    print("\n--- Example 3: Energetic User ---")
    energetic_user_example()
    
    print("\n✅ All examples completed!")
