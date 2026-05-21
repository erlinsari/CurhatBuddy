"""
Emotional Memory System
- Remembers emotional patterns across conversation
- Tracks repeated themes and insecurities
- Builds user emotional profile
- Enables contextual response generation
"""

from typing import Dict, List, Set, Optional
from collections import defaultdict
from datetime import datetime


class EmotionalMemory:
    """Tracks emotional patterns and context"""

    def __init__(self):
        # Core emotional state tracking
        self.primary_emotions: Dict[str, int] = defaultdict(int)  # count
        self.implied_emotions: Dict[str, int] = defaultdict(int)  # count
        
        # Relational context
        self.mentioned_people: Set[str] = set()
        self.relationship_context: Dict[str, str] = {}
        
        # Patterns discovered
        self.repeated_themes: Set[str] = set()
        self.emotional_triggers: List[Dict] = []
        
        # User attachment profile
        self.attachment_indicators = {
            'anxious_attachment': 0,
            'avoidant_attachment': 0,
            'secure_attachment': 0,
        }
        
        # Story arc tracking
        self.story_progression: List[Dict] = []
        self.conversation_stage = 1  # 1-4
        self.emotional_arc = []  # track emotional journey
        
        # Conversation history for context
        self.message_history: List[Dict] = []

    def record_message(
        self,
        text: str,
        emotions: List[tuple],
        implied_emotions: List[str],
        details: Dict
    ):
        """Record a user message with emotional analysis"""
        
        # Track primary emotions
        for emotion_name, confidence in emotions:
            self.primary_emotions[emotion_name] += 1
        
        # Track implied emotions
        for emotion in implied_emotions:
            self.implied_emotions[emotion] += 1
        
        # Track mentioned people
        people_keywords = [
            'pacar', 'partner', 'dia', 'bf', 'gf', 
            'orang tua', 'ibunya', 'ayahnya', 'teman'
        ]
        for keyword in people_keywords:
            if keyword in text.lower():
                self.mentioned_people.add(keyword)
        
        # Track themes
        theme_keywords = [
            'fear_of_abandonment', 'insecurity', 'overthinking',
            'emotional_exhaustion', 'loneliness'
        ]
        for emotion in emotions:
            if emotion[0] in theme_keywords:
                self.repeated_themes.add(emotion[0])
        
        # Record attachment indicators
        if any(e[0] in ['fear_of_abandonment', 'emotional_dependency', 'anxious_attachment'] 
               for e in emotions):
            self.attachment_indicators['anxious_attachment'] += 1
        
        # Store message record
        self.message_history.append({
            'text': text,
            'emotions': emotions,
            'implied': implied_emotions,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update emotional arc
        self._update_emotional_arc(emotions)

    def _update_emotional_arc(self, emotions: List[tuple]):
        """Track how emotions progress through conversation"""
        if emotions:
            dominant_emotion = emotions[0][0] if emotions else None
            self.emotional_arc.append({
                'stage': self.conversation_stage,
                'emotion': dominant_emotion,
                'intensity': emotions[0][1] if emotions else 0
            })

    def get_dominant_emotions(self, top_n: int = 3) -> List[tuple]:
        """Get most frequent emotions detected"""
        sorted_emotions = sorted(
            self.primary_emotions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_emotions[:top_n]

    def get_repeated_themes(self) -> List[str]:
        """Themes that appear multiple times"""
        return list(self.repeated_themes)

    def get_emotional_profile(self) -> Dict:
        """Generate emotional profile of user"""
        return {
            'primary_emotions': dict(sorted(
                self.primary_emotions.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]),
            'implied_emotions': dict(sorted(
                self.implied_emotions.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]),
            'repeated_themes': list(self.repeated_themes),
            'mentioned_people': list(self.mentioned_people),
            'attachment_style': self._infer_attachment_style(),
            'conversation_stage': self.conversation_stage,
            'message_count': len(self.message_history),
        }

    def _infer_attachment_style(self) -> str:
        """Infer user's likely attachment style"""
        max_indicator = max(
            self.attachment_indicators.items(),
            key=lambda x: x[1]
        )
        return max_indicator[0]

    def should_advance_stage(self) -> bool:
        """Determine if conversation should move to next stage"""
        message_count = len(self.message_history)
        
        # Advance based on message count and emotional clarity
        if self.conversation_stage == 1 and message_count >= 2:
            return True
        elif self.conversation_stage == 2 and message_count >= 4:
            return True
        elif self.conversation_stage == 3 and message_count >= 6:
            return True
        
        return False

    def advance_stage(self):
        """Move conversation to next stage"""
        if self.conversation_stage < 4:
            self.conversation_stage += 1

    def get_context_for_response(self) -> Dict:
        """Get all context needed for response generation"""
        return {
            'stage': self.conversation_stage,
            'dominant_emotions': self.get_dominant_emotions(),
            'repeated_themes': self.get_repeated_themes(),
            'mentioned_people': list(self.mentioned_people),
            'attachment_style': self._infer_attachment_style(),
            'emotional_profile': self.get_emotional_profile(),
            'recent_messages': self.message_history[-3:] if self.message_history else [],
        }

    def has_theme(self, theme_name: str) -> bool:
        """Check if specific emotional theme was detected"""
        return theme_name in self.repeated_themes

    def count_emotion(self, emotion_name: str) -> int:
        """Count how many times specific emotion was detected"""
        return self.primary_emotions.get(emotion_name, 0)


class ConversationStageManager:
    """Manage conversation progression through stages"""

    STAGES = {
        1: {
            'name': 'Listening Phase',
            'description': 'Focus on listening and acknowledging',
            'response_type': 'reflective',
            'question_depth': 'surface',
            'insight_depth': 'none',
            'support_level': 'minimal',
        },
        2: {
            'name': 'Understanding Phase',
            'description': 'Deepen understanding of the story',
            'response_type': 'reflective + question',
            'question_depth': 'medium',
            'insight_depth': 'light',
            'support_level': 'gentle',
        },
        3: {
            'name': 'Insight Phase',
            'description': 'Share emotional insights',
            'response_type': 'insight + reflection',
            'question_depth': 'deep',
            'insight_depth': 'moderate',
            'support_level': 'active',
        },
        4: {
            'name': 'Support Phase',
            'description': 'Provide support and gentle guidance',
            'response_type': 'support + insight',
            'question_depth': 'deep',
            'insight_depth': 'deep',
            'support_level': 'strong',
        },
    }

    def __init__(self):
        self.current_stage = 1

    def get_stage_info(self, stage: Optional[int] = None) -> Dict:
        """Get info about current or specified stage"""
        stage = stage or self.current_stage
        return self.STAGES.get(stage, self.STAGES[1])

    def should_listen_more(self) -> bool:
        """Should bot focus on listening?"""
        return self.current_stage <= 2

    def should_give_insight(self) -> bool:
        """Should bot provide insights?"""
        return self.current_stage >= 3

    def should_provide_support(self) -> bool:
        """Should bot provide active support?"""
        return self.current_stage >= 3

    def get_response_strategy(self) -> Dict:
        """Get response building strategy for current stage"""
        stage_info = self.get_stage_info()
        
        return {
            'include_reflection': True,
            'include_question': self.current_stage >= 2,
            'include_insight': self.current_stage >= 3,
            'include_support': self.current_stage >= 3,
            'depth': stage_info['question_depth'],
            'tone': self._get_tone_for_stage(),
        }

    def _get_tone_for_stage(self) -> str:
        """Get appropriate response tone"""
        if self.current_stage == 1:
            return 'warm_listening'
        elif self.current_stage == 2:
            return 'warm_understanding'
        elif self.current_stage == 3:
            return 'warm_insightful'
        else:
            return 'warm_supportive'

    def advance(self):
        """Move to next stage"""
        if self.current_stage < 4:
            self.current_stage += 1

    def reset(self):
        """Reset to first stage"""
        self.current_stage = 1


class ContextWindow:
    """Manage recent context for response generation"""

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.messages: List[Dict] = []

    def add_message(self, role: str, text: str, emotions: List[tuple] = None):
        """Add message to context window"""
        self.messages.append({
            'role': role,
            'text': text,
            'emotions': emotions or []
        })
        
        # Keep only recent messages
        if len(self.messages) > self.window_size:
            self.messages.pop(0)

    def get_recent_context(self) -> str:
        """Get recent conversation as context string"""
        context_lines = []
        
        for msg in self.messages[-3:]:  # Last 3 messages
            role = msg['role'].upper()
            context_lines.append(f"{role}: {msg['text'][:100]}...")
        
        return "\n".join(context_lines)

    def get_last_user_message(self) -> Optional[Dict]:
        """Get the last user message"""
        for msg in reversed(self.messages):
            if msg['role'] == 'user':
                return msg
        return None

    def get_message_pattern(self) -> Dict:
        """Detect pattern in recent messages"""
        if len(self.messages) < 2:
            return {'pattern': 'too_short'}
        
        # Check if user is elaborating (explaining more detail)
        if len(self.messages) >= 2:
            last_user = None
            prev_user = None
            
            user_messages = [m for m in self.messages if m['role'] == 'user']
            if len(user_messages) >= 2:
                last_user = len(user_messages[-1]['text'])
                prev_user = len(user_messages[-2]['text'])
                
                if last_user > prev_user * 1.3:
                    return {'pattern': 'elaborating'}
        
        return {'pattern': 'normal'}

    def clear(self):
        """Clear context window"""
        self.messages = []
