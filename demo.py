#!/usr/bin/env python3
"""
Interactive Demo - Shows the AI Detective in action with various scenarios
"""
import time
from src.models.data_models import (
    Mood, ContentType, Context, Subscription, UserProfile
)
from src.agents.ai_detective import AIDetective


def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def print_scenario(number, description):
    """Print scenario header"""
    print(f"\n🎬 SCENARIO {number}: {description}")
    print("-" * 70)


def print_recommendations(response):
    """Print recommendations in a nice format"""
    print(f"\n⏱️  Decision Time: {response.decision_time:.3f} seconds")
    print(f"🎯 Confidence: {response.confidence:.0f}%")
    print(f"\n📋 Analysis:\n   {response.analysis}")
    print(f"\n💡 Top Recommendations:")
    
    for i, rec in enumerate(response.recommendations[:3], 1):
        print(f"\n   {i}. {rec.title}")
        print(f"      Service: {rec.service} | Duration: {rec.duration} min | Score: {rec.match_score:.0f}/100")
        print(f"      {rec.reasoning}")


def demo_weekend_morning():
    """Demo: Weekend morning, energetic mood"""
    print_scenario(1, "Weekend Morning - Energetic & Ready for Action")
    
    detective = AIDetective()
    
    context = Context(
        time_of_day="morning",
        day_of_week="Saturday",
        available_time=120,
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
    
    profile = UserProfile(
        user_id="demo_user_1",
        current_mood=Mood.ENERGETIC,
        context=context,
        subscriptions=subscriptions
    )
    
    print("\n👤 User Profile:")
    print(f"   Mood: {profile.current_mood.value.capitalize()}")
    print(f"   Time: {context.time_of_day.capitalize()}, {context.day_of_week}")
    print(f"   Available Time: {context.available_time} minutes")
    print(f"   Subscriptions: {', '.join([s.service_name for s in subscriptions])}")
    
    print("\n🔍 Investigating...")
    time.sleep(0.5)  # Dramatic pause
    
    response = detective.investigate(profile)
    print_recommendations(response)


def demo_stressed_evening():
    """Demo: Stressful workday evening"""
    print_scenario(2, "Stressful Workday Evening - Need to Unwind")
    
    detective = AIDetective()
    
    context = Context(
        time_of_day="evening",
        day_of_week="Monday",
        available_time=60,
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
        ),
        Subscription(
            service_name="Audible",
            content_types=[ContentType.BOOK, ContentType.PODCAST],
            is_active=True
        )
    ]
    
    profile = UserProfile(
        user_id="demo_user_2",
        current_mood=Mood.STRESSED,
        context=context,
        subscriptions=subscriptions
    )
    
    print("\n👤 User Profile:")
    print(f"   Mood: {profile.current_mood.value.capitalize()} 😓")
    print(f"   Time: {context.time_of_day.capitalize()}, {context.day_of_week}")
    print(f"   Available Time: {context.available_time} minutes")
    print(f"   Context: After a long workday, needs relaxation")
    
    print("\n🔍 Investigating...")
    time.sleep(0.5)
    
    response = detective.investigate(profile)
    print_recommendations(response)


def demo_family_time():
    """Demo: Weekend family time"""
    print_scenario(3, "Weekend Family Time - Quality Time Together")
    
    detective = AIDetective()
    
    context = Context(
        time_of_day="afternoon",
        day_of_week="Sunday",
        available_time=150,
        social_context="with_family"
    )
    
    subscriptions = [
        Subscription(
            service_name="Disney Plus",
            content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
            is_active=True
        ),
        Subscription(
            service_name="Netflix",
            content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
            is_active=True
        )
    ]
    
    profile = UserProfile(
        user_id="demo_user_3",
        current_mood=Mood.HAPPY,
        context=context,
        subscriptions=subscriptions
    )
    
    print("\n👤 User Profile:")
    print(f"   Mood: {profile.current_mood.value.capitalize()} 😊")
    print(f"   Time: {context.time_of_day.capitalize()}, {context.day_of_week}")
    print(f"   Available Time: {context.available_time} minutes")
    print(f"   Social Context: {context.social_context.replace('_', ' ').title()}")
    
    print("\n🔍 Investigating...")
    time.sleep(0.5)
    
    response = detective.investigate(profile)
    print_recommendations(response)


def demo_late_night_bored():
    """Demo: Late night, bored, limited subscriptions"""
    print_scenario(4, "Late Night Boredom - Limited Time & Options")
    
    detective = AIDetective()
    
    context = Context(
        time_of_day="night",
        day_of_week="Wednesday",
        available_time=30,
        social_context="alone"
    )
    
    subscriptions = [
        Subscription(
            service_name="YouTube Premium",
            content_types=[ContentType.VIDEO, ContentType.MUSIC],
            is_active=True
        )
    ]
    
    profile = UserProfile(
        user_id="demo_user_4",
        current_mood=Mood.BORED,
        context=context,
        subscriptions=subscriptions
    )
    
    print("\n👤 User Profile:")
    print(f"   Mood: {profile.current_mood.value.capitalize()} 😐")
    print(f"   Time: {context.time_of_day.capitalize()}, {context.day_of_week}")
    print(f"   Available Time: Only {context.available_time} minutes")
    print(f"   Subscriptions: Limited options")
    
    print("\n🔍 Investigating...")
    time.sleep(0.5)
    
    response = detective.investigate(profile)
    print_recommendations(response)


def demo_quick_decision():
    """Demo: Show how fast the system is"""
    print_scenario(5, "Speed Test - Solving 45-Minute Decision Fatigue")
    
    detective = AIDetective()
    
    print("\n⏰ The Problem: Average person spends 45 minutes deciding what to watch")
    print("✨ The Solution: AI Detective analyzes and decides in milliseconds")
    
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
    
    profile = UserProfile(
        user_id="demo_user_5",
        current_mood=Mood.RELAXED,
        context=context,
        subscriptions=subscriptions
    )
    
    print("\n🏃 Running speed test...")
    
    # Run multiple times and average
    times = []
    for i in range(5):
        response = detective.investigate(profile)
        times.append(response.decision_time)
        print(f"   Attempt {i+1}: {response.decision_time*1000:.2f} ms")
    
    avg_time = sum(times) / len(times)
    traditional_time = 45 * 60  # 45 minutes in seconds
    speedup = traditional_time / avg_time
    time_saved = traditional_time - avg_time
    
    print(f"\n📊 Results:")
    print(f"   Average Decision Time: {avg_time*1000:.2f} milliseconds")
    print(f"   Traditional Time: 45 minutes (2,700 seconds)")
    print(f"   Speed Improvement: {speedup:.0f}x faster")
    print(f"   Time Saved: {time_saved/60:.1f} minutes per decision")
    print(f"\n💡 That's {(time_saved/60)*365:.0f} minutes saved per year (daily use)!")


def main():
    """Run all demo scenarios"""
    print_header("🔍 AI DETECTIVE - Interactive Demo")
    print("\nWelcome to the AI-Agentic Content Recommendation System!")
    print("This demo shows how the AI Detective solves decision fatigue")
    print("by analyzing mood, context, and subscriptions.")
    
    # Run all scenarios
    demo_weekend_morning()
    input("\n\nPress Enter to continue to next scenario...")
    
    demo_stressed_evening()
    input("\n\nPress Enter to continue to next scenario...")
    
    demo_family_time()
    input("\n\nPress Enter to continue to next scenario...")
    
    demo_late_night_bored()
    input("\n\nPress Enter to continue to speed test...")
    
    demo_quick_decision()
    
    # Final message
    print_header("🎉 Demo Complete!")
    print("\n✅ You've seen how the AI Detective:")
    print("   • Analyzes mood, context, and subscriptions")
    print("   • Provides personalized recommendations")
    print("   • Makes decisions in milliseconds, not minutes")
    print("   • Adapts to different scenarios and moods")
    print("   • Solves the 45-minute decision fatigue problem")
    
    print("\n🚀 Try it yourself:")
    print("   • Run 'python main.py' for interactive CLI")
    print("   • Run 'python examples.py' for more examples")
    print("   • Import as a library in your own code")
    
    print("\n💡 Remember: Life's too short to spend 45 minutes deciding what to watch!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for watching!")
