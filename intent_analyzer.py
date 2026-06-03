"""
Intent Analyzer - Detects what user actually needs from the conversation
Intent types:
- venting: user just wants to express themselves
- validation_seeking: user wants to be heard and validated
- support_seeking: user wants emotional support and companionship
- advice_seeking: user wants practical guidance or solutions
- reassurance_seeking: user wants to be reassured/calmed down
- loneliness: user is seeking connection and to not feel alone
"""

from typing import Dict, List, Tuple, Optional
import re


class IntentAnalyzer:
    """
    Analyzes what the user actually needs in this moment.
    """
    
    def __init__(self):
        # Patterns for each intent type
        self.intent_patterns = {
            'advice_seeking': {
                'keywords': [
                    'gimana', 'cara', 'bagaimana', 'how',
                    'aku harus', 'saya harus', 'i should',
                    'sebaiknya', 'menurut kamu', 'according to you',
                    'saran', 'advice', 'tips', 'solusi',
                    'solution', 'bantu', 'help', 'bisa',
                    'apa yang harus', 'apa yang bisa',
                    'solusi apa', 'cara mengatasinya',
                    'bagaimana cara', 'bagaimana sih',
                    'aku bisa apa', 'bisa gimana',
                    'lihat apa', 'coba apa', 'taro kemana',
                    'gimana kalau', 'bagaimana kalau',
                ],
                'patterns': [
                    r'(gimana|bagaimana).{0,5}(kalau|kalo)',  # "gimana kalau" - what if pattern - ACTUAL ADVICE SEEKING
                    r'(gimana|bagaimana|cara).{0,30}(caranya|nya).{0,20}(aku|saya|gue)',  # "bagaimana caranya aku" - specific advice
                    r'aku.{0,20}(harus|sebaiknya|bisa).{0,20}apa',  # "aku harus apa"
                    r'(saran|advice|tips|solusi).{0,30}(apa|dong|ya)',
                    r'(menurut|menurut kamu|menurut kamu sih)',
                    r'(bisa|boleh).{0,20}(bantu|help|kasih saran)',
                    r'(apa yang|yang mana).{0,20}(harus|bisa).{0,20}(aku|saya)',
                    r'(kalau|kalo).{0,30}(gagal|lulus|bisa|nggak)',  # "kalau gagal/lulus" - conditional
                    r'(langkah|step).{0,20}(apa|gimana|bagaimana)',  # explicit step/solution seeking
                ],
                'intent': 'advice_seeking',
                'priority': 'high'
            },
            
            'venting': {
                'keywords': [
                    'pengen curhat', 'perlu cerita',
                    'sekarang lagi', 'hari ini', 'kemarin',
                    'terus terusan', 'selalu', 'setiap hari',
                    'akhir-akhir ini', 'belakangan', 'recently',
                    'terjadi', 'kejadian', 'case',
                    'cerita', 'story', 'tell you',
                ],
                'patterns': [
                    r'(pengen|mau|ingin).{0,20}(curhat|cerita|bagi)',
                    r'(hari|minggu|bulan).{0,20}ini.{0,30}(lagi|sedang|sekarang)',
                    r'(terus|selalu|setiap).{0,30}(terjadi|begini|gini)',
                    r'(tadi|kemarin|barusan).{0,30}(terjadi|happened|case)',
                    # Only match plain statements, not "gimana/bagaimana" queries or worry expressions
                    r'^(?!.*gimana)(?!.*bagaimana)(?!.*kalau)[^?!]*$(?<!\.)',  
                ],
                'intent': 'venting',
                'priority': 'low'
            },
            
            'validation_seeking': {
                'keywords': [
                    'bener', 'benar', 'right', 'kan',
                    'ya', 'ya kan', 'yes right',
                    'aku benar', 'aku bener', 'i am right',
                    'nggak salah', 'gak salah', 'not wrong',
                    'boleh', 'bisa', 'boleh dong',
                    'wajar', 'normal', 'itu normal',
                    'salah nggak', 'salah gak', 'is it wrong',
                    'nggak apa-apa', 'gak apa-apa', 'it\'s okay',
                ],
                'patterns': [
                    r'(bener|benar|right).{0,20}(kan|nggak|gak|tidak)',
                    r'(boleh|bisa).{0,20}(dong|ya|gak)',
                    r'(wajar|normal).{0,20}(nggak|gak|tidak|kan)',
                    r'(nggak|gak|tidak).{0,20}(salah|apa-apa|papa)',
                    r'(aku|saya).{0,20}(benar|bener|right).{0,20}kan',
                ],
                'intent': 'validation_seeking',
                'priority': 'medium'
            },
            
            'support_seeking': {
                'keywords': [
                    'bisa', 'boleh', 'jangan tinggal',
                    'jangan pergi', 'stay with me',
                    'ditemani', 'temani', 'accompany',
                    'nggak mau sendirian', 'takut sendirian',
                    'ada nggak', 'ada gak', 'is there anyone',
                    'bersama', 'dengan', 'together',
                    'dukung', 'support', 'ada untuk',
                    'peluk', 'hug', 'comfort',
                ],
                'patterns': [
                    r'(boleh|bisa).{0,20}(temani|ditemani|stay)',
                    r'(nggak|gak).{0,20}(mau|pengen).{0,20}(sendirian|aja)',
                    r'(takut|khawatir).{0,20}(sendirian|aja|alone)',
                    r'(ada|ada nggak).{0,20}(untuk|yang care)',
                    r'(dukung|support|peluk|hug).{0,20}(aku|saya|aq)',
                ],
                'intent': 'support_seeking',
                'priority': 'medium'
            },
            
            'reassurance_seeking': {
                'keywords': [
                    'baik-baik', 'okay', 'akan baik',
                    'akan ok', 'akan oke', 'akan baik-baik',
                    'pasti', 'pasti baik', 'surely',
                    'takut', 'khawatir', 'fear', 'anxious',
                    'semoga', 'harap', 'hope',
                    'bisa berhasil', 'pasti bisa',
                    'nggak apa-apa', 'gak apa-apa',
                    'yakinkan', 'convince', 'percaya diri',
                ],
                'patterns': [
                    r'(akan|bakal).{0,20}(baik|ok|okay|baik-baik)',
                    r'(pasti|surely).{0,20}(baik|akan baik|bisa)',
                    r'(takut|khawatir).{0,30}(tapi|benarkah|yakin)',
                    r'(semoga|harap|hope).{0,20}(baik|akan)',
                    r'(bisa|pasti).{0,20}(berhasil|lolos|lulus)',
                ],
                'intent': 'reassurance_seeking',
                'priority': 'high'
            },
            
            'loneliness': {
                'keywords': [
                    'sendirian', 'sepi', 'aja', 'alone',
                    'kesepian', 'loneliness', 'isolated',
                    'tidak ada orang', 'tidak ada siapa',
                    'nggak ada yang', 'gak ada yang',
                    'orang tidak peduli', 'tidak ada yang care',
                    'diabaikan', 'dilupakan', 'forgotten',
                    'merasa sendiri', 'feel alone',
                    'tidak cocok', 'tidak fit in', 'outsider',
                ],
                'patterns': [
                    r'(sendirian|sepi|aja|aja).{0,30}(terus|selalu|banget)',
                    r'(tidak|nggak|gak).{0,20}ada.{0,20}(orang|yang|siapa)',
                    r'(kesepian|loneliness|isolated)',
                    r'(orang|semua).{0,20}(tidak peduli|care|lupa)',
                    r'(merasa|feel).{0,20}(sendiri|sepi|aja)',
                ],
                'intent': 'loneliness',
                'priority': 'high'
            },
        }
    
    def detect(self, user_message: str) -> Tuple[Optional[str], float]:
        """
        Detect primary intent from user message.
        Returns: (intent_name, confidence_score)
        
        Priority: patterns first (more specific), then keywords (broader)
        """
        user_lower = user_message.lower()
        best_intent = None
        best_confidence = 0
        
        for intent_type, intent_config in self.intent_patterns.items():
            confidence = 0
            
            # Check patterns FIRST - they are more specific
            for pattern in intent_config['patterns']:
                if re.search(pattern, user_lower):
                    confidence = 0.75  # Pattern match = high confidence
                    break
            
            # If no pattern match, check keywords
            if confidence == 0:
                keyword_matches = 0
                for keyword in intent_config['keywords']:
                    if keyword in user_lower:
                        keyword_matches += 1
                
                if keyword_matches > 0:
                    confidence = min(keyword_matches * 0.12, 0.5)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent_type
        
        # Default to venting if nothing detected
        if best_intent is None:
            best_intent = 'venting'
            best_confidence = 0.4
        
        return best_intent, best_confidence
    
    def requires_response(self, intent: str) -> bool:
        """
        Check if this intent REQUIRES a substantive response.
        advice_seeking and reassurance_seeking MUST be answered.
        """
        must_answer_intents = ['advice_seeking', 'reassurance_seeking']
        return intent in must_answer_intents
    
    def get_priority(self, intent: str) -> str:
        """Get priority level for this intent"""
        for intent_type, config in self.intent_patterns.items():
            if intent_type == intent:
                return config['priority']
        return 'low'
