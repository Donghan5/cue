"""
Command-line interface for the AI-Agentic Recommendation System
"""
import sys
from typing import List
from datetime import datetime

from src.models.data_models import (
    Mood, ContentType, Context, Subscription, UserProfile
)
from src.agents.ai_detective import AIDetective


class RecommendationCLI:
    """Interactive CLI for getting content recommendations"""
    
    def __init__(self):
        self.detective = AIDetective()
        print("\n" + "="*70)
        print("🔍 AI DETECTIVE - Content Recommendation System")
        print("Solving your 45-minute decision fatigue!")
        print("="*70 + "\n")
    
    def run(self):
        """Main CLI loop"""
        try:
            # Gather user information
            print("Let me investigate your situation to find the perfect content...\n")
            
            # Step 1: Get mood
            mood = self._get_mood()
            
            # Step 2: Get context
            context = self._get_context()
            
            # Step 3: Get subscriptions
            subscriptions = self._get_subscriptions()
            
            # Create user profile
            user_profile = UserProfile(
                user_id="cli_user",
                current_mood=mood,
                context=context,
                subscriptions=subscriptions,
                viewing_history=[]
            )
            
            # Get recommendations
            print("\n🔍 Investigating your preferences...")
            print("⚡ Analyzing mood, context, and subscriptions...")
            
            response = self.detective.investigate(user_profile)
            
            # Display results
            self._display_results(response)
            
        except KeyboardInterrupt:
            print("\n\nInvestigation cancelled. See you next time! 👋")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    
    def _get_mood(self) -> Mood:
        """Interactive mood selection"""
        print("📊 STEP 1: How are you feeling right now?")
        moods = list(Mood)
        for i, mood in enumerate(moods, 1):
            print(f"  {i}. {mood.value.capitalize()}")
        
        while True:
            try:
                choice = input("\nEnter number (1-{}): ".format(len(moods)))
                idx = int(choice) - 1
                if 0 <= idx < len(moods):
                    selected = moods[idx]
                    print(f"✓ Selected: {selected.value.capitalize()}\n")
                    return selected
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def _get_context(self) -> Context:
        """Interactive context gathering"""
        print("⏰ STEP 2: Tell me about your current situation")
        
        # Time of day
        print("\nWhat time of day is it?")
        times = ["morning", "afternoon", "evening", "night"]
        for i, time in enumerate(times, 1):
            print(f"  {i}. {time.capitalize()}")
        
        while True:
            try:
                choice = input("Enter number (1-4): ")
                idx = int(choice) - 1
                if 0 <= idx < len(times):
                    time_of_day = times[idx]
                    break
            except ValueError:
                pass
            print("Invalid choice. Please try again.")
        
        # Day of week
        current_day = datetime.now().strftime("%A")
        print(f"\n✓ Detected day: {current_day}")
        
        # Available time
        while True:
            try:
                available_time = int(input("\nHow many minutes do you have? "))
                if available_time > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Social context
        print("\nWho are you with?")
        social_options = ["alone", "with_friends", "with_family", "with_partner"]
        for i, option in enumerate(social_options, 1):
            print(f"  {i}. {option.replace('_', ' ').capitalize()}")
        
        while True:
            try:
                choice = input("Enter number (1-4): ")
                idx = int(choice) - 1
                if 0 <= idx < len(social_options):
                    social_context = social_options[idx]
                    break
            except ValueError:
                pass
            print("Invalid choice. Please try again.")
        
        print("✓ Context gathered\n")
        
        return Context(
            time_of_day=time_of_day,
            day_of_week=current_day,
            available_time=available_time,
            social_context=social_context
        )
    
    def _get_subscriptions(self) -> List[Subscription]:
        """Interactive subscription gathering"""
        print("📺 STEP 3: What streaming services do you have?")
        
        available_services = {
            "1": ("Netflix", [ContentType.MOVIE, ContentType.TV_SHOW]),
            "2": ("Spotify", [ContentType.MUSIC, ContentType.PODCAST]),
            "3": ("Amazon Prime", [ContentType.MOVIE, ContentType.TV_SHOW, ContentType.MUSIC]),
            "4": ("Disney Plus", [ContentType.MOVIE, ContentType.TV_SHOW]),
            "5": ("HBO Max", [ContentType.MOVIE, ContentType.TV_SHOW]),
            "6": ("Hulu", [ContentType.MOVIE, ContentType.TV_SHOW]),
            "7": ("YouTube Premium", [ContentType.VIDEO, ContentType.MUSIC]),
            "8": ("Apple Music", [ContentType.MUSIC, ContentType.PODCAST]),
            "9": ("Audible", [ContentType.BOOK, ContentType.PODCAST]),
        }
        
        print("\nSelect your subscriptions (enter numbers separated by commas):")
        for key, (name, _) in available_services.items():
            print(f"  {key}. {name}")
        print("  0. None / Skip")
        
        choice = input("\nYour subscriptions (e.g., 1,2,3): ").strip()
        
        subscriptions = []
        if choice and choice != "0":
            selected = [s.strip() for s in choice.split(",")]
            for sel in selected:
                if sel in available_services:
                    name, content_types = available_services[sel]
                    subscriptions.append(Subscription(
                        service_name=name,
                        content_types=content_types,
                        is_active=True
                    ))
        
        if subscriptions:
            print(f"✓ {len(subscriptions)} subscription(s) added\n")
        else:
            print("✓ No subscriptions (will show free content)\n")
        
        return subscriptions
    
    def _display_results(self, response):
        """Display recommendation results"""
        print("\n" + "="*70)
        print("🎯 INVESTIGATION COMPLETE!")
        print("="*70)
        
        print(f"\n⏱️  Decision Time: {response.decision_time:.2f} seconds")
        print(f"🎯 Confidence: {response.confidence:.0f}%")
        
        print(f"\n📋 ANALYSIS:")
        print(f"   {response.analysis}")
        
        print(f"\n🎬 TOP RECOMMENDATIONS:")
        print("="*70)
        
        for i, rec in enumerate(response.recommendations, 1):
            print(f"\n{i}. {rec.title}")
            print(f"   Type: {rec.content_type.value.replace('_', ' ').title()}")
            print(f"   Service: {rec.service}")
            print(f"   Duration: {rec.duration} minutes")
            print(f"   Match Score: {rec.match_score:.0f}/100")
            if rec.genre:
                print(f"   Genre: {', '.join(rec.genre)}")
            print(f"   💡 {rec.reasoning}")
            print(f"   😊 {rec.mood_alignment}")
        
        print("\n" + "="*70)
        print("Enjoy your content! Decision fatigue solved! 🎉")
        print("="*70 + "\n")


def main():
    """Entry point for CLI"""
    cli = RecommendationCLI()
    cli.run()


if __name__ == "__main__":
    main()
