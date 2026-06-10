"""
Dynamic Response Builder
- Builds layered responses based on emotions, details, and context
- Reflects user's story with specific details
- Detects implied emotions and validates them
- Creates human-like conversational responses
- Uses weighted contextual selection (not pure random)
- Includes detail mentions from user's story
- Humanizes final response to feel natural
- Handles advice-seeking with practical support
- Maintains emotional continuity across conversation
"""

from typing import Dict, List, Tuple, Optional
import re
import random
import time
from emotion_analyzer import MicroEmotionDetector, DetailExtractor, IntentDetector
from emotional_memory import EmotionalMemory
from advice_support_builder import AdviceSupportBuilder


class TopicEmotionMapper:
    """
    Map any topic/problem to underlying emotions.
    
    Handles case where:
    - detector gagal
    - emotion kosong
    - topic belum ada di patterns
    
    Tetap bisa generate emotional reflection dengan memetakan:
    topik → kemungkinan emosi → refleksi emosional
    """
    
    def __init__(self):
        # Topic to underlying emotions mapping
        self.topic_emotion_map = {
        # APPEARANCE/BODY IMAGE
            'jerawat|acne|pimple': ['shame', 'body_image_issue', 'fear_of_judgment', 'insecurity'],
            'gigi|gigi ompong|gigi goyang|ompong': ['shame', 'social_insecurity', 'fear_of_rejection', 'minder'],
            'berat|gemuk|gendut|badan|weight': ['shame', 'body_image_issue', 'insecurity', 'fear_of_judgment'],
            'jelek|nggak cantik|nggak ganteng': ['shame', 'insecurity', 'low_self_esteem'],
            'rambut|kulit|penampilan|appearance': ['shame', 'body_image_issue', 'social_anxiety'],
            'malu|embarrassed|malu banget': ['shame', 'body_image_issue', 'fear_of_judgment'],
            
            # ACADEMIC/PROFESSIONAL
            'nilai|grade|ujian|test|exam': ['fear_of_failure', 'pressure', 'self_worth_issue', 'anxiety'],
            'sekolah|sekolahan': ['stress', 'pressure', 'social_anxiety', 'fear_of_failure'],
            'kerjaan|pekerjaan|kerja': ['stress', 'burnout', 'insecurity', 'fear_of_inadequacy'],
            'bocor|jelek|gagal': ['shame', 'fear_of_failure', 'self_worth_issue'],
            
            # RELATIONSHIP
            'pasangan|partner|pacar|bf|gf': ['fear_of_abandonment', 'anxiety', 'insecurity', 'overthinking'],
            'berubah|dingin|jauh': ['fear_of_abandonment', 'anxiety', 'fear_of_loss', 'overthinking'],
            'lama bales|jarang hubungi': ['anxiety', 'fear_of_abandonment', 'insecurity'],
            'putus|break up|break': ['grief', 'loss', 'abandonment', 'sadness', 'despair'],
            'teman|friendship': ['loneliness', 'social_anxiety', 'insecurity', 'fear_of_rejection'],
            
            # FAMILY
            'orang tua|ibu|ayah|ortu': ['family_conflict', 'pressure', 'anxiety', 'insecurity'],
            'saudara|adik|kakak': ['conflict', 'comparison', 'insecurity', 'rivalry'],
            
            # MENTAL STATE
            'capek|tired|lelah|exhausted': ['emotional_exhaustion', 'burnout', 'depression', 'hopelessness'],
            'sedih|sad|sadsad|sedih banget': ['sadness', 'grief', 'despair', 'hopelessness'],
            'takut|khawatir|cemas|anxious|anxiety': ['anxiety', 'fear', 'worry', 'dread'],
            'nggak bisa|helpless|nggak tahu|confuse': ['helplessness', 'confusion', 'despair', 'anxiety'],
            'sendirian|sepi|lonely|alone': ['loneliness', 'isolation', 'abandonment', 'despair'],
            'hampa|kosong|empty': ['emptiness', 'depression', 'hopelessness', 'disconnection'],
            'overthink|pikiran|mikirin|thinking': ['anxiety', 'overthinking', 'rumination', 'stress'],
            
            # SELF-WORTH
            'nggak cukup|nggak layak|kurang': ['insecurity', 'low_self_esteem', 'shame', 'unworthiness'],
            'percaya diri|pede|confidence': ['insecurity', 'low_self_esteem', 'self_doubt'],
            'malu|shame|embarrassed': ['shame', 'embarrassment', 'social_anxiety', 'fear_of_judgment'],
            'bersalah|guilty|bersalahan': ['guilt', 'shame', 'self_blame', 'regret'],
            
            # FUTURE/UNCERTAINTY
            'masa depan|future|nanti|akan': ['anxiety_future', 'uncertainty', 'fear', 'despair'],
            'jalan keluar|solusi|fix|cara': ['helplessness', 'anxiety', 'confusion'],
            
            # SOCIAL
            'beda|berbeda|different|tertinggal': ['comparison', 'insecurity', 'low_self_esteem', 'isolation'],
            'dinilai|judge|judgement': ['fear_of_judgment', 'social_anxiety', 'insecurity'],
            'diliatin|dikritik|dikira': ['shame', 'fear_of_judgment', 'social_anxiety'],
        }
    
    def get_underlying_emotions(self, user_message: str) -> List[str]:
        """Get potential underlying emotions for any message"""
        user_lower = user_message.lower()
        detected_emotions = set()
        
        for topic_pattern, emotions in self.topic_emotion_map.items():
            if re.search(topic_pattern, user_lower):
                detected_emotions.update(emotions)
        
        return list(detected_emotions) if detected_emotions else ['uncertainty']
    
    def get_primary_emotion(self, user_message: str) -> str:
        """Get single most likely underlying emotion"""
        emotions = self.get_underlying_emotions(user_message)
        # Return first emotion (most common)
        return emotions[0] if emotions else 'uncertainty'


class UniversalEmotionalReflectionEngine:
    """
    Generate emotionally intelligent reflections untuk topik apapun.
    
    Tidak hanya "aku siap dengarkan"
    Tapi actual emotional reflection yang menunjukkan pemahaman.
    """
    
    def __init__(self):
        self.topic_mapper = TopicEmotionMapper()
        
        # Refleksi emosi spesifik - natural Indonesian, emotionally intelligent
        self.emotional_reflections = {
            'insecurity': [
                "Pasti ada rasa takut kalo orang lain nanti akan nilai atau bandingin kamu.",
                "Ketika rasa percaya diri mulai goyah, hal-hal kecil jadi terasa besar.",
                "Perasaan kayak nggak cukup itu emang berat dan bikin kita ngerasa nggak aman.",
                "Kalau nggak percaya diri, setiap interaksi jadi terasa berat di pikiran.",
                "Ada suara di kepala yang terus bilang 'kamu nggak cukup baik', dan itu capek.",
                "Pas kamu bandingin diri sama orang lain, rasanya selalu kurang.",
            ],
            'body_image_issue': [
                "Kadang hal yang kecil soal penampilan bisa jadi besar banget buat rasa percaya diri kita.",
                "Ketika ada sesuatu tentang badan yang mengganggu pikiran, itu bisa bikin kita jadi nggak nyaman sama diri sendiri.",
                "Perasaan malu dengan penampilan itu benar dan bisa sangat membuat orang jadi sendiri.",
                "Hal-hal yang sebenarnya nggak penting buat orang lain, tapi buat kita bisa menjadi beban yang berat.",
                "Kalau pikiran terus kembali ke penampilan, itu emang bisa bikin capek emosionalnya.",
            ],
            'fear_of_judgment': [
                "Pasti ada rasa takut kalo orang lain akan lihat dan judge kamu.",
                "Takut dilihat atau dinilai itu rasa yang bener-bener banyak orang alamin.",
                "Kalau selalu khawatir sama penilaian orang, itu bikin susah untuk santai.",
                "Rasanya orang terus liat dan nilai kamu, bahkan cuma di pikiran kamu sendiri.",
            ],
            'shame': [
                "Rasa malu itu bikin kita pengen sembunyi dari orang lain.",
                "Pas ada yang terasa memalukan, rasanya pengen menjauh dan nggak ketemu siapa-siapa.",
                "Rasa malu biasanya bikin kita pendem sendiri, nggak cerita ke orang lain.",
                "Perasaan kayak ada yang salah dengan diri sendiri itu emang berat.",
                "Malu dengan penampilan itu membuat kita merasa nggak layak untuk ketemu orang.",
                "Ketika shame tentang penampilan muncul, semuanya jadi terasa tentang itu aja.",
            ],
            'fear_of_abandonment': [
                "Takut kehilangan atau ditinggal orang penting itu emang salah satu yang paling nyakitin.",
                "Pas ada perubahan kecil dalam hubungan, langsung timbul khawatir kalo orang mau pergi.",
                "Nggak tahu pasti orang bakal tetap atau nggak itu bikin hati goyah.",
                "Takut ditinggal sering bikin kita terus mikirin setiap yang dilakukan orang itu.",
            ],
            'anxiety': [
                "Rasa khawatir yang terus ada itu emang bikin capek.",
                "Pas pikiran terus berputar tentang hal-hal yang mungkin terjadi, susah untuk santai.",
                "Kecemasan yang terus ada itu bukan cuma di kepala, tapi tubuh juga jadi lelah.",
                "Kalau khawatir terus ada, jadi susah untuk nikmati hal yang seharusnya fun.",
            ],
            'emotional_exhaustion': [
                "Kelelahan emosional itu lebih dalam daripada hanya tubuh terasa lelah.",
                "Ketika energi buat bertahan udah habis, semuanya jadi terasa penuh dan susah.",
                "Capek terus-menerus itu bukan hanya tentang perasaan, tapi juga habisnya kemampuan buat kuat.",
                "Kalau kepala udah penuh dengan beban, bahkan hal-hal yang biasanya mudah jadi terasa sangat berat.",
            ],
            'loneliness': [
                "Merasa sendirian adalah salah satu rasa yang paling dalam dan menyakitkan.",
                "Kesepian bukan hanya tentang nggak ada orang, tapi tentang ngerasa nggak ada yang benar-benar ngerti.",
                "Ketika merasa sendirian, itu bisa membuat semuanya terasa lebih gelap.",
                "Kesepian yang dalam sering kali lebih menyakitkan daripada hal-hal yang terlihat jelas.",
            ],
            'sadness': [
                "Kesedihan yang dalam itu butuh waktu dan tempat untuk bisa diproses dengan baik.",
                "Ketika ada kehilangan atau kekecewaan, itu natural buat merasa sedih dan lemas.",
                "Kesedihan yang mendalam sering kali diikuti dengan rasa hampa dan putus asa.",
            ],
            'helplessness': [
                "Merasa nggak bisa apa-apa adalah salah satu perasaan yang paling sulit.",
                "Ketika kontrol hilang, itu bisa membuat kita merasa sangat lemah dan nggak berdaya.",
                "Rasa nggak berdaya sering kali adalah awal dari rasa putus asa yang lebih dalam.",
            ],
            'overthinking': [
                "Pikiran yang terus berputar itu bikin capek banget buat dijalanin.",
                "Ketika pikiran mulai membuat skenario yang belum tentu terjadi, itu bisa sangat menguras pikiran.",
                "Terlalu banyak mikir adalah bentuk kekhawatiran yang sering tersembunyi di balik 'hanya berpikir'.",
                "Kalau kepala terus penuh dengan kemungkinan buruk, itu susah buat santai dan present.",
            ],
            'fear_of_failure': [
                "Takut gagal itu bisa membuat kita jadi lumpuh dan nggak mau maju.",
                "Ketakutan tentang nggak cukup baik itu bisa berat banget dibawa.",
                "Takut gagal sering kali terhubung sama perasaan nggak berharga dan nilai diri yang rendah.",
            ],
            'guilt': [
                "Rasa bersalah yang dalam itu bikin kita jadi keras dalam menilai diri sendiri.",
                "Rasa bersalah adalah emosi yang sering bikin orang pendem sendiri dan nggak cerita.",
                "Ketika merasa bersalah, itu bisa bikin kita terus hukum diri sendiri berulang-ulang.",
            ],
            'self_worth_issue': [
                "Ketika perasaan nggak berharga, setiap hal jadi terasa seperti pujian atau penolakan.",
                "Perasaan kayak nggak worth anything itu berat banget dibawa setiap hari.",
                "Rasa nggak percaya diri sering kali membuat kita menilai hal-hal netral jadi negatif.",
            ],
            'uncertainty': [
                "Nggak tahu apa yang bakalan terjadi itu bisa bikin cemas dan gelisah.",
                "Ketidakpastian tentang masa depan bisa membuat pikiran jadi penuh dengan hal-hal yang menakutkan.",
            ],
            'pressure': [
                "Tekanan dari berbagai arah itu bisa membuat rasanya ada beban di dada.",
                "Ketika tekanan menumpuk, itu bisa susah buat bernafas dan santai.",
            ],
            'comparison': [
                "Membandingkan diri sama orang lain itu seperti permainan yang kita selalu kalah.",
                "Ketika terus membandingkan, itu bisa bikin rasa nggak percaya diri jadi semakin dalam.",
            ],
            'stress': [
                "Stress yang terus-terusan itu bukan cuma pikiran, tapi juga badan terasa terganggu.",
                "Ketika stress menumpuk, itu bisa susah buat berpikir jernih dan bertahan.",
            ],
        }
    
    def generate_reflection(
        self, 
        user_message: str,
        emotions_detected: Optional[List[Tuple]] = None
    ) -> str:
        """
        Generate emotional reflection untuk any message.
        
        Tidak hanya acknowledgement, tapi true reflection tentang
        potential emotional state berdasarkan message content.
        """
        
        # 1. Get underlying emotions dari message
        primary_emotion = self.topic_mapper.get_primary_emotion(user_message)
        
        # 2. Jika ada detected emotions dari detector, use those sebagai hint
        if emotions_detected and len(emotions_detected) > 0:
            emotion_name = emotions_detected[0][0]
            if emotion_name in self.emotional_reflections:
                primary_emotion = emotion_name
        
        # 3. Generate reflection
        if primary_emotion in self.emotional_reflections:
            return random.choice(self.emotional_reflections[primary_emotion])
        else:
            # Default universal reflection
            return random.choice(self.emotional_reflections['uncertainty'])


class ResponseWeightSelector:
    """
    Weighted contextual response selection
    (not pure random - considers context, emotions, memory, stage)
    """

    def __init__(self):
        self.weights = {
            'emotion_match': 0.4,      # How well template matches dominant emotion
            'context_relevance': 0.25,  # How relevant to conversation context
            'detail_mention': 0.2,      # Whether template mentions extracted details
            'stage_appropriateness': 0.15,  # How appropriate for conversation stage
        }

    def select_weighted(
        self,
        templates: List[str],
        context: Dict
    ) -> str:
        """
        Select response template based on weights
        Context includes: emotions, details, stage, memory, etc
        """
        if not templates:
            return ""

        if len(templates) == 1:
            return templates[0]

        # Calculate scores for each template
        scores = []
        for template in templates:
            score = self._calculate_template_score(template, context)
            scores.append(score)

        # Select based on weighted scores
        max_score = max(scores) if scores else 0
        if max_score > 0:
            # Weighted random selection (higher scores more likely)
            weights = [s / max_score for s in scores]
            selected = random.choices(templates, weights=weights, k=1)[0]
            return selected
        else:
            return random.choice(templates)

    def _calculate_template_score(self, template: str, context: Dict) -> float:
        """Calculate score for a template based on context"""
        score = 0.0

        # 1. Emotion match
        emotions = context.get('emotions', [])
        dominant_emotion = emotions[0][0] if emotions else None
        
        # Check if template mentions emotion-related keywords
        emotional_keywords = [
            'takut', 'khawatir', 'cemas', 'sedih', 'capek', 'lelah',
            'sendirian', 'kosong', 'hampa', 'nggak cukup', 'bersalah'
        ]
        if any(kw in template.lower() for kw in emotional_keywords):
            score += self.weights['emotion_match'] * 0.8

        # 2. Context relevance
        # Check if template mentions details or specific situations
        context_keywords = [
            'perubahan', 'berubah', 'tiba-tiba', 'biasanya', 'sekarang',
            'dulu', 'terus', 'selalu', 'malam', 'siang', 'terus menerus'
        ]
        if any(kw in template.lower() for kw in context_keywords):
            score += self.weights['context_relevance']

        # 3. Detail mention - if template is specific
        details = context.get('details', {})
        detail_keywords = []
        for category, items in details.items():
            detail_keywords.extend(items)
        
        if detail_keywords and any(
            kw.lower() in template.lower() for kw in detail_keywords
        ):
            score += self.weights['detail_mention'] * 1.5

        # 4. Stage appropriateness
        stage = context.get('stage', 1)
        # Stage 1-2 should be listening, not advice
        if stage <= 2 and not any(
            word in template.lower() for word in ['coba', 'mulai', 'lakukan', 'seharusnya']
        ):
            score += self.weights['stage_appropriateness']

        return score


class ResponseLayer:
    """Individual response layer"""

    def __init__(self):
        # Layer templates mapped to emotions/contexts
        
        # EMOTIONAL ACKNOWLEDGEMENT layer
        self.acknowledgement_templates = {
            'shame': [
                "Rasa malu dengan penampilan itu emang dalam dan bisa bikin kita jadi tertutup dari orang lain.",
                "Ketika ada yang mengganggu tentang wajah atau badan kita, itu bisa jadi berat banget.",
                "Jerawat atau masalah kulit itu hal yang banyak orang alami, tapi rasanya kayak cuma kamu yang punya.",
                "Malu dengan penampilan sering bikin kita nggak mau ketemu orang, padahal itu yang bikin shame jadi lebih dalam.",
            ],
            'fear_of_abandonment': [
                "Pas orang yang biasanya perhatian tiba-tiba jadi dingin atau jarang hubungi, itu memang langsung terasa banget ya.",
                "Kalau ada perubahan dalam komunikasi, langsung terasa nggak aman.",
                "Takut kehilangan orang penting itu emang yang paling nyakitin.",
                "Pas tiba-tiba ada jarak dengan orang itu, semuanya jadi terasa beda.",
            ],
            'insecurity': [
                "Rasa nggak cukup itu emang sering muncul pas nggak percaya diri.",
                "Merasa kayak kurang dari orang lain itu emang berat.",
                "Pas percaya diri mulai goyah, semuanya jadi terasa lebih berat.",
            ],
            'emotional_exhaustion': [
                "Capek terus-terusan itu emang bukan cuma fisik, tapi juga mental.",
                "Kalau energi habis, semuanya jadi terasa penuh dan berat.",
                "Kelelahan sedalam itu memang perlu perhatian khusus.",
            ],
            'loneliness': [
                "Merasa sendiri itu emang salah satu rasa paling berat.",
                "Pas ngerasa nggak ada yang ngerti, itu bikin sepi banget.",
                "Kesepian yang dalam biasanya lebih pedih daripada cuma sedih.",
            ],
            'overthinking': [
                "Pikiran berputar terus itu emang capek, apalagi pas sendiri.",
                "Pas pikiran mulai bikin skenario yang belum tentu terjadi, emang lelah.",
                "Banyak mikir adalah bentuk khawatir yang sering nggak disadarin.",
            ],
            'grief_loss': [
                "Kehilangan emang salah satu pengalaman paling berat.",
                "Ketika sesuatu yang penting hilang, itu meninggalkan kekosongan yang dalam.",
                "Proses kehilangan memang butuh waktu untuk dipahami dan diterima.",
            ],
            'emotional_suppression': [
                "Pas terpaksa pura-pura kuat terus, itu emang berat banget secara emosional.",
                "Memendam sendiri bikin beban jadi lebih terasa.",
                "Perlu energi besar untuk terus tahan tanpa ada yang tahu.",
            ],
            'shame': [
                "Rasa malu yang dalam itu membuat kita ingin menyembunyikan diri.",
                "Ketika merasa ada yang memalukan tentang diri sendiri, itu bisa membuat kita tertutup dari orang lain.",
                "Rasa malu adalah emosi yang sering kali membuat kita terpencil dan sendiri.",
                "Malu dengan penampilan itu membuat kita merasa nggak layak untuk dilihat atau didengar.",
                "Ketika shame tentang wajah atau badan muncul, itu bisa jadi overwhelming dan bikin kita isolate.",
            ],
            'guilt': [
                "Rasa bersalah itu berat pas kamu merasa diri sendiri yang salah.",
                "Pas rasa bersalah tertanam di hati, susah untuk lepas.",
                "Rasa bersalah yang dalam bikin susah memaafkan diri sendiri.",
            ],
            'helplessness': [
                "Merasa nggak bisa apa-apa itu emang salah satu perasaan tersulit.",
                "Pas kontrol hilang, rasanya jadi sangat lemah.",
                "Rasa nggak berdaya biasanya jadi awal dari putus asa yang lebih dalam.",
            ],
            'anxiety_future': [
                "Takut tentang masa depan itu rasa yang beneran ada.",
                "Pas nggak bisa lihat jalan keluar, masa depan terasa gelap.",
                "Khawatir tentang apa yang akan datang biasanya lebih berat daripada masalah sekarang.",
            ],
            'disconnection': [
                "Merasa terputus dari orang atau kehidupan emang kesepian yang dalam.",
                "Pas koneksi putus, rasanya kayak tersesat sendiri.",
                "Rasa terpisah adalah bentuk isolasi yang paling susah diakui.",
            ],
            'emptiness': [
                "Rasa hampa itu bentuk kesedihan yang nggak punya bentuk jelas.",
                "Pas rasanya nggak ada yang berarti lagi, itu kekosongan yang dalam.",
                "Rasa hampa adalah pas segala sesuatu jadi terasa kosong.",
            ],
        }

        # STORY REFLECTION layer
        self.reflection_templates = {
            'change': [
                "Tiba-tiba ada perubahan dari orang yang penting itu memang bikin rasa nggak stabil.",
                "Ketika sesuatu yang normal berubah jadi aneh, itu langsung bikin kita khawatir.",
                "Perubahan yang besar seperti itu biasanya membuat kita mulai banyak mikir.",
            ],
            'trigger': [
                "Aksi kecil seperti itu tapi berdampak besar pada perasaan kita.",
                "Sering kali hal-hal yang terlihat sederhana itu yang paling nyakitin hati.",
                "Detail yang kecil itu sering kali menjadi pesan besar tentang perasaan.",
            ],
            'duration': [
                "Ketika sesuatu yang berat berlangsung lama, itu bisa jadi menguras habis energi.",
                "Tekanan yang terus-terusan itu lebih berbahaya daripada tekanan sesaat.",
                "Durasi juga mempengaruhi berapa dalam emosi itu berbekas.",
            ],
            'self_blame': [
                "Tapi seringkali kita salahkan diri sendiri untuk hal yang sebenarnya bukan kesalahan kita.",
                "Menyalahkan diri sendiri itu adalah cara hati kita mencari penjelasan, tapi sering kali salah sasaran.",
                "Ada kecenderungan kita untuk terima tanggung jawab yang sebenarnya bukan hak kita.",
            ],
            'physical': [
                "Emosi yang dalam itu sering kali nampak dalam bentuk fisik seperti itu.",
                "Badan kita selalu menunjukkan kondisi hati kita yang sebenarnya.",
                "Ketika emosi terganggu, yang pertama kali terserang adalah tidur dan nafsu makan.",
            ],
        };

        # IMPLIED EMOTION layer
        self.implied_templates = {
            'fear_of_abandonment': "Dari cerita kamu, kayaknya yang paling takut adalah ditinggal atau kehilangan orang itu. Itu rasa yang wajar tapi pasti berat.",
            'insecurity': "Ada rasa takut bahwa mungkin kamu nggak cukup baik untuk orang itu. Rasa itu sering muncul pas ada perubahan.",
            'emotional_dependency': "Kayaknya rasa tenang kamu sangat bergantung pada perhatian dari orang itu. Jadi setiap perubahan langsung terasa besar.",
            'anxiety_future': "Di balik semua ini, sepertinya ada rasa khawatir tentang apa yang akan terjadi selanjutnya.",
            'loneliness': "Dalam cerita ini, kayaknya kamu merasa sendirian dalam menghadapi ini. Seperti nggak ada yang benar-benar ngerti.",
        }

        # GENTLE SUPPORT layer
        self.support_templates = {
            'validation': [
                "Semua yang kamu rasain itu wajar dan normal.",
                "Apa yang kamu rasain itu benar dan layak untuk diakui.",
                "Nggak ada yang salah dengan emosi yang kamu rasakan.",
            ],
            'normalization': [
                "Apa yang kamu alami itu hal yang biasa dialami banyak orang.",
                "Ini adalah respons yang wajar terhadap situasi yang kamu hadapi.",
                "Banyak orang yang merasa sama seperti kamu dalam situasi ini.",
            ],
            'gentle_reframe': [
                "Mungkin kita bisa lihat ini dari sudut lain yang belum kita pikir.",
                "Kadang-kadang ada cara lain untuk melihat apa yang terjadi.",
                "Ada kemungkinan makna lain di balik semua ini yang belum kita lihat.",
            ],
        }


class ResponseHumanizer:
    """
    Humanize responses to feel more natural and conversational
    - Remove template feel
    - Add natural transitions
    - Vary sentence structure
    - Add empathetic markers
    - Reduce toxic/AI-sounding language
    - Maintain emotional authenticity
    """

    def __init__(self):
        # Varied empathetic starters
        self.empathetic_starters = [
            "Dari cerita kamu,",
            "Kayaknya,",
            "Aku ngerti kalau",
            "Yang aku lihat,",
            "Sepertinya,",
            "Seperti yang kamu bilang,",
            "Dengar cerita kamu,",
            "Rasanya,",
            "Di situasi kamu,",
        ]

        self.connectors = [
            "dan itu bikin",
            "yang bikin",
            ", jadi",
            ", sehingga",
            ", yang artinya",
            "- padahal",
            "tapi kayaknya",
            "dan yang lebih berat lagi",
        ]

        self.emotional_markers = [
            "memang",
            "ya",
            "tuh",
            "banget",
            "sekali",
            "sih",
            "aja",
        ]

        # Anti-patterns to remove (toxic/AI-sounding language)
        self.toxic_patterns = {
            r'\bpattern recognition\b': 'pola yang terulang',
            r'\bimplied emotion\b': 'perasaan yang tersembunyi',
            r'\brepeat.*theme': 'tema yang berulang',
            r'\bemotional dependency\b': 'attachment yang kuat',
            r'\bnormali[sz]e\b': 'acknowledge',
            r'\battachment.*style': 'cara kamu attach ke orang',
            r'\bfear of abandonment\b': 'takut ditinggal',
            r'\binsecu': 'rasa nggak cukup',
            r'\baku siap (dengarkan|mendengarkan|dengerin|kok dengarkan)\b': 'kayaknya ini penting buat kamu',
            r'\baku di sini\b': 'kayaknya kamu perlu',
            r'\bcerita (aja|kok|lagi|lebih|lebih banyak)\b': 'ada yang mau dituang',
            r'\blanjutin?(in)? (kalau|kalo) (mau|pengen)\b': 'coba share lebih',
            r'\bmau cerita (lebih|lagi)?\b': 'kayaknya ada',
            r'\baku (mendengarkan|dengarkan|kok dengarkan|mengerti kalau)\b': 'ngerti kalau',
            r'\baku (paham|ngerti)\b': 'like',
            r'\bcempal.*emosi\b': '',
            r'\bvalidasi\b': 'acknowledge',
            r'\bemosional\b': '',
            r'\bkamu tahu\b': 'kamu',
            r'\bseperti yang.*bilang': 'kayak',
            r'\bprioritize\b': 'pilih mana yang penting',
            r'\bpriority\b': 'yang penting',
            r'\bmicro-?steps?\b': 'langkah kecil',
            r'\bconsistency\b': 'rutinitas',
            r'\bcumulative effect\b': 'lama-lama',
            r'\bsignal\b': 'tanda',
            r'\blet go\b': 'lepas',
            r'\bempty cup\b': 'diri sendiri yang kosong',
            r'\bconcrete request\b': 'permintaan yang jelas',
            r'\boverwhel[m]?ing.*will pass\b': 'lama-lama akan berkurang',
            r'\bcreate routine\b': 'bikin rutinitas',
            r'\boptimize\b': 'perbaiki',
            r'\bset boundaries\b': 'buat batasan',
            r'\bstabilize emotion\b': 'tenang',
            r'\bbreakdown task\b': 'pecah jadi bagian kecil',
            r'\bpriority\b': 'yang penting',
            r'\bmicro-?steps?\b': 'langkah kecil',
            r'\bconsistency\b': 'rutinitas',
            r'\bcumulative effect\b': 'lama-lama',
            r'\bsignal\b': 'tanda',
            r'\blet go\b': 'lepas',
            r'\bempty cup\b': 'diri sendiri yang kosong',
            r'\bconcrete request\b': 'permintaan yang jelas',
            r'\boverwhel[m]?ing.*will pass\b': 'lama-lama akan berkurang',
            r'\bcreate routine\b': 'bikin rutinitas',
            r'\boptimize\b': 'perbaiki',
            r'\bset boundaries\b': 'buat batasan',
            r'\bstabilize emotion\b': 'tenang',
            r'\bbreakdown task\b': 'pecah jadi bagian kecil',
            r'\bself-?care\b': 'jaga diri sendiri',
            r'\bhealing\b': 'proses penyembuhan',
            r'\btrauma\b': 'luka',
            r'\btherapy\b': 'konseling',
            r'\bcoping mechanism\b': 'cara bertahan',
            r'\bgrounding technique\b': 'cara menenangkan diri',
            r'\bmindfulness\b': 'sadar diri',
            r'\bmeditation\b': 'meditasi',
            r'\baffirmation\b': 'pernyataan positif',
            r'\bmanifest\b': 'wujudkan',
            r'\benergy\b': 'semangat',
            r'\bvibe\b': 'suasana',
            r'\btoxic\b': 'beracun',
            r'\bburned out\b': 'capek total',
            r'\bmental breakdown\b': 'mental yang hancur',
            r'\binsecure\b': 'nggak percaya diri',
            r'\btherapist\b': 'konselor',
            r'\bcoach\b': 'pelatih',
            r'\bjournal\b': 'tulis',
            r'\bprocess\b': 'proses',
            r'\bwork through\b': 'hadapi',
            r'\binner child\b': 'diri kecil kamu',
            r'\binner voice\b': 'suara dalam hati',
            r'\bself-?love\b': 'cinta diri sendiri',
            r'\bself-?worth\b': 'nilai diri',
            r'\bself-?esteem\b': 'percaya diri',
            r'\bself-?doubt\b': 'ragu sama diri sendiri',
            r'\bself-?blame\b': 'salahkan diri sendiri',
            r'\bself-?sabotage\b': 'sabotase diri sendiri',
            r'\bself-?compassion\b': 'belas kasih ke diri sendiri',
            r'\bself-?awareness\b': 'sadar diri',
            r'\bself-?improvement\b': 'perbaikan diri',
            r'\bpersonal growth\b': 'pertumbuhan pribadi',
            r'\bpersonal development\b': 'pengembangan diri',
            r'\bself-?actualization\b': 'aktualisasi diri',
            r'\bpotential\b': 'potensi',
            r'\bfulfillment\b': 'kepuasan',
            r'\bpurpose\b': 'tujuan',
            r'\bmeaning\b': 'makna',
            r'\bpassion\b': 'gairah',
            r'\bdream\b': 'impian',
            r'\bgoal\b': 'tujuan',
            r'\bvision\b': 'visi',
            r'\bmission\b': 'misi',
            r'\bsuccess\b': 'kesuksesan',
            r'\bfailure\b': 'kegagalan',
            r'\bsucceeded?\b': 'berhasil',
            r'\bfailed?\b': 'gagal',
            r'\bwin\b': 'menang',
            r'\blose\b': 'kalah',
            r'\bvictory\b': 'kemenangan',
            r'\bdefeat\b': 'kekalahan',
            r'\bchampion\b': 'juara',
            r'\bwarrior\b': 'prajurit',
            r'\bfighter\b': 'pejuang',
            r'\bstrong\b': 'kuat',
            r'\bweak\b': 'lemah',
            r'\bpowerful\b': 'kuat',
            r'\bpowerless\b': 'tidak berdaya',
            r'\bempowered?\b': 'diberdayakan',
            r'\bempowerment\b': 'pemberdayaan',
            r'\bconfident\b': 'percaya diri',
            r'\bconfidence\b': 'percaya diri',
            r'\bsecure\b': 'aman',
            r'\bsecurity\b': 'keamanan',
            r'\bsafe\b': 'aman',
            r'\bsafety\b': 'keamanan',
            r'\bvulnerable\b': 'rentan',
            r'\bvulnerability\b': 'kerentanan',
            r'\bopen\b': 'terbuka',
            r'\bopeness\b': 'keterbukaan',
            r'\bclose\b': 'tertutup',
            r'\bclosure\b': 'penutupan',
            r'\baccept\b': 'terima',
            r'\bacceptance\b': 'penerimaan',
            r'\breject\b': 'tolak',
            r'\brejection\b': 'penolakan',
            r'\bapprove\b': 'setujui',
            r'\bapproval\b': 'persetujuan',
            r'\bdisapprove\b': 'tidak setujui',
            r'\bdisapproval\b': 'ketidaksetujuan',
            r'\bjudge\b': 'nilai',
            r'\bjudgment\b': 'penilaian',
            r'\bcritique\b': 'kritik',
            r'\bcritical\b': 'kritis',
            r'\bpraise\b': 'pujian',
            r'\bblame\b': 'salahkan',
            r'\bforgive\b': 'maafkan',
            r'\bforgiveness\b': 'pengampunan',
            r'\bregret\b': 'penyesalan',
            r'\bremorse\b': 'penyesalan',
            r'\bguilt\b': 'rasa bersalah',
            r'\bshame\b': 'rasa malu',
            r'\bembarrassment\b': 'rasa malu',
            r'\bhumiliation\b': 'penghinaan',
            r'\bhumiliate\b': 'hinakan',
            r'\bhumble\b': 'rendah hati',
            r'\bhumility\b': 'kerendahan hati',
            r'\bpride\b': 'kebanggaan',
            r'\bproud\b': 'bangga',
            r'\barrogance\b': 'kesombongan',
            r'\barrogant\b': 'sombong',
            r'\bhumble\b': 'rendah hati',
            r'\bmodest\b': 'sederhana',
            r'\bmodesty\b': 'kesederhanaan',
            r'\bvain\b': 'percaya diri berlebihan',
            r'\bvanity\b': 'kesombongan',
            r'\bego\b': 'ego',
            r'\begotistical\b': 'egois',
            r'\bselfish\b': 'egois',
            r'\bselfishness\b': 'keegoisannya',
            r'\bgenerous\b': 'murah hati',
            r'\bgenerosity\b': 'kemurahan hati',
            r'\bkind\b': 'baik',
            r'\bkindness\b': 'kebaikan',
            r'\bcruel\b': 'kejam',
            r'\bcruelty\b': 'kekejaman',
            r'\bcompassion\b': 'belas kasih',
            r'\bcompassionate\b': 'penuh belas kasih',
            r'\bempathy\b': 'empati',
            r'\bempathetic\b': 'empatik',
            r'\bsympathy\b': 'simpati',
            r'\bsympathetic\b': 'simpatik',
            r'\bunderstand\b': 'mengerti',
            r'\bunderstanding\b': 'pemahaman',
            r'\bmisunderstand\b': 'salah mengerti',
            r'\bmisunderstanding\b': 'kesalahpahaman',
            r'\bcommunicate\b': 'komunikasi',
            r'\bcommunication\b': 'komunikasi',
            r'\bexpress\b': 'ungkapkan',
            r'\bexpression\b': 'ungkapan',
            r'\bshare\b': 'bagikan',
            r'\blisten\b': 'dengarkan',
            r'\blistening\b': 'mendengarkan',
            r'\bhear\b': 'dengar',
            r'\bheard\b': 'didengar',
            r'\bspeak\b': 'bicara',
            r'\bspeech\b': 'pidato',
            r'\btalk\b': 'bicara',
            r'\bconversation\b': 'percakapan',
            r'\bdialogue\b': 'dialog',
            r'\bdiscuss\b': 'diskusi',
            r'\bdiscussion\b': 'diskusi',
            r'\bdebate\b': 'perdebatan',
            r'\bargue\b': 'bertengkar',
            r'\bargument\b': 'pertengkaran',
            r'\bconflict\b': 'konflik',
            r'\bconflicting\b': 'bertentangan',
            r'\bresolve\b': 'selesaikan',
            r'\bresolution\b': 'penyelesaian',
            r'\bcompromise\b': 'kompromi',
            r'\bagreement\b': 'kesepakatan',
            r'\bdisagreement\b': 'ketidaksepakatan',
            r'\bharmony\b': 'harmoni',
            r'\bharmonious\b': 'harmonis',
            r'\bdisharmony\b': 'ketidakharmonisan',
            r'\bpeace\b': 'kedamaian',
            r'\bpeaceful\b': 'damai',
            r'\bwar\b': 'perang',
            r'\bfight\b': 'pertarungan',
            r'\bbattle\b': 'pertempuran',
            r'\bstruggle\b': 'perjuangan',
            r'\bstruggling\b': 'berjuang',
            r'\bstruggled\b': 'berjuang',
            r'\bsuffer\b': 'menderita',
            r'\bsuffering\b': 'penderitaan',
            r'\bpain\b': 'rasa sakit',
            r'\bpainful\b': 'menyakitkan',
            r'\bache\b': 'nyeri',
            r'\bache\b': 'nyeri',
            r'\bhurt\b': 'sakit',
            r'\bhurting\b': 'menyakiti',
            r'\bwound\b': 'luka',
            r'\bwounded\b': 'terluka',
            r'\bscar\b': 'bekas luka',
            r'\bscared\b': 'takut',
            r'\bscary\b': 'menakutkan',
            r'\bfear\b': 'takut',
            r'\bfearful\b': 'penuh ketakutan',
            r'\bafraid\b': 'takut',
            r'\bterror\b': 'teror',
            r'\bterrified\b': 'ketakutan',
            r'\bterrifying\b': 'menakutkan',
            r'\bworry\b': 'khawatir',
            r'\bworried\b': 'khawatir',
            r'\bworrying\b': 'mengkhawatirkan',
            r'\banxious\b': 'cemas',
            r'\banxiety\b': 'kecemasan',
            r'\bstress\b': 'stress',
            r'\bstressed\b': 'stress',
            r'\bstressful\b': 'penuh stress',
            r'\btense\b': 'tegang',
            r'\btension\b': 'ketegangan',
            r'\brelax\b': 'santai',
            r'\brelaxed\b': 'santai',
            r'\brelaxation\b': 'relaksasi',
            r'\bcalm\b': 'tenang',
            r'\bcalming\b': 'menenangkan',
            r'\bpeace\b': 'kedamaian',
            r'\bpeaceful\b': 'damai',
            r'\bquiet\b': 'sunyi',
            r'\bsilence\b': 'kesunyian',
            r'\bsilent\b': 'senyap',
            r'\bloud\b': 'keras',
            r'\bnoise\b': 'kebisingan',
            r'\bnoisy\b': 'bising',
            r'\bsound\b': 'suara',
            r'\bsounds?\b': 'suara',
            r'\bmusic\b': 'musik',
            r'\bsong\b': 'lagu',
            r'\bsing\b': 'nyanyikan',
            r'\bsinging\b': 'bernyanyi',
            r'\bsang\b': 'bernyanyi',
            r'\bdance\b': 'tari',
            r'\bdancing\b': 'menari',
            r'\bdanced\b': 'menari',
            r'\bmovement\b': 'gerakan',
            r'\bmove\b': 'bergerak',
            r'\bmoving\b': 'bergerak',
            r'\bmoved\b': 'bergerak',
            r'\bstill\b': 'diam',
            r'\bstatic\b': 'statis',
            r'\bmotion\b': 'gerakan',
            r'\baction\b': 'tindakan',
            r'\bactive\b': 'aktif',
            r'\bactivity\b': 'aktivitas',
            r'\bpassive\b': 'pasif',
            r'\bpassivity\b': 'kepassifan',
            r'\brest\b': 'istirahat',
            r'\bresting\b': 'beristirahat',
            r'\brested\b': 'beristirahat',
            r'\bsleep\b': 'tidur',
            r'\bsleeping\b': 'tidur',
            r'\bslept\b': 'tidur',
            r'\bawake\b': 'bangun',
            r'\bawaken\b': 'bangunkan',
            r'\bawakening\b': 'kebangkitan',
            r'\bawakened\b': 'terbangun',
            r'\bdream\b': 'mimpi',
            r'\bdreaming\b': 'bermimpi',
            r'\bdreamed\b': 'bermimpi',
            r'\bdreamt\b': 'bermimpi',
            r'\bnightmare\b': 'mimpi buruk',
            r'\bwake\b': 'bangun',
            r'\bwaking\b': 'bangun',
            r'\bwoke\b': 'bangun',
            r'\bwoken\b': 'terbangun',
            r'\beye\b': 'mata',
            r'\beyes\b': 'mata',
            r'\bsee\b': 'lihat',
            r'\bseeing\b': 'melihat',
            r'\bseen\b': 'dilihat',
            r'\bsaw\b': 'melihat',
            r'\bsight\b': 'penglihatan',
            r'\bblind\b': 'buta',
            r'\bblindness\b': 'kebutaan',
            r'\bvisible\b': 'terlihat',
            r'\binvisible\b': 'tidak terlihat',
            r'\bvisibility\b': 'visibilitas',
            r'\bvision\b': 'visi',
            r'\bview\b': 'pandangan',
            r'\bperspective\b': 'perspektif',
            r'\bfocus\b': 'fokus',
            r'\bfocused\b': 'fokus',
            r'\bfocusing\b': 'fokus',
            r'\bfocused\b': 'fokus',
            r'\bblur\b': 'buram',
            r'\bblurred\b': 'buram',
            r'\bblurry\b': 'buram',
            r'\bclear\b': 'jelas',
            r'\bclarity\b': 'kejelasan',
            r'\bconfusion\b': 'kebingungan',
            r'\bconfused\b': 'bingung',
            r'\bconfusing\b': 'membingungkan',
            r'\bconfuse\b': 'bingungkan',
            r'\bunderstand\b': 'mengerti',
            r'\bunderstanding\b': 'pemahaman',
            r'\bunderstandable\b': 'dapat dimengerti',
            r'\bcomprehend\b': 'pahami',
            r'\bcomprehension\b': 'pemahaman',
            r'\bcomprehensible\b': 'dapat dipahami',
            r'\bgrasp\b': 'pahami',
            r'\bgrasping\b': 'memahami',
            r'\bgrasped\b': 'memahami',
            r'\bknow\b': 'tahu',
            r'\bknowing\b': 'mengetahui',
            r'\bknown\b': 'diketahui',
            r'\bknew\b': 'tahu',
            r'\bknowledge\b': 'pengetahuan',
            r'\bknowledgeable\b': 'berpengetahuan',
            r'\bignore\b': 'abaikan',
            r'\bignoring\b': 'mengabaikan',
            r'\bignored\b': 'diabaikan'
        } 

    def humanize(self, response: str, stage: int) -> str:
        """Apply humanization techniques to response"""
        if not response:
            return response

        # 1. Remove toxic/AI-sounding patterns
        response = self._remove_toxic_patterns(response)

        # 2. Fix repetitive patterns
        response = self._reduce_repetition(response)

        # 3. Improve flow between sentences
        response = self._improve_flow(response)

        # 4. Add natural markers based on stage
        if stage == 1:
            response = self._add_listening_tone(response)
        elif stage == 2:
            response = self._add_understanding_tone(response)
        elif stage == 3:
            response = self._add_insight_tone(response)
        else:
            response = self._add_support_tone(response)

        # 5. Final polish
        response = self._final_polish(response)

        return response

    def _remove_toxic_patterns(self, text: str) -> str:
        """Remove AI-sounding, overly formal language"""
        for pattern, replacement in self.toxic_patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _reduce_repetition(self, text: str) -> str:
        """Remove overly repetitive words/patterns"""
        # Remove double spaces
        text = re.sub(r' +', ' ', text)
        
        # Reduce "dari cerita kamu" - appears too much
        count_dari = text.count('Dari cerita kamu')
        if count_dari > 1:
            lines = text.split('\n')
            new_lines = []
            dari_count = 0
            for line in lines:
                if 'Dari cerita kamu' in line and dari_count > 0:
                    # Replace with variation
                    line = line.replace('Dari cerita kamu', 'Kayaknya')
                elif 'Dari cerita kamu' in line:
                    dari_count += 1
                new_lines.append(line)
            text = '\n'.join(new_lines)
        
        # Reduce "kayaknya" repetition
        if text.count('kayaknya') > 2:
            text = re.sub(r'kayaknya.*?\.', lambda m: self._vary_kayaknya(m.group(0)), text)
        
        # Vary "itu" usage
        words = text.split()
        new_words = []
        for i, word in enumerate(words):
            if word == "itu" and i > 0 and words[i-1] == "itu":
                # Replace second "itu" with variation
                new_words.append(random.choice(["hal ini", "kondisi ini", "situasi ini", "keadaan ini"]))
            else:
                new_words.append(word)
        
        return " ".join(new_words)

    def _vary_kayaknya(self, text: str) -> str:
        """Vary kayaknya usage"""
        variations = [
            "Sepertinya",
            "Rasanya",
            "Mungkin",
            "Kayaknya",
        ]
        return text.replace('kayaknya', random.choice(variations), 1)

    def _improve_flow(self, text: str) -> str:
        """Improve flow between sentences"""
        # Add natural connectors between separate thoughts
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) > 1:
            improved = [sentences[0]]
            for sent in sentences[1:]:
                # Check if connector needed
                if sent and sent[0].isupper() and not any(
                    sent.startswith(word) for word in 
                    ['Dan', 'Tapi', 'Atau', 'Jadi', 'Oleh karena', 'Kayaknya', 'Rasanya', 'Sepertinya']
                ):
                    # Maybe add subtle connector
                    if random.random() > 0.5:
                        improved.append(sent)
                    else:
                        improved.append(sent)
                else:
                    improved.append(sent)
            
            return " ".join(improved)
        
        return text

    def _add_listening_tone(self, text: str) -> str:
        """Add empathetic listening tone (Stage 1)"""
        # Replace any "solution" words with listening words
        text = text.replace("coba", "kayaknya")
        text = text.replace("seharusnya", "seperti")
        
        # Add emphasis to emotions naturally (less frequent)
        text = re.sub(
            r'\b(capek|sedih|takut|kesepian|nggak enak)\b(?! banget)',
            r'\1 banget',
            text
        )
        
        return text

    def _add_understanding_tone(self, text: str) -> str:
        """Add understanding/reflection tone (Stage 2)"""
        # Don't overuse "dari cerita kamu"
        if text.count("Dari cerita kamu") == 1:
            # Keep first instance
            pass
        
        return text

    def _add_insight_tone(self, text: str) -> str:
        """Add insight tone (Stage 3)"""
        # Add phrases that show deeper understanding naturally
        if "sering kali" not in text:
            text = re.sub(
                r'\bmemang\b',
                'memang sering kali',
                text,
                count=1  # Only first occurrence
            )
        
        return text

    def _add_support_tone(self, text: str) -> str:
        """Add supportive tone (Stage 4)"""
        # Add empowering language naturally
        text = re.sub(r'\bbisa\b', 'bisa kok', text, count=1)
        
        return text

    def _final_polish(self, text: str) -> str:
        """Final polish for naturalness"""
        # Ensure proper spacing around punctuation
        text = re.sub(r'\s+([,.!?])', r'\1', text)
        
        # Remove leading spaces
        text = text.lstrip()
        
        # Ensure ends with period if it doesn't have punctuation
        if text and text[-1] not in '.!?':
            text += '.'
        
        # Remove excessive exclamation marks or question marks
        text = re.sub(r'([!?]){2,}', r'\1', text)
        
        return text


class DynamicResponseBuilder:
    """Build contextual, layered responses"""

    def __init__(self):
        self.layer = ResponseLayer()
        self.emotion_detector = MicroEmotionDetector()
        self.detail_extractor = DetailExtractor()
        self.intent_detector = IntentDetector()
        self.advice_builder = AdviceSupportBuilder()
        self.weight_selector = ResponseWeightSelector()
        self.humanizer = ResponseHumanizer()
        # NEW: Universal engines untuk fallback dan emotional reflection
        self.emotional_reflection_engine = UniversalEmotionalReflectionEngine()
        self.topic_mapper = TopicEmotionMapper()

    def build_response(
        self,
        user_message: str,
        emotional_memory: EmotionalMemory,
        stage: int
    ) -> str:
        """Build complete response using multiple layers"""

        # 1. Detect micro emotions
        emotions = self.emotion_detector.get_dominant_emotions(user_message)
        implied_emotions = self.emotion_detector.get_implied_emotions(user_message)

        # 2. Extract details
        details = self.detail_extractor.extract_details(user_message)
        keywords = self.detail_extractor.get_key_words(user_message)

        # 3. CRITICAL: Detect user's intent
        intent_scores = self.intent_detector.detect_intent(user_message)
        primary_intent, intent_confidence = self.intent_detector.get_primary_intent(user_message)

        # 4. CHECK: If user is asking for advice, use specialized builder or internal method
        if self.intent_detector.has_advice_request(user_message) and primary_intent == 'advice_seeking':
            primary_emotion = emotions[0][0] if emotions else None
            
            # Get previous topic context from emotional_memory
            previous_topic = None
            if emotional_memory and emotional_memory.message_history:
                # Get the last message's emotions to understand the topic
                for prev_msg in reversed(emotional_memory.message_history):
                    if prev_msg.get('emotions'):
                        prev_emotions = prev_msg['emotions']
                        if prev_emotions:
                            previous_topic = prev_emotions[0][0]  # Get primary emotion from previous message
                        break
            
            try:
                response = self.advice_builder.build_advice_response(
                    user_message, 
                    primary_emotion=primary_emotion,
                    primary_intent=primary_intent,
                    previous_topic=previous_topic
                )
            except:
                # Fallback ke internal advice handler jika advice_builder fail
                response = self._build_advice_response(user_message, emotions, details, keywords)
            response = self.humanizer.humanize(response, stage)
            return response

        # 5. Build response based on stage
        if stage == 1:
            response = self._build_stage1_response(
                user_message, emotions, details, keywords, primary_intent
            )
        elif stage == 2:
            response = self._build_stage2_response(
                user_message, emotions, implied_emotions, details, keywords, primary_intent
            )
        elif stage == 3:
            response = self._build_stage3_response(
                user_message, emotions, implied_emotions, details, keywords, emotional_memory, primary_intent
            )
        else:  # stage 4
            response = self._build_stage4_response(
                user_message, emotions, implied_emotions, details, emotional_memory, primary_intent
            )

        # 6. Humanize response (final layer)
        response = self.humanizer.humanize(response, stage)

        return response

    def _build_advice_response(
        self,
        user_message: str,
        emotions: List[Tuple],
        details: Dict,
        keywords: List[str]
    ) -> str:
        """
        Internal advice response handler - natural Indonesian.
        
        Format:
        1. Validasi emosi
        2. Insight sederhana
        3. Langkah kecil realistis
        4. Penutup suportif
        """
        lines = []
        
        # 1. VALIDASI EMOSI
        if emotions:
            emotion_name, _ = emotions[0]
            if emotion_name in self.layer.acknowledgement_templates:
                validation = random.choice(self.layer.acknowledgement_templates[emotion_name])
                lines.append(validation)
        else:
            reflection = self.emotional_reflection_engine.generate_reflection(user_message, emotions)
            lines.append(reflection)
        
        # 2. INSIGHT SEDERHANA - natural Indonesian
        insight = self._generate_advice_insight(keywords, user_message)
        if insight:
            lines.append(f"\n\n{insight}")
        
        # 3. LANGKAH KECIL REALISTIS
        steps = self._generate_practical_steps(keywords, emotion_name if emotions else 'uncertainty')
        if steps:
            lines.append(f"\n\n{steps}")
        
        # 4. PENUTUP SUPORTIF
        closing = self._generate_supportive_closing(keywords, emotion_name if emotions else 'uncertainty')
        if closing:
            lines.append(f"\n\n{closing}")
        
        response = "".join(lines).strip()
        return response if response else self._generate_universal_fallback(user_message)
    
    def _generate_advice_insight(self, keywords: List[str], user_message: str) -> str:
        """Generate simple, reassuring insight in natural Indonesian"""
        insights = {
            'pressure': "Yang bikin makin berat bukan cuma tantangannya, tapi karena kamu merasa harus segera selesaikan semuanya sendiri.",
            'anxiety': "Yang bikin capek mungkin bukan cuma masalahnya, tapi karena kepala terus memikirkan semua kemungkinan buruk.",
            'future': "Takut tentang masa depan itu wajar, tapi sering kali kita sudah bayangkan hal-hal yang belum tentu terjadi.",
            'exhaustion': "Ketika sudah capek, yang perlu bukan tambahan tugas, tapi waktu untuk istirahat dan tenang.",
            'failure': "Banyak orang juga khawatir gagal, dan itu nggak berarti kamu nggak mampu.",
            'loneliness': "Perasaan sendirian biasanya bikin beban terasa lebih berat.",
            'change': "Perubahan memang bikin nggak nyaman, tapi di hidup nggak ada yang tetap.",
            'insecurity': "Rasa nggak cukup itu biasanya bikin kita jadi keras ke diri sendiri, padahal kita udah cukup.",
            'comparison': "Kalau terus bandingin diri sama orang lain, lama-lama kita lupa kalau setiap orang punya cerita sendiri.",
            'overthinking': "Pikiran yang terus berputar itu emang capek, apalagi kalau sendiri terus.",
            'burnout': "Capek terus-terusan itu bukan cuma fisik, tapi juga mental yang udah habis energinya.",
            'shame': "Rasa malu yang dalam itu bikin kita pengen sembunyi, padahal yang kita pikir memalukan sebenarnya lebih normal.",
            'guilt': "Rasa bersalah itu berat, tapi sering kali kita terlalu keras menghukum diri sendiri.",
            'relationship': "Kalau ada perubahan dalam hubungan, langsung terasa nggak aman. Itu wajar kok.",
            'body_image': "Insecure soal penampilan memang gampang bikin kita jadi keras ke diri sendiri.",
        }
        
        # Match keywords dengan insights
        for keyword in keywords:
            for key, value in insights.items():
                if keyword.lower() in key.lower():
                    return value
        
        # Default insight
        return "Yang paling melelahkan biasanya bukan cuma situasinya, tapi karena kamu hadapin sendiri tanpa ada yang dengarkan."
    
    def _generate_practical_steps(self, keywords: List[str], emotion: str) -> str:
        """Generate realistic small steps in natural Indonesian"""
        steps_map = {
            'pressure': "Daripada maksa selesaiin semuanya, coba fokus ke satu hal kecil dulu. Cukup selesain itu aja dulu.",
            'anxiety': "Pas pikiran berputar terus, coba tulis aja pikiran-pikiran itu. Lihat mana yang bener-bener bisa terjadi, mana yang cuma khayalan.",
            'exhaustion': "Kalau udah capek, istirahat dulu aja. Istirahat itu bagian dari proses, bukan kemalasan.",
            'failure': "Mulai dari hal kecil, raih kemenangan kecil dulu. Dari situ percaya diri mulai tumbuh.",
            'loneliness': "Cerita ke satu orang yang kamu percaya. Nggak harus ke semua orang, satu aja cukup.",
            'relationship': "Coba bicara langsung tentang apa yang kamu rasain. Orang nggak bisa baca pikiran.",
            'shame': "Yang kamu pikir paling memalukan, sebenarnya lebih normal. Banyak orang juga pernah.",
            'insecurity': "Pelan-pelan mulai kurangin kebiasaan ngomong buruk ke diri sendiri dulu aja. Nggak harus langsung percaya diri penuh.",
            'comparison': "Coba kurangin waktu liat orang lain dulu. Fokus ke diri sendiri aja, lihat apa yang udah kamu capai.",
            'overthinking': "Pas kepala penuh, coba lakukan sesuatu yang bikin tangan dan pikiran sibuk. Kadang itu bikin kepala sedikit lebih tenang.",
            'burnout': "Nggak perlu langsung besar-besaran. Mulai dari istirahat yang bener dulu, tidur yang cukup, makan yang teratur.",
            'body_image': "Nggak harus langsung maksa diri percaya diri. Tapi pelan-pelan mulai appreciate hal-hal kecil dari tubuh kamu.",
            'guilt': "Coba terima kalau kamu udah melakukan yang terbaik dengan kondisi yang kamu punya saat itu.",
            'future': "Nggak perlu mikirin semuanya sekarang. Fokus ke apa yang bisa kamu lakukan hari ini aja.",
        }
        
        # Match dengan emotion atau keywords
        for key, step in steps_map.items():
            if key in emotion or any(kw.lower() in key for kw in keywords):
                return step
        
        # Default steps
        return "Coba mulai dari hal kecil dulu. Nggak perlu langsung besar-besaran."
    
    def _generate_supportive_closing(self, keywords: List[str], emotion: str) -> str:
        """Generate supportive, encouraging closing in natural Indonesian"""
        closings = [
            "Pelan-pelan aja, nggak ada yang instant.",
            "Kamu nggak sendiri dalam hal gini, banyak orang juga ngalamin.",
            "Coba aja dulu, nggak perlu langsung sempurna.",
            "Kalau masih berat, itu wajar kok.",
            "Percaya diri memang dibangun pelan-pelan.",
            "Langkah kecil juga tetap maju.",
            "Jangan terlalu keras ke diri sendiri.",
            "Ada aja caranya, cuma memang butuh waktu.",
            "Seenggaknya sampai hari ini kamu masih bertahan, itu udah cukup.",
            "Nggak perlu langsung berubah total. Perubahan kecil juga berarti.",
            "Kalau hari ini berat, besok bisa jadi lebih ringan.",
            "Kamu udah cukup, serius.",
            "Nggak ada yang salah dengan kamu.",
            "Proses itu memang nggak linear, dan itu normal.",
            "Kadang yang paling penting adalah kamu tetap coba.",
        ]
        return random.choice(closings)


    def _build_stage1_response(
        self,
        user_message: str,
        emotions: List[Tuple],
        details: Dict,
        keywords: List[str],
        primary_intent: Optional[str] = None
    ) -> str:
        """Stage 1: Listening Phase - Focus on emotional acknowledgement and reflection (REVISED: Less asking, more understanding)"""

        lines = []

        # Get dominant emotion
        context = {
            'emotions': emotions,
            'details': details,
            'stage': 1,
        }

        # PRIMARY: Emotional acknowledgement based on detected emotion
        if emotions:
            emotion_name, _ = emotions[0]

            # Use weighted selection for acknowledgement
            if emotion_name in self.layer.acknowledgement_templates:
                templates = self.layer.acknowledgement_templates[emotion_name]
                acknowledgement = self.weight_selector.select_weighted(
                    templates, context
                )
                lines.append(acknowledgement)
        else:
            # Fallback: Use emotional reflection engine jika emotion tidak terdeteksi
            reflection = self.emotional_reflection_engine.generate_reflection(user_message, emotions)
            lines.append(reflection)

        # SECONDARY: Add reflective element with detail mentions
        reflection = self._build_reflection_with_details(
            user_message, keywords, details
        )
        if reflection:
            lines.append(f"\n{reflection}")

        # TERTIARY: Gentle follow-up - REDUCED generic asking
        # Only add jika really needed (very short messages atau unclear sentiment)
        message_length = len(user_message.split())
        if message_length < 8:
            follow_ups = [
                # REVISED: Less "cerita lagi", more emotional validation
                "\n\nAda yang ingin kamu ungkapin lebih dari ini?",
                "\n\nRasanya ada lebih banyak yang ingin keluar dari hati kamu.",
                "\n\nPelan-pelan saja, kayaknya ada yang perlu kamu keluarkan.",
                # Maksimal 3 follow-up yang lebih natural
            ]
            if follow_ups:
                lines.append(random.choice(follow_ups))

        # SAFETY CHECK: Universal fallback if response is empty
        response = "".join(lines).strip()
        if not response:
            response = self._generate_universal_fallback(user_message)
        
        return response

    def _build_story_reflection_detailed(
        self,
        user_message: str,
        keywords: List[str],
        emotions: List[Tuple],
        implied_emotions: List[str]
    ) -> str:
        """Build detailed story reflection that mentions specific elements"""
        
        parts = []
        
        # Mention the main emotion + detail
        if emotions:
            main_emotion = emotions[0][0]
            
            # Add specific context
            if 'change' in keywords:
                parts.append("ada perubahan yang terasa dalam situasi kamu")
            elif 'fear' in keywords:
                parts.append("ada rasa takut yang memberat")
            elif 'exhaustion' in keywords:
                parts.append("ada kelelahan yang dalam")
            elif 'loneliness' in keywords:
                parts.append("ada kesepian yang terasa")
            else:
                parts.append(f"ada rasa {main_emotion.replace('_', ' ')} yang terasa")
        
        # Add implied emotion insight
        if implied_emotions:
            implied = implied_emotions[0].replace('_', ' ')
            parts.append(f"dan di balik itu sepertinya ada {implied}")
        
        # Connect to their story
        if parts:
            return f"Dari cerita kamu, {' yang mungkin bikin '.join(parts)}."
        
        return None

    def _build_reflection_with_details(
        self,
        user_message: str,
        keywords: List[str],
        details: Dict
    ) -> str:
        """Build reflection that mentions specific details from user's message"""
        
        detail_mentions = []
        
        # Extract actual phrases from message that show emotion
        if 'change' in keywords or 'berubah' in user_message.lower():
            detail_mentions.append("ada perubahan yang terasa")
        
        if 'fear' in keywords or 'takut' in user_message.lower():
            detail_mentions.append("ada rasa takut")
        
        if 'exhaustion' in keywords or 'capek' in user_message.lower():
            detail_mentions.append("capek terus-terusan")
        
        if detail_mentions:
            detail_str = " dan ".join(detail_mentions)
            return f"Dari cerita kamu, kayaknya {detail_str} bikin semuanya terasa berat."
        
        return None

    def _build_stage2_response(
        self,
        user_message: str,
        emotions: List[Tuple],
        implied_emotions: List[str],
        details: Dict,
        keywords: List[str],
        primary_intent: Optional[str] = None
    ) -> str:
        """Stage 2: Understanding Phase - Deeper reflection + emotional insight (REVISED: More reflection, strategic asking)"""

        lines = []
        
        context = {
            'emotions': emotions,
            'details': details,
            'stage': 2,
        }

        # PRIMARY ACKNOWLEDGEMENT: with specific detail or emotional reflection
        if emotions:
            emotion_name, _ = emotions[0]
            if emotion_name in self.layer.acknowledgement_templates:
                templates = self.layer.acknowledgement_templates[emotion_name]
                ack = self.weight_selector.select_weighted(templates, context)
                lines.append(ack)
        else:
            # Fallback: emotional reflection jika emotion tidak terdeteksi
            reflection = self.emotional_reflection_engine.generate_reflection(user_message, emotions)
            lines.append(reflection)

        # SECONDARY: Build deeper story reflection with details
        story_reflection = self._build_story_reflection_detailed(
            user_message, keywords, emotions, implied_emotions
        )
        if story_reflection:
            lines.append(f"\n{story_reflection}")

        # TERTIARY: Add implied emotion insight jika ada
        if implied_emotions and implied_emotions[0] in self.layer.implied_templates:
            implied_insight = self.layer.implied_templates[implied_emotions[0]]
            lines.append(f"\n\n{implied_insight}")

        # QUATERNARY: Strategic deepening question (NOT always)
        # Only ask jika benar-benar ada clue untuk ditanya
        question = self._generate_deepening_question(
            keywords, emotions, user_message, details
        )
        # REDUCED: Only add question 60% of the time
        if question and random.random() < 0.6:
            lines.append(f"\n\n{question}")

        # SAFETY CHECK: Universal fallback if response is empty
        response = "".join(lines).strip()
        if not response:
            response = self._generate_universal_fallback(user_message)
        
        return response

    def _build_stage3_response(
        self,
        user_message: str,
        emotions: List[Tuple],
        implied_emotions: List[str],
        details: Dict,
        keywords: List[str],
        emotional_memory: EmotionalMemory,
        primary_intent: Optional[str] = None
    ) -> str:
        """Stage 3: Insight Phase - Deeper emotional insights + validation (REVISED: More insight, less asking)"""

        lines = []

        # PRIMARY ACKNOWLEDGEMENT: with emotional depth
        if emotions:
            emotion_name, _ = emotions[0]
            if emotion_name in self.layer.acknowledgement_templates:
                ack = self._pick_random(
                    self.layer.acknowledgement_templates[emotion_name]
                )
                lines.append(ack)
        else:
            # Fallback: emotional reflection jika emotion tidak terdeteksi
            reflection = self.emotional_reflection_engine.generate_reflection(user_message, emotions)
            lines.append(reflection)

        # SECONDARY: Story reflection with more depth
        lines.append("\n" + self._build_story_summary(keywords, user_message))

        # TERTIARY: Implied emotion - deeper insight
        if implied_emotions and implied_emotions[0] in self.layer.implied_templates:
            implied = self.layer.implied_templates[implied_emotions[0]]
            lines.append(f"\n\n{implied}")

        # QUATERNARY: Validation and insight together (NOT separated)
        validation = self._pick_random(self.layer.support_templates['validation'])
        lines.append(f"\n\n{validation}")

        # OPTIONAL: Gentle question (50% probability - be more selective)
        question = self._generate_insight_question(emotions, keywords)
        if question and random.random() < 0.5:
            lines.append(f"\n\n{question}")

        # SAFETY CHECK: Universal fallback if response is empty
        response = "".join(lines).strip()
        if not response:
            response = self._generate_universal_fallback(user_message)
        
        return response

    def _build_stage4_response(
        self,
        user_message: str,
        emotions: List[Tuple],
        implied_emotions: List[str],
        details: Dict,
        emotional_memory: EmotionalMemory,
        primary_intent: Optional[str] = None
    ) -> str:
        """Stage 4: Support Phase - Insights + gentle support + soft guidance (REVISED: Focus on patterns and reframes)"""

        lines = []

        # PRIMARY ACKNOWLEDGEMENT: Deep emotional understanding
        if emotions:
            emotion_name, _ = emotions[0]
            if emotion_name in self.layer.acknowledgement_templates:
                ack = self._pick_random(
                    self.layer.acknowledgement_templates[emotion_name]
                )
                lines.append(ack)
        else:
            # Fallback: emotional reflection
            reflection = self.emotional_reflection_engine.generate_reflection(user_message, emotions)
            lines.append(reflection)

        # SECONDARY: Pattern recognition from memory (if available)
        profile = emotional_memory.get_emotional_profile()
        if profile['repeated_themes']:
            theme = profile['repeated_themes'][0]
            # HUMANIZED: Less technical, more conversational
            pattern_msg = f"\nDari cerita-cerita kamu, terlihat bahwa {theme} ini adalah hal yang terus terulang dalam pikiran kamu."
            lines.append(pattern_msg)

        # TERTIARY: Implied emotions insight
        if implied_emotions:
            implied = implied_emotions[0]
            if implied in self.layer.implied_templates:
                lines.append(f"\n\n{self.layer.implied_templates[implied]}")

        # QUATERNARY: Validation (simplified, more natural)
        validation = self._pick_random(self.layer.support_templates['validation'])
        lines.append(f"\n\n{validation}")

        # QUINARY: Gentle reframe
        reframe = self._pick_random(self.layer.support_templates['gentle_reframe'])
        lines.append(f"\n\n{reframe}")

        # SENARY: Support action (if applicable)
        support = self._generate_support_action(emotions)
        if support:
            lines.append(f"\n\n{support}")

        # SAFETY CHECK: Universal fallback if response is empty
        response = "".join(lines).strip()
        if not response:
            response = self._generate_universal_fallback(user_message)
        
        return response

    def _build_story_summary(self, keywords: List[str], user_message: str) -> str:
        """Build summary that reflects the user's story"""
        parts = []

        if 'change' in keywords:
            parts.append("Ada perubahan yang signifikan dalam cerita kamu")

        if 'fear' in keywords:
            parts.append("dan rasa takut yang ikut muncul")

        if 'loss' in keywords:
            parts.append("dengan perasaan kehilangan")

        if 'exhaustion' in keywords:
            parts.append("sementara energi kamu terus terkuras")

        if not parts:
            return "Dari cerita yang kamu bagikan, terlihat ada beban yang cukup dalam yang kamu bawa."

        return ", ".join(parts) + "."

    def _generate_deepening_question(
        self,
        keywords: List[str],
        emotions: List[Tuple],
        user_message: str,
        details: Dict
    ) -> str:
        """Generate question to deepen understanding"""

        questions = {
            'change': "Dari semua perubahan itu, yang paling nyakitin kamu bagian yang mana?",
            'fear': "Ketakutan yang kamu rasain itu biasanya muncul paling kuat kapan?",
            'loss': "Saat kehilangan itu terjadi, ada orang yang bisa kamu cerita nggak?",
            'exhaustion': "Udah berapa lama kamu merasa capek kayak gini?",
            'confusion': "Belakangan ini yang paling bingung kamu tentang apa?",
            'isolation': "Ada yang kamu percaya dan bisa kamu cerita tentang ini?",
        }

        for keyword in keywords[:1]:
            if keyword in questions:
                return questions[keyword]

        return None

    def _generate_insight_question(
        self,
        emotions: List[Tuple],
        keywords: List[str]
    ) -> str:
        """Generate insight-level question"""

        if emotions:
            emotion_name, _ = emotions[0]

            insight_questions = {
                'fear_of_abandonment': "Menurut kamu, apa yang paling takut kamu kehilangan dari orang itu?",
                'insecurity': "Ada bagian dari diri kamu yang rasa nggak cukup, bagian yang mana?",
                'overthinking': "Kalau pikiran mulai berjalan, biasanya ending yang kamu khayalkan apa?",
                'emotional_exhaustion': "Kalau kamu boleh istirahat dari semua ini, hal pertama yang pengen kamu lakukan apa?",
            }

            if emotion_name in insight_questions:
                return insight_questions[emotion_name]

        return None

    def _generate_support_action(self, emotions: List[Tuple]) -> str:
        """Generate gentle supportive action or suggestion"""

        support_actions = {
            'fear_of_abandonment': "Mungkin worth it buat coba communicate dengan orang itu kalau kamu merasa ada yang berubah.",
            'emotional_exhaustion': "Mungkin perlu dedicated time buat istirahat dan refuel emotional battery kamu.",
            'loneliness': "Mungkin bisa mulai dari sharing dengan satu orang yang kamu percaya tentang ini.",
            'overthinking': "Mungkin bisa helpful buat write down pikiran kamu dan lihat mana yang nyata vs imajinasi.",
        }

        if emotions:
            emotion_name, _ = emotions[0]
            if emotion_name in support_actions:
                return support_actions[emotion_name]

        return None

    def _pick_random(self, items: List[str]) -> str:
        """Pick random item from list"""
        import random
        return random.choice(items)

    def _generate_universal_fallback(self, user_message: str) -> str:
        """
        UNIVERSAL EMOTIONAL REFLECTION FALLBACK - NATURAL INDONESIAN
        
        Generate emotionally intelligent response untuk TOPIK APAPUN ketika:
        - emotion detection gagal
        - keyword tidak ditemukan
        - topic belum ada di patterns
        - detector fail
        
        CORE: Emotional reflection, bukan "aku siap dengarkan"
        HARUS: Full natural Indonesian, nggak ada English
        """
        
        # 1. Generate emotional reflection dari engine
        emotional_reflection = self.emotional_reflection_engine.generate_reflection(
            user_message,
            emotions_detected=None
        )
        
        # 2. Analyze message untuk context
        user_lower = user_message.lower()
        message_length = len(user_message.split())
        
        # Detect sentiment untuk context
        negative_words = [
            'nggak', 'tidak', 'udah', 'berat', 'capek', 'lelah', 'sedih',
            'takut', 'khawatir', 'cemas', 'kosong', 'hampa', 'sendiri',
            'sepi', 'kecewa', 'malu', 'bersalah', 'sakit', 'nyeri',
        ]
        has_negative_sentiment = any(word in user_lower for word in negative_words)
        
        # Detect if user asking for advice
        advice_keywords = ['gimana', 'bagaimana', 'aku harus', 'solusi', 'cara', 'biar nggak', 'supaya']
        is_asking_advice = any(kw in user_lower for kw in advice_keywords)
        
        # 3. Build response
        response = emotional_reflection
        
        # 4. Add optional second layer berdasarkan context
        if message_length < 8 and has_negative_sentiment:
            # Short emotional messages - encourage sharing
            follow_ups = [
                "\n\nAda yang lagi terasa berat dalam hidup kamu belakangan ini, ya.",
                "\n\nKalau ada yang mau kamu cerita lebih lanjut, nggak masalah.",
                "\n\nRasanya ada sesuatu yang ingin kamu lepaskan dari hati kamu.",
                "\n\nPasti ada yang membuat kamu merasa kayak gitu.",
            ]
            response += random.choice(follow_ups)
        elif is_asking_advice:
            # User asking for solutions - add practical nudge
            advice_follow_ups = [
                "\n\nMungkin kita bisa coba lihat dari cara yang berbeda.",
                "\n\nAda beberapa hal kecil yang mungkin bisa membantu.",
                "\n\nKadang dimulai dari hal yang paling sederhana bisa jadi awal yang baik.",
            ]
            response += random.choice(advice_follow_ups)
        
        # 5. Final polish
        response = self.humanizer.humanize(response, stage=1)
        
        return response
