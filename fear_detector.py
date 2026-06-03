"""
Fear Detector - Detects underlying fears and anxieties
Explicit fears: takut, khawatir, cemas
Implicit fears: hidden worries that users don't explicitly mention
"""

from typing import Dict, List, Tuple, Optional
import re


class FearDetector:
    """
    Detects explicit and implicit fears behind user's messages.
    """
    
    def __init__(self):
        self.fear_patterns = {
            # EXPLICIT FEARS - User directly states fear
            'fear_of_failure': {
                'keywords': [
                    'takut gagal', 'khawatir gagal', 'cemas gagal',
                    'takut tidak lulus', 'takut tidak bisa', 'takut nggak bisa',
                    'takut salah', 'takut jelek',
                    'nggak bisa', 'pasti gagal', 'takut gagal',
                ],
                'patterns': [
                    r'(takut|khawatir|cemas).{0,20}(gagal|tidak lulus|nggak lulus|tidak bisa|nggak bisa)',
                    r'(gagal|fail).{0,20}(terus|terus-terusan|selalu)',
                    r'(takut|khawatir).{0,20}(tidak|nggak|ga).{0,15}ikut',  # "tidak bisa ikut ujian"
                ],
                'category': 'explicit',
                'severity': 'high'
            },
            
            'fear_of_rejection': {
                'keywords': [
                    'takut ditolak', 'khawatir ditolak',
                    'takut nggak diterima', 'takut nggak cocok',
                    'takut ganggu', 'takut bawel',
                    'takut dibenci', 'takut dimarahin',
                ],
                'patterns': [
                    r'(takut|khawatir|cemas).{0,20}(ditolak|diterima|diterima)',
                    r'(takut|khawatir).{0,20}(ganggu|bawel|dibenci|dimarah)',
                ],
                'category': 'explicit',
                'severity': 'high'
            },
            
            'fear_of_abandonment': {
                'keywords': [
                    'takut ditinggal', 'takut kehilangan',
                    'takut pergi', 'takut meninggal',
                    'takut jauh', 'takut sendirian',
                    'takut nggak peduli', 'takut lupa',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,20}(ditinggal|kehilangan|pergi)',
                    r'(takut|khawatir).{0,20}(sendirian|aja|aja)',
                ],
                'category': 'explicit',
                'severity': 'high'
            },
            
            'fear_of_judgment': {
                'keywords': [
                    'takut dinilai', 'takut dijudge',
                    'takut diliatin', 'takut dikritik',
                    'takut dibandingin', 'takut diolok',
                    'takut dilihat', 'takut shame',
                    'malu', 'minder', 'malu ketemu',
                    'tidak percaya diri',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,20}(dinilai|dijudge|dikritik)',
                    r'(takut|khawatir).{0,20}(dibandingin|diolok|diliatin)',
                    r'(malu|shame|minder).{0,30}(banget|terus|selalu)',
                    r'(malu|shame).{0,20}(ketemu|bertemu|tampil)',
                    r'(mikir|pikir).{0,30}(orang melihat|orang nilai)',
                ],
                'category': 'explicit',
                'severity': 'high'
            },
            
            'fear_of_inadequacy': {
                'keywords': [
                    'takut nggak cukup', 'takut nggak layak',
                    'takut nggak bagus', 'takut nggak bisa',
                    'takut kalah', 'takut kurang',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,20}(nggak|tidak).{0,20}(cukup|layak|bagus)',
                    r'(takut|khawatir).{0,20}(kalah|kurang)',
                ],
                'category': 'explicit',
                'severity': 'medium'
            },
            
            'fear_of_change': {
                'keywords': [
                    'takut berubah', 'takut dulu tidak sama',
                    'takut lain dari sebelum',
                    'takut tidak sama lagi',
                ],
                'patterns': [
                    r'(takut|khawatir).{0,20}(berubah|tidak sama|lain)',
                ],
                'category': 'explicit',
                'severity': 'medium'
            },
            
            'fear_of_future': {
                'keywords': [
                    'takut masa depan', 'khawatir masa depan',
                    'takut nanti', 'takut akan datang',
                    'cemas masa depan', 'anxiety tentang nanti',
                ],
                'patterns': [
                    r'(takut|khawatir|cemas).{0,20}(masa depan|nanti|akan)',
                ],
                'category': 'explicit',
                'severity': 'high'
            },
            
            # IMPLICIT FEARS - Hidden behind user's words
            'implied_fear_of_worth': {
                'keywords': [
                    'nggak cukup', 'nggak layak', 'nggak pantas',
                    'kurang', 'lebih jelek', 'beda',
                    'dibandingin', 'dilihat', 'dikira',
                    'minder', 'malu',
                ],
                'patterns': [
                    r'(nggak|tidak).{0,20}(cukup|layak|pantas)',
                    r'(bandingin|dilihat|dikira)',
                    r'(minder|malu).{0,30}(dengan|sama|dari)',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_judgment + fear_of_inadequacy',
                'severity': 'medium'
            },
            
            'implied_fear_of_loss': {
                'keywords': [
                    'berubah', 'dingin', 'jauh', 'lama bales',
                    'nggak peduli', 'berubah jadi', 'tidak sama',
                    'hilang', 'gone', 'pergi',
                ],
                'patterns': [
                    r'(berubah|dingin|jauh).{0,20}(karena|sejak)',
                    r'(lama|jarang).{0,20}(bales|chat|hubungi)',
                    r'(berubah|tidak).{0,20}(sama|peduli)',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_abandonment + fear_of_loss',
                'severity': 'high'
            },
            
            'implied_fear_of_failure': {
                'keywords': [
                    'banyak tugas', 'semua deadline', 'banyak ujian',
                    'nggak bisa', 'tidak tahu', 'bingung',
                    'kewalahan', 'overwhelm', 'terlalu banyak',
                    'capek', 'lelah', 'exhaust',
                ],
                'patterns': [
                    r'(banyak|semua|terlalu).{0,20}(tugas|deadline|ujian)',
                    r'(nggak|tidak).{0,20}(bisa|tahu|mengerti)',
                    r'(kewalahan|overwhelm|terlalu banyak)',
                    r'(capek|lelah|exhaust).{0,20}(tapi masih|dan masih)',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_failure + fear_of_inadequacy',
                'severity': 'high'
            },
            
            'implied_fear_of_loneliness': {
                'keywords': [
                    'sendirian', 'sepi', 'aja', 'tidak ada teman',
                    'diabaikan', 'dilupakan', 'nggak ada yang',
                    'orang tidak peduli', 'tidak fit in',
                ],
                'patterns': [
                    r'(sendirian|sepi|aja).{0,30}(terus|selalu)',
                    r'(tidak|nggak).{0,20}ada.{0,20}(orang|teman|yang)',
                    r'(diabaikan|dilupakan|lupa)',
                    r'(tidak|nggak).{0,20}fit in',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_abandonment + loneliness',
                'severity': 'high'
            },
            
            'implied_fear_of_inadequacy': {
                'keywords': [
                    'orang lain bisa', 'dia bisa', 'semua bisa',
                    'cuma aku', 'cuma gue', 'hanya aku',
                    'nggak kayak', 'tidak seperti', 'berbeda',
                    'tertinggal', 'slow', 'lambat',
                ],
                'patterns': [
                    r'(orang lain|semua|dia).{0,20}(bisa|berhasil|bisa)',
                    r'(cuma|hanya).{0,20}(aku|gue|saya).{0,20}(tidak|nggak)',
                    r'(tertinggal|slow|lambat)',
                    r'(tidak|nggak).{0,20}kayak.{0,20}(orang lain|semua)',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_inadequacy + social_comparison',
                'severity': 'medium'
            },
            
            'implied_fear_of_uncertainty': {
                'keywords': [
                    'tidak tahu', 'bingung', 'tidak mengerti',
                    'tidak jelas', 'tidak pasti', 'mungkin',
                    'kemungkinan', 'bagaimana jika', 'entahlah',
                    'masa depan', 'akan jadi', 'akan gimana',
                ],
                'patterns': [
                    r'(tidak|nggak).{0,20}(tahu|mengerti|paham|jelas)',
                    r'(bingung|confused|tidak pasti)',
                    r'(bagaimana|gimana).{0,20}(jika|kalau|nanti)',
                    r'(masa depan|akan|nanti).{0,20}(gimana|apa|bagaimana)',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_uncertainty + fear_of_future',
                'severity': 'medium'
            },
            
            'implied_fear_of_catastrophe': {
                'keywords': [
                    'overthinking', 'worst case', 'skenario terburuk',
                    'bagaimana kalau', 'kalau apa', 'pasti bakal',
                    'stress', 'panik', 'panic',
                    'tidak bisa tidur', 'tidur berantakan', 'insomnia',
                ],
                'patterns': [
                    r'(overthinking|over thinking)',
                    r'(skenario|scenario).{0,20}(terburuk|worst|buruk)',
                    r'(bagaimana|gimana|kalau).{0,20}(terus|selalu|pasti)',
                    r'(pasti|akan).{0,20}(jadi|terjadi|jelek|buruk|salah)',
                    r'(stress|panik).{0,20}(terus|banget|banget sekali)',
                    r'(tidur).{0,20}(berantakan|tidak bisa|nggak bisa)',
                ],
                'category': 'implicit',
                'underlying_fear': 'fear_of_catastrophe + anxiety',
                'severity': 'high'
            },
        }
    
    def detect(self, user_message: str) -> List[Tuple[str, float, str]]:
        """
        Detect fears from user message.
        Returns: [(fear_name, confidence_score, category), ...]
        """
        user_lower = user_message.lower()
        detected_fears = []
        
        for fear_name, fear_config in self.fear_patterns.items():
            confidence = 0
            
            # Check keywords
            keyword_matches = 0
            for keyword in fear_config['keywords']:
                if keyword in user_lower:
                    keyword_matches += 1
            
            if keyword_matches > 0:
                # Implicit fears need higher confidence threshold
                if fear_config['category'] == 'implicit':
                    confidence = min(keyword_matches * 0.15, 0.6)
                else:
                    confidence = min(keyword_matches * 0.18, 0.7)
            
            # Check patterns
            for pattern in fear_config['patterns']:
                if re.search(pattern, user_lower):
                    if fear_config['category'] == 'implicit':
                        confidence = max(confidence, 0.65)
                    else:
                        confidence = max(confidence, 0.8)
                    break
            
            if confidence > 0.3:
                detected_fears.append((fear_name, confidence, fear_config['category']))
        
        # Sort by confidence
        detected_fears.sort(key=lambda x: x[1], reverse=True)
        return detected_fears
    
    def get_underlying_fears(self, user_message: str) -> Dict[str, float]:
        """
        Get all fears (explicit + implicit) mapped to confidence.
        """
        fears = self.detect(user_message)
        return {fear[0]: fear[1] for fear in fears}
    
    def get_primary_fear(self, user_message: str) -> Optional[Tuple[str, float]]:
        """Get the strongest detected fear"""
        fears = self.detect(user_message)
        return (fears[0][0], fears[0][1]) if fears else None
