"""
Integrated Chatbot System - NEW ARCHITECTURE
Orchestrates all analysis modules (contextual, intent, fear, emotion, reasoning)
Produces sophisticated, context-aware responses that feel like a real friend
"""

from typing import Dict, List, Optional
from advanced_response_builder import AdvancedResponseBuilder
from emotional_memory import EmotionalMemory
from reasoning_engine import ReasoningEngine


class IntegratedChatbot:
    """
    Main chatbot class that combines all new analysis modules.
    Simpler, cleaner interface than original CurhatBot.
    """
    
    def __init__(self):
        """Initialize all components"""
        self.response_builder = AdvancedResponseBuilder()
        self.emotional_memory = EmotionalMemory()
        self.conversation_history: List[Dict] = []
        
        self.greeting = (
            'Hai! Aku teman curhatmu di sini. '
            'Cerita aja apa yang lagi mengganjal di pikiranmu, santai aja ya.'
        )
        
        self.closing = (
            'Makasih ya udah cerita jujur. '
            'Aku ada di sini kalau kamu mau curhat lagi kapan pun.'
        )
    
    def get_greeting(self) -> str:
        """Get greeting message"""
        return self.greeting
    
    def process_user_message(self, user_message: str) -> str:
        """
        Process user message and generate response.
        Main entry point for conversation.
        """
        
        # 1. VALIDATE MESSAGE
        if not user_message or len(user_message.strip()) < 2:
            return "Hmm, boleh yang sedikit lebih detail? Aku ingin benar-benar dengarkan kamu."
        
        # 2. RECORD MESSAGE IN HISTORY
        self.conversation_history.append({
            'role': 'user',
            'message': user_message
        })
        
        # 3. GENERATE RESPONSE
        response = self.response_builder.generate_response(
            user_message=user_message,
            conversation_history=self.conversation_history,
            emotional_memory=self.emotional_memory
        )
        
        # 4. RECORD RESPONSE IN HISTORY
        self.conversation_history.append({
            'role': 'bot',
            'message': response
        })
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history
    
    def get_emotional_profile(self) -> Dict:
        """Get emotional profile of user based on conversation"""
        return self.emotional_memory.get_emotional_profile()
    
    def get_understanding_progress(self) -> Dict:
        """Get how much bot understands so far"""
        return self.emotional_memory.get_understanding_progression()
    
    def reset_conversation(self):
        """Reset conversation state for new user"""
        self.conversation_history = []
        self.emotional_memory = EmotionalMemory()
    
    def get_message_count(self) -> int:
        """Get number of user messages so far"""
        return len([msg for msg in self.conversation_history if msg['role'] == 'user'])
