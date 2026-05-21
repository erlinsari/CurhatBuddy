"""
Advanced Emotion Analyzer
- Detects micro emotions (not just broad categories)
- Detects implied emotions (hidden fears, insecurities)
- Extracts emotional patterns
- Maps emotional complexity
"""

from typing import Dict, List, Set, Tuple, Optional
import re


class MicroEmotionDetector:
    """Detect fine-grained emotional nuances"""

    def __init__(self):
        # Micro emotions mapping
        self.micro_emotions = {
            # ABANDONMENT & REJECTION
            'fear_of_abandonment': {
                'keywords': [
                    'takut ditinggal',
                    'takut kehilangan',
                    'lama bales',
                    'pergi',
                    'ninggalin',
                    'tergantung',
                    'takut sendirian',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,15}(ditinggal|pergi|hilang)',
                    r'(lama|jarang).{0,15}(bales|hubungi|chat)',
                    r'kalau.*pergi.*aku.*jadi',
                ],
                'severity': 'high'
            },

            'fear_of_rejection': {
                'keywords': [
                    'takut ditolak',
                    'takut nggak diterima',
                    'takut ganggu',
                    'takut bawel',
                    'takut dibenci',
                    'nggak pantas',
                    'nggak layak',
                ],
                'patterns': [
                    r'takut.{0,15}(tolak|benci|marah|kesal)',
                    r'(jangan|takut).{0,15}ganggu',
                    r'aku.{0,15}(tidak|nggak).{0,15}layak',
                ],
                'severity': 'high'
            },

            'insecurity': {
                'keywords': [
                    'nggak cukup',
                    'nggak layak',
                    'kurang',
                    'nggak bagus',
                    'nggak percaya diri',
                    'ragu',
                    'minder',
                    'kalah',
                    'insecure',
                    'nggak pede',
                    'beda sama',
                    'beda dengan',
                    'gendut',
                    'jelek',
                    'kurang cantik',
                    'kurang ganteng',
                    'compare diri',
                    'dibandingin',
                    'takut dinilai',
                    'takut dibandingin',
                    'takut nggak diterima',
                    'body image',
                    'penampilan',
                    'nggak pantas',
                ],
                'patterns': [
                    r'(nggak|tidak).{0,15}(cukup|layak|bagus|pede)',
                    r'(aku|dia).{0,15}lebih.*dari',
                    r'(beda|berbeda).{0,15}(sama|dengan)',
                    r'(gendut|jelek|jelek|payah)',
                    r'(compare|bandingin|dibanding)',
                    r'(takut|khawatir).{0,15}(dinilai|dibandingin|nggak diterima)',
                    r'(insecure|nggak pede|nggak percaya diri)',
                ],
                'severity': 'medium'
            },

            # CHANGE & LOSS
            'fear_of_change': {
                'keywords': [
                    'berubah',
                    'tidak sama',
                    'dulu vs sekarang',
                    'berubah jadi',
                    'udah nggak kayak dulu',
                ],
                'patterns': [
                    r'(dulu|sebelumnya).{0,20}(sekarang|sekarang)',
                    r'berubah.*menjadi',
                    r'tidak.*lagi.*seperti',
                ],
                'severity': 'medium'
            },

            'grief_loss': {
                'keywords': [
                    'hilang',
                    'pergi',
                    'meninggal',
                    'putus',
                    'lepas',
                    'habis',
                    'gone',
                ],
                'patterns': [
                    r'(sudah|udah).{0,15}(hilang|pergi|meninggal)',
                    r'kehilangan',
                ],
                'severity': 'high'
            },

            # EMOTIONAL EXHAUSTION
            'emotional_exhaustion': {
                'keywords': [
                    'capek',
                    'lelah',
                    'nguras',
                    'habis tenaga',
                    'kelelahan',
                    'penat',
                    'jenuh',
                ],
                'patterns': [
                    r'(terlalu|sudah|terus).{0,15}capek',
                    r'capek.{0,15}(terus|menerus)',
                    r'energy.*habis',
                ],
                'severity': 'high'
            },

            'emotional_suppression': {
                'keywords': [
                    'pura-pura kuat',
                    'tahan diri',
                    'nggak boleh nangis',
                    'memendam',
                    'menyembunyikan',
                    'pura pura',
                    'ditahan',
                ],
                'patterns': [
                    r'(pura|tahan).{0,15}(kuat|diri)',
                    r'nggak boleh.*nangis',
                    r'(memendam|menyimpan).*sendiri',
                ],
                'severity': 'high'
            },

            # ANXIETY & OVERTHINKING
            'overthinking': {
                'keywords': [
                    'overthinking',
                    'terus pikir',
                    'ngebas-ngebis',
                    'imajinasi',
                    'nebak-nebak',
                    'apa kalau',
                    'parang',
                ],
                'patterns': [
                    r'(terus|selalu).{0,15}pikir',
                    r'(pikir|khawatir).{0,15}(apa|jika|kalau)',
                    r'nebak.*sendiri',
                ],
                'severity': 'medium'
            },

            'anxiety_future': {
                'keywords': [
                    'takut masa depan',
                    'bingung masa depan',
                    'nggak tahu nasib',
                    'takut gagal',
                    'takut nggak bisa',
                    'quarter life crisis',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,15}(masa depan|gagal)',
                    r'(nggak|tidak).{0,15}tahu.*kemana',
                    r'(nasib|masa depan).*gelap',
                ],
                'severity': 'high'
            },

            # LONELINESS & ISOLATION
            'loneliness': {
                'keywords': [
                    'sendirian',
                    'soliter',
                    'kesepian',
                    'sepi',
                    'nggak ada yang ngerti',
                    'nggak ada orang',
                    'terisolir',
                ],
                'patterns': [
                    r'(sendirian|kesepian|sepi)',
                    r'nggak.*ada.*yang.*ngerti',
                    r'(merasa|jadi).{0,15}sepi',
                ],
                'severity': 'high'
            },

            'social_rejection': {
                'keywords': [
                    'dikucilkan',
                    'diejakin',
                    'dihina',
                    'diperolok',
                    'bullied',
                    'excluded',
                    'tidak diterima',
                ],
                'patterns': [
                    r'(dikucilkan|diejakin|dihina)',
                    r'(orang.*membully|dibully)',
                    r'tidak.*termasuk.*kelompok',
                ],
                'severity': 'high'
            },

            # ANGER & RESENTMENT
            'resentment': {
                'keywords': [
                    'kesal',
                    'jengkel',
                    'muak',
                    'naik darah',
                    'marah besar',
                    'dendam',
                ],
                'patterns': [
                    r'(kesal|jengkel|muak)',
                    r'(naik|panas).{0,15}(darah|hati)',
                    r'(dendam|benci).*dalam',
                ],
                'severity': 'medium'
            },

            'helplessness': {
                'keywords': [
                    'nggak bisa apa-apa',
                    'nggak ada kontrol',
                    'pasrah',
                    'putus asa',
                    'nyerah',
                    'nggak kuat lagi',
                ],
                'patterns': [
                    r'(nggak|tidak).{0,15}(bisa|kuasa).*apa',
                    r'(pasrah|nyerah)',
                    r'(putus|gantung).{0,15}asa',
                ],
                'severity': 'high'
            },

            # SHAME & GUILT
            'shame': {
                'keywords': [
                    'malu',
                    'memalukan',
                    'maluin',
                    'aib',
                    'disekatan',
                    'nggak terbuka',
                    'jerawat',
                    'acne',
                    'pimple',
                    'wajah',
                    'penampilan',
                    'jelek',
                    'gendut',
                    'gemuk',
                    'berat',
                    'kulit',
                    'rambut',
                    'gigi',
                    'ompong',
                    'nggak cantik',
                    'nggak ganteng',
                    'males ketemu',
                    'nggak pede ngobrol',
                    'embarrassed',
                    'ga pede',
                ],
                'patterns': [
                    r'(malu|maluin|memalukan)',
                    r'takut.*dibuka.*orang',
                    r'(jerawat|acne|pimple)',
                    r'(malu|shame).{0,20}(wajah|penampilan|jerawat)',
                    r'(males|nggak mau).{0,15}(ketemu|ngobrol)',
                    r'(ga|nggak).{0,10}pede',
                ],
                'severity': 'high'
            },

            'guilt': {
                'keywords': [
                    'salah sendiri',
                    'aku yang bersalah',
                    'aku yang bermasalah',
                    'dipukul hati',
                    'bersalah',
                    'menyesal',
                ],
                'patterns': [
                    r'(aku|saya).{0,15}(salah|bersalah|bermasalah)',
                    r'(menyesal|penyesalan).*dalam',
                    r'(tidak|nggak).{0,15}termaafkan',
                ],
                'severity': 'medium'
            },

            # DEPENDENCY & ATTACHMENT
            'emotional_dependency': {
                'keywords': [
                    'tergantung',
                    'nggak bisa tanpa',
                    'perlu terus',
                    'attachment',
                    'clinginess',
                ],
                'patterns': [
                    r'(tergantung|bergantung)',
                    r'nggak.*bisa.*tanpa',
                    r'(terus|selalu).*perlu',
                ],
                'severity': 'medium'
            },

            'anxious_attachment': {
                'keywords': [
                    'khawatir hubungan',
                    'takut ditinggal',
                    'perlu validasi',
                    'perlu perhatian',
                ],
                'patterns': [
                    r'(selalu|terus).{0,15}(cemas|khawatir).{0,15}hubungan',
                    r'(butuh|perlu).{0,15}(validasi|perhatian)',
                ],
                'severity': 'medium'
            },

            # DISCONNECTION & EMPTINESS
            'emptiness': {
                'keywords': [
                    'kosong',
                    'hampa',
                    'nggak ada arti',
                    'meaningless',
                    'void',
                    'kehampaan',
                ],
                'patterns': [
                    r'(kosong|hampa|void)',
                    r'(nggak|tidak).*ada.*arti',
                    r'(rasanya|jadi).*hampa',
                ],
                'severity': 'high'
            },

            'disconnection': {
                'keywords': [
                    'terputus',
                    'nggak connect',
                    'alienated',
                    'jauh',
                    'nggak ada koneksi',
                ],
                'patterns': [
                    r'(terputus|terasing)',
                    r'nggak.*ada.*connection',
                    r'(jauh|menjauh).*dari',
                ],
                'severity': 'medium'
            },

            # UNCERTAINTY & CONFUSION
            'uncertainty': {
                'keywords': [
                    'bingung',
                    'nggak tahu',
                    'tidak yakin',
                    'ragu-ragu',
                    'tidak pasti',
                ],
                'patterns': [
                    r'(bingung|ragu|tidak.*yakin)',
                    r'(nggak|tidak).{0,15}tahu.*apa',
                ],
                'severity': 'medium'
            },
        }

    def detect_micro_emotions(self, text: str) -> Dict[str, Tuple[bool, float]]:
        """
        Detect micro emotions with confidence scores
        Returns: {'emotion_name': (detected, confidence)}
        """
        text_lower = text.lower()
        results = {}

        for emotion_name, emotion_data in self.micro_emotions.items():
            detected = False
            confidence = 0.0

            # Check keywords
            for keyword in emotion_data['keywords']:
                if keyword in text_lower:
                    detected = True
                    confidence = max(confidence, 0.6)
                    break

            # Check regex patterns (higher confidence)
            if not detected or confidence < 0.8:
                for pattern in emotion_data['patterns']:
                    if re.search(pattern, text_lower):
                        detected = True
                        confidence = 0.85
                        break

            results[emotion_name] = (detected, confidence)

        return results

    def get_dominant_emotions(
        self, text: str, threshold: float = 0.6
    ) -> List[Tuple[str, float]]:
        """Get list of detected emotions sorted by confidence"""
        emotions = self.detect_micro_emotions(text)
        detected = [
            (name, conf)
            for name, (is_detected, conf) in emotions.items()
            if is_detected and conf >= threshold
        ]
        return sorted(detected, key=lambda x: x[1], reverse=True)

    def get_implied_emotions(self, text: str) -> List[str]:
        """
        Extract implied/hidden emotions behind explicit ones
        
        Example:
        - "lama bales" -> fear_of_abandonment, insecurity
        - "capek pura-pura kuat" -> emotional_exhaustion, emotional_suppression
        """
        emotions = self.get_dominant_emotions(text)
        implied = set()

        for emotion_name, _ in emotions:
            # Build implied emotion chains
            if emotion_name == 'fear_of_abandonment':
                implied.update(['insecurity', 'anxiety_future'])

            elif emotion_name == 'fear_of_rejection':
                implied.update(['shame', 'insecurity'])

            elif emotion_name == 'emotional_suppression':
                implied.update(['emotional_exhaustion', 'loneliness'])

            elif emotion_name == 'overthinking':
                implied.update(['anxiety_future', 'insecurity'])

            elif emotion_name == 'grief_loss':
                implied.update(['emptiness', 'loneliness'])

        return list(implied)

    def get_emotion_severity(self, text: str) -> str:
        """Rate overall emotional severity: low, medium, high, critical"""
        emotions = self.get_dominant_emotions(text, threshold=0.5)

        if not emotions:
            return 'low'

        # Count high-severity emotions
        high_severity_count = sum(
            1 for name, _ in emotions
            if self.micro_emotions[name]['severity'] == 'high'
        )

        if len(emotions) >= 4 or high_severity_count >= 2:
            return 'critical'
        elif high_severity_count >= 1 or len(emotions) >= 3:
            return 'high'
        elif len(emotions) >= 2:
            return 'medium'
        else:
            return 'low'


class DetailExtractor:
    """Extract specific details from user's message"""

    def __init__(self):
        self.detail_patterns = {
            # Changes
            'change_described': {
                'patterns': [
                    r'(berubah|jadi|menjadi|udah nggak).{0,30}(dari|seperti)',
                    r'(dulu|sebelumnya).{0,20}(sekarang|sekarang)',
                ],
                'category': 'change'
            },

            # Time aspect
            'duration': {
                'patterns': [
                    r'(sudah|udah|terus).{0,20}(berhari-hari|berminggu|berbulan|lama)',
                    r'(setiap|selalu|terus).{0,15}(hari|malam|waktu)',
                ],
                'category': 'duration'
            },

            # Isolation
            'feeling_alone': {
                'patterns': [
                    r'(sendirian|kesepian|sepi)',
                    r'nggak.*ada.*yang.*ngerti',
                ],
                'category': 'isolation'
            },

            # Specific person involved
            'relationship_context': {
                'patterns': [
                    r'(pacar|partner|dia|dia|bf|gf|suami|istri)',
                    r'(orang tua|ibunya|ayahnya|teman|sahabat|rekan kerja)',
                ],
                'category': 'person'
            },

            # Specific action/behavior
            'trigger_action': {
                'patterns': [
                    r'(lama bales|nggak bales|jarang hubungi)',
                    r'(pergi|tidak datang|membatalkan)',
                    r'(menghiraukan|mengabaikan|tidak peduli)',
                ],
                'category': 'trigger'
            },

            # Physical manifestation
            'physical_symptom': {
                'patterns': [
                    r'(gak tidur|tidak bisa tidur|begadang)',
                    r'(gak makan|tidak makan|mual)',
                    r'(pusing|sakit kepala|sesak)',
                ],
                'category': 'physical'
            },

            # Self-blame
            'self_blame': {
                'patterns': [
                    r'(aku.*salah|salah.*sendiri)',
                    r'(aku.*yang.*bermasalah)',
                    r'(aku.*tidak.*cukup)',
                ],
                'category': 'blame'
            },
        }

    def extract_details(self, text: str) -> Dict[str, List[str]]:
        """Extract categorized details from message"""
        text_lower = text.lower()
        extracted = {}

        for detail_name, detail_data in self.detail_patterns.items():
            category = detail_data['category']

            for pattern in detail_data['patterns']:
                matches = re.findall(pattern, text_lower)
                if matches:
                    if category not in extracted:
                        extracted[category] = []
                    extracted[category].append(detail_name)

        return extracted

    def get_key_words(self, text: str) -> List[str]:
        """Extract key emotional/action words"""
        keywords = []

        # Define key word patterns
        patterns = {
            'change': r'\b(berubah|jadi|menjadi|bermodal)\b',
            'fear': r'\b(takut|khawatir|cemas|panik)\b',
            'loss': r'\b(hilang|pergi|lepas|putus|ditinggal)\b',
            'pain': r'\b(sakit|pedih|nyeri)\b',
            'exhaustion': r'\b(capek|lelah|habis|lemes)\b',
            'confusion': r'\b(bingung|nggak tahu|tidak yakin)\b',
            'isolation': r'\b(sendirian|sepi|kesepian|terisolir)\b',
        }

        text_lower = text.lower()

        for category, pattern in patterns.items():
            if re.search(pattern, text_lower):
                keywords.append(category)

        return keywords


class IntentDetector:
    """Detect user's true intent behind the message"""
    
    def __init__(self):
        self.intents = {
            'advice_seeking': {
                'keywords': [
                    'gimana cara',
                    'gimana caranya',
                    'apa yang harus',
                    'harus gimana',
                    'apa yang bisa',
                    'cara ngatasinnya',
                    'solusinya',
                    'biar nggak',
                    'agar nggak',
                    'supaya',
                    'tips',
                    'saran',
                    'bantu',
                    'bantuin',
                    'aku harus',
                ],
                'patterns': [
                    r'(gimana|bagaimana).{0,5}(cara|caranya)',
                    r'(apa|bagaimana).{0,5}(harus|yang harus)',
                    r'(harus|bisa).{0,15}(gimana|bagaimana)',
                    r'(cara|solusi).{0,15}(apa|gimana)',
                    r'biar.*nggak',
                    r'agar.*nggak',
                ],
                'weight': 1.0
            },
            
            'validation_seeking': {
                'keywords': [
                    'itu normal',
                    'wajar nggak',
                    'salah nggak',
                    'nggak salah',
                    'boleh nggak',
                    'pantas nggak',
                    'layak nggak',
                    'aneh nggak',
                    'gila nggak',
                ],
                'patterns': [
                    r'(itu|ini).{0,10}(normal|wajar|salah)',
                    r'(normal|wajar|salah).{0,10}(nggak|gak)',
                    r'boleh.{0,15}(aku|aku gini)',
                    r'(aku|saya).{0,15}(wajar|normal|salah)',
                ],
                'weight': 0.8
            },
            
            'venting': {
                'keywords': [
                    'kesal banget',
                    'muak',
                    'bosan',
                    'lelah banget',
                    'capek banget',
                    'males',
                    'jengkel',
                    'kesel',
                    'ahhh',
                    'argh',
                    'aku emosi',
                ],
                'patterns': [
                    r'(kesal|muak|jengkel).{0,15}banget',
                    r'(capek|lelah).{0,15}banget',
                    r'(boong|goblok|dasar).*deh',
                    r'(ahhh|argh|huff).*',
                ],
                'weight': 0.7
            },
            
            'reflection_seeking': {
                'keywords': [
                    'apa arti',
                    'apa maksud',
                    'apa alasan',
                    'kenapa aku',
                    'kenapa dia',
                    'kenapa kok',
                    'kenapa jadi',
                    'apa yang salah',
                    'apa yang bikin',
                ],
                'patterns': [
                    r'(apa|apakah).{0,15}(arti|maksud|alasan)',
                    r'(kenapa|why).{0,15}(aku|aku jadi|dia)',
                    r'apa.{0,15}(yang|yang membuat|yang bikin)',
                ],
                'weight': 0.75
            },
            
            'emotional_support': {
                'keywords': [
                    'tolong',
                    'tolongin',
                    'bantuin aku',
                    'nemenin',
                    'temani',
                    'nggak kuat',
                    'gak sanggup',
                    'butuh',
                    'perlu',
                    'help',
                ],
                'patterns': [
                    r'(tolong|bantuin|tolongin).{0,15}aku',
                    r'(nemenin|temani).{0,15}(aku|saya)',
                    r'(nggak|gak).{0,15}(kuat|sanggup)',
                    r'(butuh|perlu).{0,15}(seseorang|orang)',
                ],
                'weight': 0.8
            },
            
            'emotional_masking': {
                'keywords': [
                    'pura-pura',
                    'nggak apa',
                    'fine',
                    'oke aja',
                    'biasa aja',
                    'nggak masalah',
                    'gapapa',
                    'udah move on',
                    'udah ikhlas',
                ],
                'patterns': [
                    r'(pura-pura|fakenya).{0,15}kuat',
                    r'(nggak|gak|tidak).{0,15}(apa|masalah|oke)',
                    r'(fine|oke|okay).*aja',
                    r'(udah|sudah).{0,15}(move on|ikhlas)',
                ],
                'weight': 0.7
            },
            
            'overthinking': {
                'keywords': [
                    'terus mikir',
                    'terus pikir',
                    'ngebas-ngebis',
                    'apa kalau',
                    'tapi apa',
                    'kalau misalnya',
                    'nggak bisa tidur',
                    'kemarin terus',
                    'sejak itu',
                ],
                'patterns': [
                    r'(terus|selalu).{0,15}(mikir|pikir)',
                    r'(apa|jika|kalau).{0,15}(kalau|misalnya|aku)',
                    r'(ngebas|ngebis|nebak).*sendiri',
                ],
                'weight': 0.65
            },
            
            'future_anxiety': {
                'keywords': [
                    'takut masa depan',
                    'bingung masa depan',
                    'nggak tahu nasib',
                    'gelap banget',
                    'quarter life',
                    'takut gagal',
                    'takut sendirian selamanya',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,15}masa depan',
                    r'(masa depan|nasib).{0,15}(gelap|suram)',
                    r'(takut|khawatir).{0,15}(gagal|nggak bisa)',
                ],
                'weight': 0.8
            },
            
            'loneliness': {
                'keywords': [
                    'nggak ada orang',
                    'nggak ada yang ngerti',
                    'sendirian',
                    'kesepian',
                    'nggak ada teman',
                    'merasa sepi',
                    'terisolir',
                ],
                'patterns': [
                    r'(nggak|gak).*ada.*yang',
                    r'(sendirian|kesepian|sepi)',
                    r'(merasa|jadi).{0,15}(sepi|sendirian)',
                ],
                'weight': 0.75
            },
            
            'relationship_distress': {
                'keywords': [
                    'pacar',
                    'partner',
                    'perubahan',
                    'lama bales',
                    'jarang hubungi',
                    'jarak',
                    'hubungan',
                    'pacaran',
                    'putus',
                ],
                'patterns': [
                    r'(pacar|partner|dia).{0,15}(berubah|dingin)',
                    r'(lama|jarang).{0,15}(bales|hubungi)',
                    r'hubungan.*sulit',
                ],
                'weight': 0.7
            },
            
            'self_worth_issue': {
                'keywords': [
                    'nggak cukup',
                    'nggak layak',
                    'kurang',
                    'nggak bagus',
                    'minder',
                    'ragu',
                    'kalah',
                    'nggak percaya diri',
                ],
                'patterns': [
                    r'(nggak|gak).{0,15}(cukup|layak|bagus)',
                    r'(kurang|nggak).*dibanding',
                    r'(minder|ragu|takut).{0,15}diri',
                ],
                'weight': 0.7
            },
        }
    
    def detect_intent(self, text: str) -> Dict[str, float]:
        """
        Detect user's intent with confidence scores
        Returns: {'intent_name': confidence_score, ...}
        """
        text_lower = text.lower()
        intent_scores = {}
        
        for intent_name, intent_data in self.intents.items():
            score = 0.0
            
            # Check keywords (lower confidence)
            for keyword in intent_data['keywords']:
                if keyword in text_lower:
                    score = max(score, 0.5 * intent_data['weight'])
                    break
            
            # Check patterns (higher confidence)
            for pattern in intent_data['patterns']:
                if re.search(pattern, text_lower):
                    score = max(score, 0.85 * intent_data['weight'])
            
            if score > 0:
                intent_scores[intent_name] = score
        
        return intent_scores
    
    def get_primary_intent(self, text: str) -> Tuple[Optional[str], float]:
        """Get the primary/dominant intent"""
        scores = self.detect_intent(text)
        
        if not scores:
            return None, 0.0
        
        primary = max(scores.items(), key=lambda x: x[1])
        return primary
    
    def has_advice_request(self, text: str) -> bool:
        """Check if user is asking for advice"""
        scores = self.detect_intent(text)
        return scores.get('advice_seeking', 0.0) > 0.5
    
    def is_venting(self, text: str) -> bool:
        """Check if user is venting"""
        scores = self.detect_intent(text)
        return scores.get('venting', 0.0) > 0.5
    
    def is_seeking_validation(self, text: str) -> bool:
        """Check if user is seeking validation"""
        scores = self.detect_intent(text)
        return scores.get('validation_seeking', 0.0) > 0.5
