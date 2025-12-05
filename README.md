# 🔍 CUE - AI-Agentic Content Recommendation System

**Solving your 45-minute decision fatigue with intelligent content recommendations!**

## 🎯 Overview

CUE is an AI-powered detective system that analyzes your mood, context, and subscriptions to provide personalized content recommendations in seconds. No more endless scrolling or decision paralysis - just curated content that matches your current state perfectly.

## ✨ Features

- **🧠 Mood Analysis**: Understands 10 different mood states and matches content accordingly
- **⏰ Context Awareness**: Considers time of day, available time, social setting, and more
- **📺 Subscription Intelligence**: Works with your existing streaming services (Netflix, Spotify, etc.)
- **⚡ Fast Decisions**: Provides recommendations in under 1 second
- **🎯 High Confidence**: Smart scoring system ensures quality recommendations
- **💡 Explainable AI**: Every recommendation comes with clear reasoning

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Donghan5/cue.git
cd cue
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your preferences
```

### Usage

#### Interactive CLI

Run the interactive command-line interface:

```bash
python main.py
```

The CLI will guide you through:
1. Selecting your current mood
2. Describing your context (time, available minutes, social setting)
3. Adding your streaming subscriptions
4. Receiving personalized recommendations

#### Programmatic API

Use the system in your own code:

```python
from src.models.data_models import Mood, Context, Subscription, UserProfile, ContentType
from src.agents.ai_detective import AIDetective

# Initialize the detective
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

# Use the recommendations
for rec in response.recommendations:
    print(f"{rec.title} - {rec.match_score}/100")
```

#### Run Examples

See the system in action with pre-built scenarios:

```bash
python examples.py
```

## 📊 System Architecture

The system consists of four main AI agents:

### 1. **AI Detective** (Main Coordinator)
- Orchestrates all analysis components
- Generates final recommendations
- Calculates confidence scores
- Solves decision fatigue in seconds

### 2. **Mood Analyzer**
- Analyzes 10 different mood states
- Maps moods to content preferences
- Determines energy levels and tone
- Identifies genres to prefer or avoid

### 3. **Context Analyzer**
- Evaluates time of day and available time
- Considers social context (alone, with friends, etc.)
- Adjusts for device and location
- Determines appropriate content types

### 4. **Subscription Analyzer**
- Identifies available content sources
- Maximizes subscription value
- Ensures content diversity
- Distributes recommendations across services

## 🎭 Supported Moods

- **Happy** - Uplifting, fun content
- **Sad** - Comforting, cathartic content
- **Energetic** - Fast-paced, exciting content
- **Tired** - Easy-watching, relaxing content
- **Stressed** - Calming, soothing content
- **Relaxed** - Pleasant, comfortable content
- **Bored** - Engaging, stimulating content
- **Excited** - Thrilling, adventurous content
- **Anxious** - Predictable, gentle content
- **Calm** - Peaceful, balanced content

## 📺 Supported Services

- Netflix
- Spotify
- Amazon Prime Video
- Disney+
- HBO Max
- Hulu
- YouTube Premium
- Apple Music
- Audible
- Kindle Unlimited

## 🎬 Content Types

- Movies
- TV Shows
- Music
- Podcasts
- Books/Audiobooks
- Articles
- Videos
- Games

## 🛠️ Project Structure

```
cue/
├── src/
│   ├── agents/
│   │   ├── ai_detective.py         # Main AI coordinator
│   │   ├── mood_analyzer.py        # Mood analysis agent
│   │   ├── context_analyzer.py     # Context analysis agent
│   │   └── subscription_analyzer.py # Subscription analysis agent
│   ├── models/
│   │   └── data_models.py          # Data models and schemas
│   └── __init__.py
├── main.py                          # Interactive CLI
├── examples.py                      # Usage examples
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🧪 Testing

Run the examples to see different scenarios:

```bash
# Run all examples
python examples.py

# Run interactive CLI
python main.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🎯 The Problem We Solve

**Decision Fatigue**: The average person spends 45 minutes deciding what to watch or listen to. With thousands of options across multiple streaming services, choice paralysis is real.

**Our Solution**: CUE acts as your personal AI detective, analyzing your current state (mood, context, subscriptions) and providing curated recommendations in seconds, not minutes.

## 💡 Why "Detective"?

Like a detective investigating a case, CUE:
- 🔍 Gathers clues (mood, context, subscriptions)
- 🧩 Analyzes evidence (content preferences, timing, availability)
- 🎯 Solves the mystery (finding the perfect content)
- ⚡ Delivers results (fast, confident recommendations)

## 🌟 Future Enhancements

- Machine learning integration for personalized learning
- Social features for group recommendations
- Integration with more streaming services
- Mobile app interface
- Voice assistant integration
- Viewing history analysis
- Friend recommendations
- Trending content integration

---

**Built with ❤️ to solve decision fatigue and help you enjoy your content!**
