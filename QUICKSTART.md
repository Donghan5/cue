# 🎯 Quick Start Guide

This guide will help you get started with the CUE AI-Agentic Recommendation System in minutes!

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Donghan5/cue.git
   cd cue
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **You're ready to go!** No API keys or configuration required for basic usage.

## Three Ways to Use CUE

### 1. 🖥️ Interactive CLI (Recommended for First-Time Users)

The easiest way to experience CUE:

```bash
python main.py
```

**What happens:**
1. You'll be asked about your current mood (Happy, Sad, Energetic, etc.)
2. You'll describe your context (Time of day, available minutes, who you're with)
3. You'll select your streaming subscriptions
4. CUE analyzes everything and gives you 5 personalized recommendations in under 1 second!

**Example Session:**
```
🔍 AI DETECTIVE - Content Recommendation System
Solving your 45-minute decision fatigue!

📊 STEP 1: How are you feeling right now?
  1. Happy
  2. Sad
  3. Energetic
  ...

Enter number (1-10): 3

⏰ STEP 2: Tell me about your current situation
...

🎯 INVESTIGATION COMPLETE!
```

### 2. 📝 Run Pre-Built Examples

See CUE in action with different scenarios:

```bash
python examples.py
```

**This shows:**
- Quick recommendation for a relaxed evening
- Stressed user needing to unwind
- Energetic user with friends

Perfect for understanding how the system adapts to different situations!

### 3. 💻 Use as a Python Library

Integrate CUE into your own projects:

```python
from src.models.data_models import (
    Mood, Context, Subscription, UserProfile, ContentType
)
from src.agents.ai_detective import AIDetective

# Initialize
detective = AIDetective()

# Create user profile
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
    user_id="user123",
    current_mood=Mood.RELAXED,
    context=context,
    subscriptions=subscriptions
)

# Get recommendations
response = detective.investigate(user_profile)

# Use the results
print(f"Got {len(response.recommendations)} recommendations!")
print(f"Decision time: {response.decision_time:.2f}s")
print(f"Confidence: {response.confidence:.0f}%")

for rec in response.recommendations:
    print(f"- {rec.title} ({rec.match_score}/100)")
```

## 🎭 Understanding Moods

CUE supports 10 different mood states:

| Mood | Best For | Recommended Content |
|------|----------|---------------------|
| **Happy** | Uplifting vibes | Comedy, Adventure, Upbeat music |
| **Sad** | Emotional processing | Drama, Documentary, Acoustic music |
| **Energetic** | High energy activities | Action, Thriller, Rock music |
| **Tired** | Relaxation | Sitcoms, Nature docs, Ambient music |
| **Stressed** | Unwinding | Comedy, Nature, Chill music |
| **Relaxed** | Pleasant enjoyment | Romance, Jazz, Indie |
| **Bored** | Stimulation | Mystery, Sci-fi, Variety |
| **Excited** | New experiences | Action, Adventure, New releases |
| **Anxious** | Comfort | Familiar favorites, Soft music |
| **Calm** | Peace | Drama, Documentary, Classical |

## 📺 Supported Streaming Services

CUE works with these popular services:

- **Video**: Netflix, Amazon Prime, Disney+, HBO Max, Hulu, YouTube Premium
- **Music**: Spotify, Apple Music
- **Audio**: Audible, Podcasts
- **Reading**: Kindle Unlimited

Don't have subscriptions? CUE will suggest free content too!

## ⏱️ How Fast is CUE?

**Decision time: < 1 second!**

No more 45 minutes of scrolling. CUE analyzes your mood, context, and subscriptions to give you recommendations instantly.

## 🎯 What You Get

Each recommendation includes:

- **Title** and **Service** (where to watch/listen)
- **Duration** (so you know if it fits your time)
- **Match Score** (0-100, how well it fits you)
- **Genre** information
- **Reasoning** (why CUE chose this for you)
- **Mood Alignment** (how it matches your current state)

Plus:
- **Overall Analysis** of your situation
- **Confidence Score** in the recommendations
- **Decision Time** (always under 1 second!)

## 🚀 Advanced Usage

### Customize Your Profile

```python
# Add viewing history to avoid repeats
user_profile = UserProfile(
    user_id="user123",
    current_mood=Mood.HAPPY,
    context=context,
    subscriptions=subscriptions,
    viewing_history=["The Office", "Stranger Things"],
    preferences={"favorite_genre": "sci-fi"}
)
```

### Multiple Subscriptions

```python
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
        service_name="Disney Plus",
        content_types=[ContentType.MOVIE, ContentType.TV_SHOW],
        is_active=True
    )
]
```

### Social Context Matters

```python
# Different recommendations for different situations
context_alone = Context(
    time_of_day="night",
    available_time=60,
    social_context="alone"  # Personal favorites
)

context_friends = Context(
    time_of_day="evening",
    available_time=120,
    social_context="with_friends"  # Popular, group-friendly content
)

context_family = Context(
    time_of_day="afternoon",
    available_time=90,
    social_context="with_family"  # Family-friendly content
)
```

## 💡 Pro Tips

1. **Be honest about your mood** - CUE works best with accurate mood information
2. **Specify available time** - Helps CUE filter content that actually fits
3. **Update your subscriptions** - Get recommendations from services you actually have
4. **Try different scenarios** - See how CUE adapts to your changing needs
5. **Check the reasoning** - Learn why CUE chose specific content for you

## 🤔 FAQ

**Q: Does CUE need internet?**
A: No! CUE runs completely offline with its built-in content database.

**Q: Do I need API keys?**
A: No! The system works out of the box without any external APIs.

**Q: Can I add more content?**
A: Yes! Edit `src/agents/ai_detective.py` and add to the `_initialize_content_database()` method.

**Q: Can I add more streaming services?**
A: Yes! Edit `src/agents/subscription_analyzer.py` to add service definitions.

**Q: How accurate are the recommendations?**
A: CUE uses a sophisticated scoring system considering mood, context, and subscriptions. Confidence scores typically range from 70-100%.

**Q: Can I use this commercially?**
A: Yes! This is open source (MIT License).

## 🐛 Troubleshooting

**Import errors?**
```bash
# Make sure you installed dependencies
pip install -r requirements.txt
```

**Python version issues?**
```bash
# CUE requires Python 3.8+
python --version
```

**Module not found?**
```bash
# Run from the project root directory
cd /path/to/cue
python main.py
```

## 🎉 Next Steps

1. **Try the CLI**: `python main.py`
2. **Run examples**: `python examples.py`
3. **Build your own integration**: Use as a Python library
4. **Customize**: Add your favorite content to the database
5. **Share**: Tell others about decision-free content discovery!

---

**Happy content discovering! 🎬🎵📚**

Built to solve decision fatigue - because life's too short to spend 45 minutes deciding what to watch!
