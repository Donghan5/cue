# 🏗️ System Architecture

## Overview

The CUE AI-Agentic Recommendation System uses a multi-agent architecture where specialized agents collaborate to solve the "45-minute decision fatigue" problem. Each agent is an expert in its domain, and the AI Detective coordinates them to produce optimal recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        User Input                            │
│              (Mood, Context, Subscriptions)                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    🔍 AI DETECTIVE                          │
│                 (Main Coordinator)                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Gather     │  │   Analyze    │  │  Generate    │     │
│  │   Evidence   │─▶│   Evidence   │─▶│  Solution    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────┬──────────────┬──────────────┬─────────────────────┘
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌────────────┐ ┌──────────────────┐
│    Mood      │ │  Context   │ │  Subscription    │
│   Analyzer   │ │  Analyzer  │ │    Analyzer      │
└──────┬───────┘ └─────┬──────┘ └────────┬─────────┘
       │               │                  │
       ▼               ▼                  ▼
┌──────────────────────────────────────────────────┐
│           Content Database & Scoring             │
└──────────────┬───────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────┐
│        🎯 Personalized Recommendations           │
│     (Ranked, Scored, with Reasoning)             │
└──────────────────────────────────────────────────┘
```

## Component Architecture

### 1. AI Detective (Coordinator)

**Location**: `src/agents/ai_detective.py`

**Responsibilities**:
- Main entry point for recommendation requests
- Coordinates all specialized agents
- Combines multiple analyses into cohesive recommendations
- Calculates overall confidence scores
- Tracks decision time (performance metric)

**Key Methods**:
```python
investigate(user_profile) -> RecommendationResponse
    ├── mood_analyzer.analyze_mood()
    ├── context_analyzer.analyze_context()
    ├── subscription_analyzer.analyze_subscriptions()
    ├── _generate_recommendations()
    └── _calculate_confidence()
```

**Design Pattern**: Facade + Coordinator

### 2. Mood Analyzer

**Location**: `src/agents/mood_analyzer.py`

**Responsibilities**:
- Maps 10 mood states to content preferences
- Determines energy levels
- Identifies preferred and avoided genres
- Calculates mood-based weights

**Data Structure**:
```python
mood_content_mapping = {
    Mood.HAPPY: {
        "energy_level": "high",
        "tone": ["uplifting", "fun"],
        "genres": ["comedy", "adventure"],
        "avoid": ["drama", "horror"]
    },
    # ... 9 more mood mappings
}
```

**Key Features**:
- Mood priority system (some moods like STRESSED get higher weight)
- Dynamic analysis generation
- Energy level correlation

### 3. Context Analyzer

**Location**: `src/agents/context_analyzer.py`

**Responsibilities**:
- Analyzes temporal context (time of day, day of week)
- Evaluates available time constraints
- Considers social setting (alone, with friends, etc.)
- Determines appropriate content types

**Time-Based Preferences**:
```python
time_preferences = {
    "morning": {
        "energy": "building",
        "suitable": ["podcast", "news"],
        "duration_range": (15, 45)
    },
    # ... evening, afternoon, night
}
```

**Key Features**:
- Duration range calculation
- Social context filtering
- Device-awareness
- Urgency factor calculation

### 4. Subscription Analyzer

**Location**: `src/agents/subscription_analyzer.py`

**Responsibilities**:
- Identifies available content sources
- Maps services to content types
- Calculates subscription diversity
- Distributes recommendations across services

**Service Catalog**:
```python
service_catalog = {
    "netflix": {
        "content_types": [MOVIE, TV_SHOW],
        "strengths": ["original series", "movies"],
        "typical_duration": {"movie": 120}
    },
    # ... 9 more services
}
```

**Key Features**:
- Service variety scoring
- Content availability checking
- Fair distribution algorithm

## Data Models

**Location**: `src/models/data_models.py`

All models use Pydantic for validation and serialization:

### Core Models

```python
UserProfile
├── user_id: str
├── current_mood: Mood
├── context: Context
├── subscriptions: List[Subscription]
├── viewing_history: Optional[List[str]]
└── preferences: Optional[Dict]

Context
├── time_of_day: str
├── day_of_week: str
├── available_time: int
├── location: str
├── social_context: str
└── device: str

Subscription
├── service_name: str
├── content_types: List[ContentType]
├── is_active: bool
└── preferences: Optional[Dict]

Recommendation
├── title: str
├── content_type: ContentType
├── service: str
├── duration: int
├── match_score: float (0-100)
├── reasoning: str
├── genre: List[str]
└── mood_alignment: str

RecommendationResponse
├── recommendations: List[Recommendation]
├── decision_time: float
├── analysis: str
├── confidence: float (0-100)
└── timestamp: datetime
```

## Recommendation Algorithm

### Step 1: Data Collection
```python
mood_analysis = mood_analyzer.analyze_mood(mood)
context_analysis = context_analyzer.analyze_context(context)
subscription_analysis = subscription_analyzer.analyze_subscriptions(subscriptions)
```

### Step 2: Content Filtering
```python
for content in database:
    # Filter by availability
    if service not in user_subscriptions: continue
    
    # Filter by duration
    if not (min_duration <= duration <= max_duration): continue
    
    # Filter by appropriateness
    if not is_appropriate(content_type, context): continue
    
    # Calculate match score
    score = calculate_match_score(content, analyses)
    candidates.append((content, score))
```

### Step 3: Scoring Algorithm

```python
def calculate_match_score(content, mood, context, profile):
    score = 50.0  # Base score
    
    # Mood matching (+15 per matching genre, -20 per avoided)
    for genre in content.genres:
        if genre in mood.preferred_genres:
            score += 15
        if genre in mood.avoid_genres:
            score -= 20
    
    # Duration matching (+10 if fits perfectly)
    if min_duration <= content.duration <= max_duration:
        score += 10
    
    # History penalty (-30 if recently watched)
    if content in viewing_history:
        score -= 30
    
    # Energy level matching (+10 if aligned)
    if energy_matches(mood.energy_level, content.duration):
        score += 10
    
    return clamp(score, 0, 100)
```

### Step 4: Ranking and Selection
```python
# Sort by score
candidates.sort(key=lambda x: x[1], reverse=True)

# Take top 5
top_recommendations = candidates[:5]
```

### Step 5: Enrichment
```python
for content, score in top_recommendations:
    recommendation = Recommendation(
        title=content.title,
        match_score=score,
        reasoning=generate_reasoning(content, mood, context),
        mood_alignment=get_mood_alignment(content, mood),
        # ... other fields
    )
```

## Performance Characteristics

### Time Complexity
- **Mood Analysis**: O(1) - Direct dictionary lookup
- **Context Analysis**: O(1) - Rule-based evaluation
- **Subscription Analysis**: O(n) where n = number of subscriptions
- **Content Filtering**: O(m) where m = database size
- **Total**: O(n + m), typically < 1 second

### Space Complexity
- **In-memory database**: O(m) where m = content items
- **User profile**: O(n) where n = subscriptions
- **Recommendations**: O(1) - fixed at 5 items

### Scalability
- **Current**: Handles 20 content items, 10 subscriptions
- **Production**: Can scale to thousands with database backend
- **Concurrent users**: Stateless design allows horizontal scaling

## Design Patterns Used

1. **Facade Pattern**: AI Detective provides simple interface
2. **Strategy Pattern**: Different analyzers for different aspects
3. **Builder Pattern**: User profile construction
4. **Factory Pattern**: Recommendation object creation
5. **Observer Pattern**: Could be extended for notifications

## Extension Points

### Adding New Content Types
```python
# 1. Add to ContentType enum
class ContentType(str, Enum):
    GAME = "game"  # New type

# 2. Update analyzers
# 3. Add to content database
```

### Adding New Moods
```python
# 1. Add to Mood enum
class Mood(str, Enum):
    NOSTALGIC = "nostalgic"  # New mood

# 2. Add mapping in MoodAnalyzer
mood_content_mapping[Mood.NOSTALGIC] = {...}
```

### Adding New Services
```python
# In SubscriptionAnalyzer
service_catalog["new_service"] = {
    "content_types": [...],
    "strengths": [...],
    "typical_duration": {...}
}
```

### Adding ML Integration
```python
# Potential integration point
class MLRecommender:
    def train(self, user_interactions):
        # Train on historical data
        pass
    
    def predict(self, user_profile):
        # Generate ML-based scores
        pass

# In AI Detective
ml_scores = ml_recommender.predict(user_profile)
final_score = (rule_based_score + ml_score) / 2
```

## Security Considerations

1. **No External APIs**: System runs offline, no data leakage
2. **Input Validation**: Pydantic models validate all inputs
3. **No User Data Storage**: Stateless processing
4. **Safe Defaults**: Fallback behaviors for all edge cases

## Error Handling

```python
try:
    response = detective.investigate(user_profile)
except ValidationError:
    # Invalid input - return helpful error
    return error_response("Invalid user profile")
except Exception as e:
    # Unexpected error - log and return safe default
    log_error(e)
    return default_recommendations()
```

## Testing Strategy

1. **Unit Tests**: Each analyzer independently
2. **Integration Tests**: Full flow with AI Detective
3. **Scenario Tests**: Real-world use cases (examples.py)
4. **Performance Tests**: Ensure < 1 second response time

## Future Architecture Enhancements

1. **Database Layer**: Replace in-memory database with PostgreSQL/MongoDB
2. **Caching Layer**: Redis for frequently accessed data
3. **ML Pipeline**: Add TensorFlow/PyTorch for learning
4. **API Layer**: FastAPI REST endpoints
5. **Message Queue**: Kafka for async processing
6. **Monitoring**: Prometheus + Grafana for metrics
7. **A/B Testing**: Framework for recommendation experiments

---

**Built with modularity, extensibility, and performance in mind!** 🏗️
