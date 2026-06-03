"""
Emotional Memory System
- Remembers emotional patterns across conversation
- Tracks repeated themes and insecurities
- Builds user emotional profile
- Enables contextual response generation
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
from datetime import datetime


class EmotionalMemory:
    """Tracks emotional patterns and context with progressive understanding"""

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
        
        # PROGRESSIVE UNDERSTANDING TRACKING
        self.topic_consistency: Dict[str, int] = defaultdict(int)  # Track main topics
        self.context_coherence_score: float = 1.0  # How coherent conversation is
        self.understanding_depth: int = 0  # 0-5 depth level
        self.linked_contexts: List[Tuple[str, str]] = []  # Contexts that relate to each other
        
        # THIRD MESSAGE RULE TRACKING
        self.message_count: int = 0
        self.has_given_interpretation: bool = False
        self.ready_for_interpretation: bool = False

    def record_message(
        self,
        text: str,
        emotions: List[tuple],
        implied_emotions: List[str],
        details: Dict,
        topic: Optional[str] = None,
        situations: List[str] = None
    ):
        """Record a user message with emotional analysis"""
        
        self.message_count += 1
        
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
        
        # PROGRESSIVE TRACKING: Track topic consistency
        if topic:
            self.topic_consistency[topic] += 1
            self._update_understanding_depth(topic, situations or [])
        
        # PROGRESSIVE TRACKING: Check if contexts are linked
        if situations and self.message_count > 1:
            for situation in situations:
                self._check_context_linking(situation)
        
        # THIRD MESSAGE RULE: Check if ready for interpretation
        if self.message_count >= 3 and not self.has_given_interpretation:
            self.ready_for_interpretation = self._check_interpretation_readiness()
        
        # Store message record
        self.message_history.append({
            'text': text,
            'emotions': emotions,
            'implied': implied_emotions,
            'details': details,
            'topic': topic,
            'situations': situations or [],
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
    
    def _update_understanding_depth(self, topic: str, situations: List[str]):
        """Update understanding depth based on new topic/situations"""
        # Increase depth with more specific information
        if situations:
            self.understanding_depth = min(self.understanding_depth + len(situations), 5)
        else:
            self.understanding_depth = min(self.understanding_depth + 1, 5)
    
    def _check_context_linking(self, situation: str):
        """Check if current situation links to previous contexts"""
        if len(self.message_history) < 2:
            return
        
        # Get previous situations mentioned
        previous_situations = set()
        for msg_record in self.message_history[:-1]:
            previous_situations.update(msg_record.get('situations', []))
        
        # If current situation is related to previous ones, mark as linked
        if situation in previous_situations or any(
            self._is_situation_related(situation, prev_sit)
            for prev_sit in previous_situations
        ):
            if previous_situations:
                self.linked_contexts.append((
                    list(previous_situations)[0],
                    situation
                ))
                self.context_coherence_score = min(self.context_coherence_score + 0.2, 1.0)
    
    def _is_situation_related(self, sit1: str, sit2: str) -> bool:
        """Check if two situations are related"""
        # Simple heuristic: same topic category
        relationship_groups = {
            'romance': ['breakup', 'relationship_distance', 'relationship_conflict', 'partner_cheating'],
            'academics': ['exam_coming', 'bad_grades', 'school_payment', 'school_dropout'],
            'career': ['job_stress', 'job_conflict', 'job_loss', 'interview_fail'],
            'appearance': ['acne_problem', 'teeth_problem', 'weight_concern', 'beauty_insecurity'],
            'family': ['parent_pressure', 'family_conflict', 'parent_unsupported'],
            'friendship': ['friend_abandoned', 'friend_betrayal', 'friend_conflict', 'no_friends'],
            'finance': ['debt_problem', 'insufficient_money'],
            'future': ['uncertain_future', 'future_anxiety'],
        }
        
        for group, situations in relationship_groups.items():
            if sit1 in situations and sit2 in situations:
                return True
        
        return False
    
    def _check_interpretation_readiness(self) -> bool:
        """
        Check if bot is ready to give interpretation (third message rule).
        Requires: 2+ linked contexts OR 1 situation + 1 strong fear
        """
        if len(self.linked_contexts) >= 1:
            return True
        
        # Check if have multiple situations or fear + emotion
        recent_situations = set()
        for msg_record in self.message_history[-3:]:
            recent_situations.update(msg_record.get('situations', []))
        
        has_multiple_situations = len(recent_situations) >= 2
        has_fears = len(self.repeated_themes) >= 2
        has_strong_emotion = any(count >= 2 for count in self.primary_emotions.values())
        
        return (has_multiple_situations) or (has_fears and has_strong_emotion)
    
    def mark_interpretation_given(self):
        """Mark that interpretation has been given"""
        self.has_given_interpretation = True

    def get_main_topic(self) -> Optional[str]:
        """Get the most consistent topic throughout conversation"""
        if not self.topic_consistency:
            return None
        
        return max(self.topic_consistency.items(), key=lambda x: x[1])[0]
    
    def is_topic_consistent(self, new_topic: Optional[str]) -> bool:
        """Check if new topic is consistent with main topic"""
        main_topic = self.get_main_topic()
        
        if not main_topic or not new_topic:
            return True  # Allow if no previous topic
        
        # If same topic, always consistent
        if new_topic == main_topic:
            return True
        
        # Otherwise inconsistent
        return False
    
    def get_understanding_progression(self) -> Dict:
        """Get how understanding has progressed"""
        return {
            'message_count': self.message_count,
            'understanding_depth': self.understanding_depth,  # 0-5
            'context_coherence': self.context_coherence_score,  # 0-1
            'linked_contexts_count': len(self.linked_contexts),
            'is_ready_for_interpretation': self.ready_for_interpretation,
            'has_interpreted': self.has_given_interpretation,
            'main_topic': self.get_main_topic(),
        }

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
