"""
Reasoning Engine - Connects all analyzers to create comprehensive understanding
Links: topic + situation + emotion + intent + fear → understanding → response strategy
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from contextual_analyzer import TopicDetector, SituationDetector
from intent_analyzer import IntentAnalyzer
from fear_detector import FearDetector
from emotion_analyzer import MicroEmotionDetector


@dataclass
class AnalysisResult:
    """Container for complete analysis of user message"""
    user_message: str
    topic: Optional[str]
    topic_confidence: float
    situations: List[Tuple[str, float]]  # [(situation, confidence), ...]
    intent: str
    intent_confidence: float
    requires_response: bool
    primary_emotion: str
    emotions: List[Tuple[str, float]]
    primary_fear: Optional[str]
    fears: Dict[str, float]  # {fear_name: confidence}
    conversation_depth: int  # 1-5, based on message count
    is_third_message_or_later: bool
    response_mode: str  # LISTENING, UNDERSTANDING, GUIDANCE, ADVICE
    meaning: Optional[str] = None  # PHASE 2: Deeper psychological meaning extracted
    fear_chain: Optional[List[str]] = None  # PHASE 2: Fear progression for the situation
    story_arc: Optional[Dict] = None  # PHASE 3: Full story from 3+ messages
    story_reasoning: Optional[Dict] = None  # PHASE 3: Story reasoning answers
    # V3 ADDITIONS:
    primary_need: Optional[str] = None  # reassurance, connection, validation, guidance, rest, safety
    intent_type: str = 'unknown'  # validation_seeking, advice_seeking, venting, companionship, guidance_seeking, reassurance_seeking, insight_seeking


class NeedDetector:
    """
    V3: Detect underlying user needs from situation + emotion + fear.
    Maps: situation/fear/emotion → what user really needs
    """
    
    def __init__(self):
        # Fear/Situation → Need mapping
        self.fear_to_need_map = {
            'fear_of_failure': 'reassurance',
            'fear_of_rejection': 'acceptance',
            'fear_of_abandonment': 'security',
            'insecurity': 'acceptance',
            'shame': 'validation',
            'loneliness': 'connection',
            'burnout': 'rest',
            'anxiety': 'reassurance',
            'helplessness': 'guidance',
            'grief': 'support',
            'low_self_esteem': 'affirmation',
        }
        
        # Situation → Need mapping
        self.situation_to_need_map = {
            'exam_coming': 'reassurance',
            'payment_issue': 'guidance',
            'sleep_problem': 'rest',
            'bad_grades': 'reassurance',
            'no_friends': 'connection',
            'breakup': 'support',
            'job_stress': 'rest',
            'health_issue': 'support',
            'family_conflict': 'guidance',
        }
    
    def detect_need(self, analysis: AnalysisResult) -> Optional[str]:
        """
        Detect primary need from fear + situation + emotion
        """
        # Priority 1: Check if primary fear maps to a need
        if analysis.primary_fear and analysis.primary_fear in self.fear_to_need_map:
            return self.fear_to_need_map[analysis.primary_fear]
        
        # Priority 2: Check if situation maps to a need
        if analysis.situations:
            situation_name = analysis.situations[0][0]
            if situation_name in self.situation_to_need_map:
                return self.situation_to_need_map[situation_name]
        
        # Priority 3: Map emotion to need
        emotion_to_need = {
            'anxiety': 'reassurance',
            'sadness': 'support',
            'shame': 'validation',
            'loneliness': 'connection',
            'exhaustion': 'rest',
            'fear': 'reassurance',
        }
        
        if analysis.primary_emotion in emotion_to_need:
            return emotion_to_need[analysis.primary_emotion]
        
        return None


class IntentClassifier:
    """
    V3: Classify intent into specific types for better response tailoring
    """
    
    def __init__(self):
        self.intent_keywords = {
            'validation_seeking': [
                'apakah', 'apa', 'benar tidak', 'gak salah kan', 'punya hak kan', 'wajar kan',
                'boleh', 'pantas', 'nggak berlebihan', 'normal', 'reasonable'
            ],
            'advice_seeking': [
                'gimana', 'bagaimana', 'solusi', 'saran', 'apa yang harus', 'cara', 'tips',
                'langkah', 'harus apa', 'gimana caranya'
            ],
            'venting': [
                'kesel', 'kesal', 'marah', 'jengkel', 'muak', 'benci', 'sebel',
                'argh', 'gah', 'ugh', 'pffft'
            ],
            'companionship': [
                'terima kasih', 'makasih', 'teman', 'menemani', 'disini', 'ada gak',
                'sendiri', 'sepi', 'solitude'
            ],
            'reassurance_seeking': [
                'tidak apa-apa', 'bakal baik-baik', 'bisa', 'mampu', 'kuat', 'sanggup',
                'layak', 'pantas', 'cukup', 'enough', 'okay'
            ],
            'insight_seeking': [
                'kenapa', 'mengapa', 'alasan', 'penyebab', 'karena apa', 'reason why',
                'bagaimana caranya', 'terjadi', 'hubungannya'
            ],
        }
    
    def classify_intent(self, user_message: str) -> str:
        """Classify specific intent type"""
        user_lower = user_message.lower()
        
        # Check each intent type
        for intent_type, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in user_lower:
                    return intent_type
        
        return 'unknown'


class ReasoningEngine:
    """
    Comprehensive reasoning system that connects all analysis modules.
    Produces a complete understanding of user's message and needs.
    """
    
    def __init__(self):
        self.topic_detector = TopicDetector()
        self.situation_detector = SituationDetector()
        self.intent_analyzer = IntentAnalyzer()
        self.fear_detector = FearDetector()
        self.emotion_detector = MicroEmotionDetector()
        # V3: New detectors
        self.need_detector = NeedDetector()
        self.intent_classifier = IntentClassifier()
        
        # Meaning extraction: situation + fear → psychological meaning
        self.meaning_map = {
            ('exam_coming', 'fear_of_failure'): 'takut tidak capable',
            ('exam_coming', 'anxiety'): 'khawatir hasil tidak memuaskan',
            ('payment_issue', 'fear_of_inadequacy'): 'merasa tidak mampu/cukup',
            ('payment_issue', 'shame'): 'malu karena financial burden',
            ('sleep_problem', 'anxiety'): 'otak overthinking nonstop',
            ('bad_grades', 'shame'): 'malu dan self-doubt',
            ('bad_grades', 'fear_of_failure'): 'takut future jadi buruk',
            ('acne_problem', 'shame'): 'insecure tentang appearance',
            ('no_friends', 'loneliness'): 'merasa sendirian dan ditinggal',
            ('breakup', 'fear_of_abandonment'): 'takut ditinggal orang yg berarti',
            ('job_stress', 'emotional_exhaustion'): 'tenaga mental habis',
        }
        
        # Fear chains: situation → likely root fear progression
        self.fear_chains = {
            'exam_coming': ['anxiety', 'fear_of_failure', 'shame', 'fear_of_inadequacy'],
            'sleep_problem': ['anxiety', 'worry', 'fear_of_abandonment'],
            'payment_issue': ['worry', 'fear_of_inadequacy', 'shame'],
            'bad_grades': ['shame', 'fear_of_failure', 'fear_of_inadequacy'],
            'breakup': ['sadness', 'fear_of_abandonment', 'fear_of_inadequacy'],
            'job_stress': ['stress', 'emotional_exhaustion', 'burnout'],
        }
    
    def analyze(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
    ) -> AnalysisResult:
        """
        Comprehensive analysis of user message.
        """
        if conversation_history is None:
            conversation_history = []
        
        # 1. DETECT TOPIC
        topic, topic_confidence = self.topic_detector.detect(user_message)

        # 2. DETECT SITUATION(S)
        situations = self.situation_detector.detect(user_message)

        previous_topic, previous_confidence = self._get_previous_topic(conversation_history)
        topic, topic_confidence = self._resolve_active_topic(
            current_topic=topic,
            current_confidence=topic_confidence,
            situations=situations,
            previous_topic=previous_topic,
            previous_confidence=previous_confidence,
        )

        # 2.5 FALLBACK: If no situations in current message, use previous only when topic is continuous.
        if not situations and conversation_history and previous_topic and topic == previous_topic:
            for i in range(len(conversation_history) - 1, -1, -1):
                prev_msg = conversation_history[i]
                if prev_msg.get('role') == 'user':
                    prev_situations = self.situation_detector.detect(prev_msg.get('message', ''))
                    if prev_situations:
                        situations = prev_situations
                        break
        
        # 3. DETECT INTENT
        intent, intent_confidence = self.intent_analyzer.detect(user_message)
        requires_response = self.intent_analyzer.requires_response(intent)
        
        # 4. DETECT EMOTIONS
        emotions = self.emotion_detector.get_dominant_emotions(user_message)
        primary_emotion = emotions[0][0] if emotions else 'uncertainty'
        
        # 5. DETECT FEARS
        fears = self.fear_detector.get_underlying_fears(user_message)
        primary_fear = self.fear_detector.get_primary_fear(user_message)
        primary_fear_name = primary_fear[0] if primary_fear else None
        
        # 6. DETERMINE CONVERSATION DEPTH
        conversation_depth = len(conversation_history) + 1  # Current message is new
        is_third_message_or_later = conversation_depth >= 3
        
        # 7. SELECT RESPONSE MODE
        response_mode = self._select_response_mode(
            intent=intent,
            conversation_depth=conversation_depth,
            situations=situations,
            primary_fear=primary_fear_name,
        )
        
        # Create analysis result
        analysis = AnalysisResult(
            user_message=user_message,
            topic=topic,
            topic_confidence=topic_confidence,
            situations=situations,
            intent=intent,
            intent_confidence=intent_confidence,
            requires_response=requires_response,
            primary_emotion=primary_emotion,
            emotions=emotions,
            primary_fear=primary_fear_name,
            fears=fears,
            conversation_depth=conversation_depth,
            is_third_message_or_later=is_third_message_or_later,
            response_mode=response_mode,
        )
        
        # V3: Detect need and intent type
        analysis.primary_need = self.need_detector.detect_need(analysis)
        analysis.intent_type = self.intent_classifier.classify_intent(user_message)
        
        # PHASE 2: Extract meaning and fear chain
        analysis.meaning = self.extract_meaning(analysis)
        analysis.fear_chain = self.build_fear_chain(analysis)
        
        return analysis

    def _get_previous_topic(self, conversation_history: List[Dict]) -> Tuple[Optional[str], float]:
        if not conversation_history:
            return None, 0.0

        for i in range(len(conversation_history) - 1, -1, -1):
            prev_msg = conversation_history[i]
            if prev_msg.get('role') != 'user':
                continue
            prev_topic, prev_confidence = self.topic_detector.detect(prev_msg.get('message', ''))
            if prev_topic and prev_confidence >= 0.25:
                return prev_topic, prev_confidence

        return None, 0.0

    def _resolve_active_topic(
        self,
        current_topic: Optional[str],
        current_confidence: float,
        situations: List[Tuple[str, float]],
        previous_topic: Optional[str],
        previous_confidence: float,
    ) -> Tuple[Optional[str], float]:
        situation_topic, situation_confidence = self._topic_from_situations(situations)

        if situation_topic and situation_confidence >= 0.75:
            if not current_topic or current_confidence < situation_confidence:
                current_topic = situation_topic
                current_confidence = situation_confidence

        if not previous_topic:
            return current_topic, current_confidence

        if not current_topic or current_confidence < 0.3:
            return previous_topic, max(previous_confidence * 0.85, 0.3)

        if current_topic == previous_topic:
            return current_topic, min(current_confidence + 0.12, 1.0)

        if current_confidence >= previous_confidence + 0.12 or current_confidence >= 0.65:
            return current_topic, current_confidence

        return previous_topic, max(previous_confidence * 0.85, current_confidence)

    def _topic_from_situations(self, situations: List[Tuple[str, float]]) -> Tuple[Optional[str], float]:
        situation_topic_map = {
            'breakup': 'relationship',
            'relationship_distance': 'relationship',
            'relationship_conflict': 'relationship',
            'partner_cheating': 'relationship',
            'exam_coming': 'education',
            'bad_grades': 'education',
            'school_payment': 'education',
            'school_dropout': 'education',
            'job_stress': 'career',
            'job_conflict': 'career',
            'job_loss': 'career',
            'interview_fail': 'career',
            'acne_problem': 'appearance',
            'teeth_problem': 'appearance',
            'weight_concern': 'appearance',
            'beauty_insecurity': 'appearance',
            'parent_pressure': 'family',
            'family_conflict': 'family',
            'parent_unsupported': 'family',
            'friend_abandoned': 'friendship',
            'friend_betrayal': 'friendship',
            'friend_conflict': 'friendship',
            'friendship_exclusion': 'friendship',
            'no_friends': 'friendship',
            'debt_problem': 'finance',
            'insufficient_money': 'finance',
            'uncertain_future': 'future',
            'future_anxiety': 'future',
            'sleep_problem': 'health',
            'stress_health': 'health',
        }

        scores = {}
        for situation, confidence in situations:
            topic = situation_topic_map.get(situation)
            if topic:
                scores[topic] = max(scores.get(topic, 0.0), confidence)

        if not scores:
            return None, 0.0

        topic, confidence = max(scores.items(), key=lambda item: item[1])
        return topic, confidence
    
    def _select_response_mode(
        self,
        intent: str,
        conversation_depth: int,
        situations: List[Tuple[str, float]],
        primary_fear: Optional[str],
    ) -> str:
        """
        Select response mode based on context.
        
        LISTENING: User just venting, early stage, need to hear and reflect
        UNDERSTANDING: Getting deeper, showing we understand the situation
        GUIDANCE: Offering perspective and light guidance
        ADVICE: Direct advice/practical steps (only for advice_seeking intent)
        """
        
        # If user explicitly asking for advice, go straight to ADVICE mode
        if intent == 'advice_seeking':
            return 'ADVICE'
        
        # If user seeking reassurance, go to GUIDANCE mode
        if intent == 'reassurance_seeking':
            return 'GUIDANCE'
        
        # If early conversation (message 1-2), start with LISTENING
        if conversation_depth <= 2:
            return 'LISTENING'
        
        # If 3+ messages and has clear situations, move to UNDERSTANDING
        if conversation_depth >= 3 and situations:
            return 'UNDERSTANDING'
        
        # If 4+ messages with fear detected, move to GUIDANCE
        if conversation_depth >= 4 and primary_fear:
            return 'GUIDANCE'
        
        # Default to UNDERSTANDING for depth > 2
        if conversation_depth > 2:
            return 'UNDERSTANDING'
        
        return 'LISTENING'
    
    def should_give_interpretation(self, analysis: AnalysisResult) -> bool:
        """
        Determine if bot should give interpretation/diagnosis.
        Third message rule: if 2+ clear contexts linked, give interpretation.
        """
        if not analysis.is_third_message_or_later:
            return False
        
        # Need at least 2 situations or 1 situation + 1 fear
        situation_count = len(analysis.situations)
        fear_count = len(analysis.fears)
        
        return (situation_count >= 2) or (situation_count >= 1 and fear_count >= 1)
    
    def should_give_advice(self, analysis: AnalysisResult) -> bool:
        """
        Determine if bot should give practical advice.
        Advice mode OR third message rule with clear guidance need.
        """
        if analysis.response_mode == 'ADVICE':
            return True
        
        # Third message rule: if analysis shows clear path, give light advice
        if analysis.is_third_message_or_later:
            return len(analysis.situations) >= 1 and len(analysis.fears) >= 1
        
        return False
    
    def should_give_support(self, analysis: AnalysisResult) -> bool:
        """
        Determine if bot should explicitly offer support/companionship.
        """
        support_indicators = [
            'loneliness',
            'support_seeking',
            'fear_of_abandonment',
        ]
        
        has_support_intent = analysis.intent in ['support_seeking', 'loneliness']
        has_support_fear = analysis.primary_fear in support_indicators
        
        return has_support_intent or has_support_fear
    
    def get_context_focus(self, analysis: AnalysisResult) -> List[str]:
        """
        Get what should be focused on in response.
        Returns list of focus areas for response builder.
        """
        focus = []
        
        # Topic focus
        if analysis.topic:
            focus.append(f'topic:{analysis.topic}')
        
        # Situation focus - use top 2 situations
        for i, (situation, _) in enumerate(analysis.situations[:2]):
            focus.append(f'situation:{situation}')
        
        # Fear focus - use primary fear
        if analysis.primary_fear:
            focus.append(f'fear:{analysis.primary_fear}')
        
        # Emotion focus - use primary emotion
        if analysis.primary_emotion:
            focus.append(f'emotion:{analysis.primary_emotion}')
        
        # Intent focus
        if analysis.intent:
            focus.append(f'intent:{analysis.intent}')
        
        return focus
    
    def get_response_instructions(self, analysis: AnalysisResult) -> Dict[str, Any]:
        """
        Generate detailed instructions for response builder.
        """
        return {
            'mode': analysis.response_mode,
            'should_interpret': self.should_give_interpretation(analysis),
            'should_advise': self.should_give_advice(analysis),
            'should_support': self.should_give_support(analysis),
            'conversation_depth': analysis.conversation_depth,
            'focus_areas': self.get_context_focus(analysis),
            'primary_topic': analysis.topic,
            'primary_fear': analysis.primary_fear,
            'primary_emotion': analysis.primary_emotion,
            'intent': analysis.intent,
            'situations': analysis.situations,
            'is_advice_required': analysis.intent == 'advice_seeking',
            'tone': self._get_tone(analysis),
        }
    
    def _get_tone(self, analysis: AnalysisResult) -> str:
        """
        Determine appropriate tone for response.
        """
        if analysis.response_mode == 'ADVICE':
            return 'practical'
        elif analysis.response_mode == 'GUIDANCE':
            return 'supportive'
        elif analysis.response_mode == 'UNDERSTANDING':
            return 'empathetic'
        else:  # LISTENING
            return 'reflective'
    
    def validate_analysis(self, analysis: AnalysisResult) -> bool:
        """
        Validate that analysis is reasonable.
        """
        # Must have at least topic or intent or emotion
        has_content = (
            analysis.topic is not None or
            analysis.intent is not None or
            analysis.primary_emotion is not None
        )
        
        return has_content and len(analysis.user_message.strip()) > 5
    
    # ========== PHASE 3: STORY REASONING RULE ==========
    
    def build_story_arc(self, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Reconstruct story from last 3+ messages.
        Returns: main_problem, root_cause, primary_fear, story_progression
        
        Note: If the last item in history is a user message, it's treated as the "current" message
        and is excluded from story analysis. This ensures the story is about PREVIOUS messages,
        not including the current one being analyzed.
        """
        if not conversation_history or len(conversation_history) < 2:
            return {
                'has_story': False,
                'main_problem': None,
                'root_cause': None,
                'primary_fear': None,
                'progression': [],
            }
        
        # Extract user messages - excluding the last one if it's a user message (current message)
        all_user_messages = [msg for msg in conversation_history if msg.get('role') == 'user']
        
        # If the last message in history is a user message, exclude it (it's the current message)
        # to build story from PREVIOUS messages only
        if (conversation_history and conversation_history[-1].get('role') == 'user' 
            and len(all_user_messages) > 1):
            user_messages = all_user_messages[:-1][-3:]  # Get last 3 excluding current
        else:
            user_messages = all_user_messages[-3:]  # Get last 3 normally
        
        if len(user_messages) < 2:
            return {
                'has_story': False,
                'main_problem': None,
                'root_cause': None,
                'primary_fear': None,
                'progression': [],
            }
        
        # Extract situations and fears from each message
        progression = []
        all_situations = []
        all_fears = []
        
        for msg in user_messages:
            text = msg.get('message', '') or msg.get('text', '')
            # Quick analysis of each message
            situations = self.situation_detector.detect(text)
            fears = self.fear_detector.get_underlying_fears(text)
            emotion = self.emotion_detector.get_dominant_emotions(text)
            
            progression.append({
                'message': text,
                'situations': situations,
                'fears': fears,
                'emotion': emotion[0][0] if emotion else None,
            })
            
            all_situations.extend([s[0] for s in situations])
            all_fears.extend(list(fears.keys()))
        # Identify main problem
        # Strategy: Prefer NEW situations (ones that haven't appeared before)
        # This helps show the conversation is PROGRESSING to new issues
        if all_situations:
            # Track situations by order of first appearance
            first_appearance_order = {}
            for i, sit in enumerate(all_situations):
                if sit not in first_appearance_order:
                    first_appearance_order[sit] = i
            
            # Count occurrences
            situation_counts = {}
            for sit in all_situations:
                situation_counts[sit] = situation_counts.get(sit, 0) + 1
            
            # Strategy:
            # 1. If a new situation appears in the last message - use that as main
            # 2. Otherwise use most frequent situation
            last_msg_situations = [s[0] for s in progression[-1]['situations']] if progression else []
            new_situations = [sit for sit in last_msg_situations if first_appearance_order.get(sit, -1) > len(all_situations) // 2]
            
            if new_situations:
                main_problem = new_situations[0]
            else:
                # Fallback: use most frequent OR most recent
                repeated_situations = [sit for sit, count in situation_counts.items() if count > 1]
                if repeated_situations:
                    main_problem = repeated_situations[0]
                else:
                    main_problem = last_msg_situations[0] if last_msg_situations else all_situations[-1]
        else:
            main_problem = None
        
        # Identify root cause (first mentioned situation usually)
        root_cause = all_situations[0] if all_situations else None
        
        # Identify primary fear (most intense fear)
        primary_fear = max(all_fears, key=lambda x: all_fears.count(x)) if all_fears else None
        
        # Ensure all values are strings for safe processing
        main_problem = str(main_problem) if main_problem else None
        root_cause = str(root_cause) if root_cause else None
        primary_fear = str(primary_fear) if primary_fear else None
        
        return {
            'has_story': True,
            'main_problem': main_problem,
            'root_cause': root_cause,
            'primary_fear': primary_fear,
            'progression': progression,
            'all_situations': all_situations,
            'all_fears': all_fears,
        }
    
    def extract_story_reasoning(self, story_arc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Answer the 4 core story reasoning questions:
        1. Apa masalah utama user?
        2. Apa penyebab masalah itu?
        3. Apa ketakutan terbesar user?
        4. Apa hubungan antara pesan sebelumnya dan pesan sekarang?
        """
        if not story_arc.get('has_story'):
            return {}
        
        progression = story_arc.get('progression', [])
        
        # Question 1: Main problem
        main_problem = story_arc.get('main_problem') or ''
        problem_description = main_problem.replace('_', ' ') if main_problem else 'masalah'
        
        # Question 2: Root cause
        root_cause = story_arc.get('root_cause') or ''
        cause_description = root_cause.replace('_', ' ') if root_cause else 'ada sesuatu'
        
        # Question 3: Biggest fear
        primary_fear = story_arc.get('primary_fear') or ''
        fear_description = primary_fear.replace('_', ' ') if primary_fear else 'belum jelas'
        
        # Question 4: Message progression/relationship
        progression_story = ""
        if len(progression) >= 2:
            first_emotion = progression[0].get('emotion')
            last_emotion = progression[-1].get('emotion')
            
            if first_emotion and last_emotion:
                if first_emotion != last_emotion:
                    progression_story = f"dari {first_emotion} berkembang menjadi {last_emotion}"
                else:
                    progression_story = f"konsisten merasa {first_emotion} di semua cerita"
        
        return {
            'main_problem': f"masalah utama: {problem_description}",
            'root_cause': f"penyebabnya: {cause_description}",
            'primary_fear': f"ketakutan terbesar: {fear_description}",
            'progression': progression_story,
            'full_narrative': f"Dari cerita kamu, saya lihat: {cause_description} → membuat kamu {progression_story}" if progression_story else f"Dari cerita kamu, saya lihat ada {problem_description}",
        }
    
    # ========== PHASE 2: MEANING EXTRACTION & CONTEXT LINKING ==========
    
    def extract_meaning(self, analysis: AnalysisResult) -> str:
        """
        Extract deeper psychological meaning from situation + fear combination.
        Returns the REAL issue behind the surface complaint.
        """
        if not analysis.situations or not analysis.primary_fear:
            return ""
        
        situation = analysis.situations[0][0]
        fear = analysis.primary_fear
        
        # Try to find exact meaning mapping
        meaning = self.meaning_map.get((situation, fear), "")
        if meaning:
            return meaning
        
        # Try partial matches
        for (sit_key, fear_key), mapped_meaning in self.meaning_map.items():
            if sit_key == situation or fear_key == fear:
                return mapped_meaning
        
        # Generic meaning extraction
        if 'fear' in fear:
            return f"ada ketakutan mendalam: {fear.replace('_', ' ')}"
        
        return ""
    
    def build_fear_chain(self, analysis: AnalysisResult) -> List[str]:
        """
        Build fear chain progression for situation.
        Shows the likely sequence of fears that develop.
        Example: exam_coming → anxiety → fear_of_failure → shame
        """
        if not analysis.situations:
            return []
        
        situation = analysis.situations[0][0]
        chain = self.fear_chains.get(situation, [])
        
        # Return chain if it exists
        if chain:
            return chain
        
        # Generic chain: emotion → fear → shame
        chain = []
        if analysis.primary_emotion:
            chain.append(analysis.primary_emotion)
        if analysis.primary_fear:
            chain.append(analysis.primary_fear)
        if analysis.primary_emotion in ['anxiety', 'worry', 'stress']:
            chain.append('shame')
        
        return chain
    
    def link_conversation_context(
        self,
        current_analysis: AnalysisResult,
        conversation_history: List[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Link current message to previous messages for context consistency.
        Shows how current situation relates to earlier messages.
        """
        if not conversation_history or len(conversation_history) < 2:
            return {}
        
        # Extract previous situations
        previous_situations = []
        previous_fears = []
        
        for msg in conversation_history[-3:]:  # Look at last 3 messages
            if 'analysis' in msg:
                prev_analysis = msg['analysis']
                if hasattr(prev_analysis, 'situations'):
                    previous_situations.extend([s[0] for s in prev_analysis.situations])
                if hasattr(prev_analysis, 'primary_fear'):
                    previous_fears.append(prev_analysis.primary_fear)
        
        # Find connections
        current_situations = [s[0] for s in current_analysis.situations]
        connections = {
            'repeating_situation': any(s in previous_situations for s in current_situations),
            'deepening_fear': current_analysis.primary_fear in previous_fears,
            'theme_consistency': self._check_theme_consistency(
                current_situations + current_situations,
                previous_situations
            ),
        }
        
        return {
            'previous_situations': previous_situations,
            'previous_fears': previous_fears,
            'connections': connections,
            'is_progression': connections['repeating_situation'] or connections['deepening_fear'],
        }
    
    def _check_theme_consistency(
        self,
        current_items: List[str],
        previous_items: List[str],
    ) -> bool:
        """Check if current and previous items share common theme"""
        if not current_items or not previous_items:
            return False
        
        # Simple overlap check
        return len(set(current_items) & set(previous_items)) > 0
    
    def select_response_mode_advanced(
        self,
        intent: str,
        conversation_depth: int,
        situations: List[Tuple[str, float]],
        primary_fear: Optional[str],
        context_links: Dict[str, Any] = None,
    ) -> str:
        """
        Advanced response mode selection using context linking.
        More nuanced than basic _select_response_mode.
        """
        if context_links is None:
            context_links = {}
        
        # If user explicitly asking for advice, ALWAYS go to ADVICE
        if intent == 'advice_seeking':
            return 'ADVICE'
        
        # If user seeking reassurance AND it's a repeat concern, GUIDANCE
        if intent == 'reassurance_seeking':
            if context_links.get('repeating_situation'):
                return 'GUIDANCE'  # We understand the pattern now
            return 'LISTENING'  # First time, just listen
        
        # If early conversation (1-2), LISTENING
        if conversation_depth <= 2:
            return 'LISTENING'
        
        # If progression detected (deepening fear), move to GUIDANCE
        if context_links.get('is_progression'):
            return 'GUIDANCE'
        
        # If 3+ messages with clear fears, UNDERSTANDING
        if conversation_depth >= 3 and primary_fear and situations:
            return 'UNDERSTANDING'
        
        # Default behavior
        return self._select_response_mode(intent, conversation_depth, situations, primary_fear)
