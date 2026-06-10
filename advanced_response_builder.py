"""
Advanced Response Builder
- Integrates all analysis modules (contextual, intent, fear, emotion, reasoning)
- Generates responses based on response mode (LISTENING, UNDERSTANDING, GUIDANCE, ADVICE)
- Implements third message rule
- Handles progressive understanding
- Maintains context consistency
- No empty responses - always gives meaningful feedback
"""

from typing import Dict, List, Optional, Tuple
import re
import random
from reasoning_engine import ReasoningEngine, AnalysisResult
from advice_support_builder import AdviceSupportBuilder
from emotional_memory import EmotionalMemory


TOPIC_SOLUTION_KB = {
    'relationship': {
        'default': (
            "bedakan dulu mana fakta dan mana asumsi. Faktanya, ada perubahan yang kamu rasakan, "
            "tapi alasan di balik perubahan itu masih perlu dibicarakan. Setelah lebih tenang, "
            "coba sampaikan bahwa kamu merasa komunikasi kalian berbeda dan ingin tahu apakah ada sesuatu yang sedang terjadi."
        ),
        'situations': {
            'relationship_distance': (
                "jangan langsung menyimpulkan bahwa kamu penyebab semuanya. Catat dulu perubahan yang nyata, "
                "misalnya chat makin singkat atau balasan makin lama. Setelah itu ajak bicara tanpa menuduh, "
                "pakai kalimat seperti kamu merasa ada jarak dan ingin memahami apa yang sedang terjadi."
            ),
            'relationship_conflict': (
                "jangan mulai pembicaraan saat emosi sedang tinggi. Pilih waktu yang lebih tenang, lalu fokus pada satu masalah utama. "
                "Kalau pertengkaran terus berulang, lihat apakah tindakannya berubah setelah dibicarakan, bukan hanya janji."
            ),
            'breakup': (
                "beri ruang dulu untuk menerima rasa kehilangan sebelum memaksa diri cepat baik-baik saja. "
                "Kurangi hal yang membuat luka terus terbuka, lalu cari satu rutinitas kecil yang membantu kamu tetap berjalan hari ini."
            ),
        },
        'followups': [
            "mulai dari satu kalimat sederhana: apa yang berubah, bagaimana dampaknya ke kamu, dan apa yang kamu butuhkan dari dia.",
            "kalau dia menghindar terus setelah dibicarakan, langkah berikutnya adalah menentukan batas supaya kamu tidak terus menunggu tanpa kejelasan.",
        ],
    },
    'education': {
        'default': (
            "pisahkan dulu masalah belajar, tugas, dan administrasi. Untuk yang paling dekat, pilih materi atau tugas yang dampaknya terbesar. "
            "Kalau ada urusan sekolah seperti pembayaran atau tenggat, cari kejelasan ke wali kelas, dosen, atau pihak sekolah."
        ),
        'situations': {
            'exam_coming': (
                "untuk sekarang jangan memikirkan seluruh kelulusan sekaligus. Pilih materi yang paling mungkin keluar atau paling belum kamu kuasai, "
                "lalu belajar dalam blok pendek. Lebih baik punya bekal inti daripada panik memikirkan semua bab."
            ),
            'school_payment': (
                "pisahkan belajar dan urusan pembayaran. Untuk administrasi, cari tahu tenggat dan pilihan yang tersedia, misalnya cicilan atau kelonggaran waktu. "
                "Kalau perlu, minta bantuan orang yang bisa bicara dengan pihak sekolah."
            ),
            'bad_grades': (
                "lihat dulu penyebab nilainya turun: kurang paham materi, kurang latihan, atau waktu belajar yang berantakan. "
                "Dari situ baru tentukan satu perbaikan paling kecil untuk ujian atau tugas berikutnya."
            ),
        },
        'followups': [
            "mulai dari daftar tiga hal: materi paling penting, waktu belajar yang tersedia, dan siapa yang bisa dimintai kejelasan.",
            "kalau waktunya mepet, jangan mengejar sempurna. Kejar bagian yang paling mungkin menambah nilai dulu.",
        ],
    },
    'career': {
        'default': (
            "kamu tidak perlu mencoba semua arah sekaligus. Pilih dulu satu jenis posisi yang paling masuk akal untuk kamu incar, "
            "rapikan CV sesuai posisi itu, lalu cek keterampilan apa yang paling sering diminta dari lowongan serupa."
        ),
        'situations': {
            'job_search_pressure': (
                "mulai dari satu posisi prioritas, bukan semua lowongan sekaligus. Sesuaikan CV untuk posisi itu, "
                "buat target lamaran realistis, lalu evaluasi setiap minggu apakah masalahnya kurang peluang atau ada keterampilan yang perlu diperkuat."
            ),
            'interview_fail': (
                "satu proses interview yang gagal belum cukup untuk menyimpulkan kamu tidak mampu. Coba catat bagian yang terasa lemah, "
                "latih jawaban untuk bagian itu, dan kalau memungkinkan minta masukan dari orang yang paham rekrutmen."
            ),
            'career_confusion': (
                "pecah kebingungan karier menjadi tiga bagian: kemampuan yang kamu punya, minat yang masih mau dicoba, dan peluang yang benar-benar tersedia. "
                "Dari situ pilih satu eksperimen kecil, bukan keputusan hidup yang besar sekaligus."
            ),
            'job_stress': (
                "bedakan apakah masalahnya beban kerja, lingkungan, atau arah karier yang tidak berkembang. "
                "Kalau masih bisa dibicarakan, siapkan contoh konkret sebelum bicara dengan atasan. Kalau tidak membaik, mulai petakan opsi pindah secara bertahap."
            ),
        },
        'followups': [
            "mulai dari tiga kolom: posisi yang diincar, syarat yang sering muncul, dan bagian CV yang perlu disesuaikan.",
            "kalau masih bingung, pilih satu posisi dulu selama satu minggu untuk diuji. Setelah itu evaluasi, bukan menilai seluruh masa depan dari satu hari.",
        ],
    },
    'finance': {
        'default': (
            "langkah pertama bukan memikirkan semua masalah uang sekaligus, tapi mengurutkannya berdasarkan tenggat dan risiko. "
            "Catat kewajiban yang paling mendesak, lalu hubungi pihak terkait untuk menanyakan kelonggaran waktu atau pilihan cicilan."
        ),
        'situations': {
            'bill_pressure': (
                "catat semua tagihan dengan tiga hal: jumlah, tanggal jatuh tempo, dan akibat kalau terlambat. "
                "Dahulukan yang risikonya paling besar, lalu tanyakan apakah ada kelonggaran waktu atau cicilan untuk yang belum sanggup dibayar penuh."
            ),
            'insufficient_money': (
                "pisahkan kebutuhan dasar dari pembayaran yang masih bisa dinegosiasikan. Setelah itu, lihat mana yang harus dibayar sebagian dulu "
                "dan mana yang perlu dibicarakan ke pihak terkait supaya kamu tidak menanggung semuanya sendirian."
            ),
            'school_payment': (
                "cari kejelasan tenggat pembayaran dan tanyakan pilihan cicilan atau penundaan. Kalau kamu masih sekolah atau kuliah, "
                "hubungi wali kelas, dosen, administrasi, atau orang yang bisa membantu bicara."
            ),
            'debt_problem': (
                "urutkan utang dari yang paling mendesak dan paling berisiko. Jangan membuat janji bayar baru sebelum tahu kemampuan nyata bulan ini. "
                "Lebih baik komunikasikan rencana kecil yang bisa ditepati daripada diam sampai makin menumpuk."
            ),
        },
        'followups': [
            "mulai dari tiga kolom sederhana: nama tagihan, tanggal jatuh tempo, dan jumlahnya. Setelah itu tandai mana yang risikonya paling besar.",
            "kalau uangnya belum cukup, tentukan pembayaran minimum yang paling aman dulu, lalu komunikasikan sisanya sebelum jatuh tempo.",
        ],
    },
    'family': {
        'default': (
            "pilih waktu bicara saat suasana lebih tenang, bukan ketika rumah sedang panas. Pakai kalimat yang fokus pada perasaan dan dampaknya ke kamu. "
            "Kalau bicara langsung terasa sulit, mulai dari pesan tertulis supaya maksudmu lebih teratur."
        ),
        'situations': {
            'parent_pressure': (
                "kamu tidak harus membalas tekanan dengan konfrontasi langsung. Kalau aman, sampaikan bahwa perbandingan justru membuat kamu kehilangan fokus. "
                "Kalau bicara langsung mudah berubah jadi pertengkaran, tulis pesan singkat dulu."
            ),
            'family_conflict': (
                "jangan memulai pembicaraan saat konflik sedang naik. Tunggu suasana turun, lalu bahas satu hal paling penting saja. "
                "Kalau situasinya tidak aman atau ada kekerasan, prioritaskan mencari bantuan dari orang dewasa atau pihak yang bisa melindungi."
            ),
            'parent_unsupported': (
                "coba jelaskan usaha yang sudah kamu lakukan dengan contoh konkret, bukan hanya membela diri. "
                "Kalau tetap tidak didengar, cari satu orang keluarga yang lebih aman untuk jadi perantara."
            ),
        },
        'followups': [
            "mulai dari pesan pendek seperti: aku jadi sulit fokus kalau terus dibandingkan, aku butuh dibicarakan dengan lebih tenang.",
            "kalau kamu takut dimarahi, jangan mulai dari percakapan panjang. Mulai dari satu kalimat inti dan pilih waktu yang aman.",
        ],
    },
    'friendship': {
        'default': (
            "jangan memaksa diri langsung masuk ke kelompok besar. Mulai dari satu orang yang paling terasa aman, "
            "lalu bangun interaksi kecil yang konsisten lewat topik sederhana seperti tugas, hobi, atau kegiatan bersama."
        ),
        'situations': {
            'no_friends': (
                "mulai dari satu orang dulu, bukan mencari banyak teman sekaligus. Cari kesempatan ngobrol kecil yang berulang, "
                "karena kedekatan biasanya tumbuh dari interaksi yang konsisten."
            ),
            'friendship_exclusion': (
                "kalau sulit masuk obrolan kelompok, coba mulai dari percakapan satu lawan satu. "
                "Pakai topik yang ringan dan nyata, misalnya tugas, kegiatan, atau hal yang sama-sama kalian lihat."
            ),
            'friend_abandoned': (
                "lihat dulu apakah mereka benar-benar menjauh atau ritme pertemanannya berubah. Kalau ada satu orang yang masih terasa aman, "
                "mulai dari menanyakan kabar atau mengajak ngobrol ringan tanpa menuntut kedekatan langsung kembali."
            ),
            'friend_conflict': (
                "kalau konflik masih panas, beri jeda dulu. Setelah itu, bicarakan satu kejadian yang spesifik dan dampaknya ke kamu, "
                "bukan menumpuk semua kesalahan sekaligus."
            ),
        },
        'followups': [
            "mulai dari satu pesan ringan ke satu orang, misalnya menanyakan tugas, kabar, atau hal yang kalian sama-sama minati.",
            "kalau kelompok besar terasa berat, jangan mulai dari sana. Mulai dari interaksi kecil yang risikonya lebih rendah.",
        ],
    },
    'self_esteem': {
        'default': (
            "coba bedakan antara mengevaluasi diri dan menghukum diri. Kamu boleh melihat hal yang perlu diperbaiki, "
            "tapi jangan menjadikan satu kekurangan sebagai kesimpulan bahwa seluruh diri kamu tidak cukup baik."
        ),
        'situations': {
            'social_anxiety_shame': (
                "mulai dari mengurangi cara bicara yang menghukum diri sendiri. Kalau takut dinilai, pilih situasi sosial kecil dulu, "
                "lalu evaluasi berdasarkan fakta, bukan asumsi terburuk."
            ),
            'beauty_insecurity': (
                "pisahkan penampilan dari nilai diri. Hal yang bisa dirawat boleh dirawat pelan-pelan, tapi jangan jadikan itu ukuran apakah kamu layak diterima."
            ),
        },
        'followups': [
            "tulis satu hal kecil yang kamu lakukan dengan baik hari ini. Bukan untuk memaksa positif, tapi untuk melatih cara menilai diri lebih adil.",
            "kalau pikiranmu bilang kamu gagal total, tanya balik: bagian mana yang faktanya perlu diperbaiki, dan bagian mana yang cuma hukuman ke diri sendiri?",
        ],
    },
    'appearance': {
        'default': (
            "pisahkan kondisi fisik dari nilai diri kamu. Hal seperti jerawat, bentuk tubuh, atau gigi bisa dirawat secara realistis, "
            "tapi itu bukan ukuran apakah kamu layak diterima. Mulai dari perawatan yang masuk akal dan kembali ke situasi sosial secara bertahap."
        ),
        'situations': {
            'acne_problem': (
                "rawat jerawat dengan langkah yang realistis dan konsisten, tapi jangan biarkan jerawat menjadi kesimpulan tentang nilai diri kamu. "
                "Kurangi kebiasaan memeriksa kekurangan terus-menerus, lalu mulai bertemu orang dari situasi yang paling nyaman."
            ),
            'weight_concern': (
                "kalau ingin berubah, mulai dari kebiasaan yang sehat dan tidak menghukum tubuh. Jangan ukur nilai diri dari angka atau komentar orang."
            ),
            'teeth_problem': (
                "kalau masalah gigi mengganggu fungsi atau percaya diri, pertimbangkan konsultasi bertahap saat memungkinkan. "
                "Sambil itu, jangan menganggap satu bagian fisik sebagai keseluruhan diri kamu."
            ),
        },
        'followups': [
            "mulai dari satu situasi sosial yang paling aman dulu, bukan langsung memaksa diri tampil di tempat yang membuat kamu sangat cemas.",
            "pilih satu hal yang bisa dirawat minggu ini, lalu batasi kebiasaan memeriksa kekurangan berulang-ulang.",
        ],
    },
    'loneliness': {
        'default': (
            "kamu tidak perlu langsung mencari banyak orang. Mungkin yang kamu butuhkan adalah satu hubungan yang terasa aman. "
            "Coba mulai berbagi satu hal kecil kepada orang yang paling kamu percaya, lalu lihat bagaimana responsnya."
        ),
        'situations': {
            'no_friends': (
                "mulai dari satu koneksi yang paling mungkin, bukan mengejar banyak kenalan. Bagikan sedikit dulu, "
                "karena kedekatan yang aman biasanya tumbuh bertahap."
            ),
            'sleep_problem': (
                "kalau rasa sepi sampai mengganggu tidur, coba keluarkan sebagian isi kepala lewat catatan singkat sebelum tidur, "
                "lalu pilih satu orang yang mungkin bisa kamu hubungi di waktu yang lebih aman."
            ),
        },
        'followups': [
            "mulai dari cerita satu bagian kecil saja, misalnya: akhir-akhir ini aku lagi berat dan butuh ditemani sebentar.",
            "kalau takut dianggap berlebihan, pilih orang yang paling pernah merespons kamu dengan tenang, bukan orang yang paling ramai di sekitar kamu.",
        ],
    },
    'health': {
        'default': (
            "jangan langsung menyimpulkan diagnosis sendiri. Catat gejala, sejak kapan muncul, seberapa sering terjadi, dan apakah mengganggu aktivitas. "
            "Kalau berlanjut, makin berat, atau terasa darurat, sebaiknya cari bantuan tenaga kesehatan atau bantuan langsung."
        ),
        'situations': {
            'sleep_problem': (
                "catat dulu pola tidurnya: jam mulai sulit tidur, apa yang dipikirkan, dan dampaknya besok hari. "
                "Kalau berlangsung terus atau sangat mengganggu aktivitas, pertimbangkan konsultasi ke tenaga kesehatan."
            ),
            'stress_health': (
                "catat gejala fisik, durasi, dan pemicunya. Aku tidak bisa menyimpulkan penyakit dari chat, jadi kalau gejala menetap, memburuk, "
                "atau mengganggu aktivitas, lebih aman diperiksa ke tenaga kesehatan."
            ),
        },
        'followups': [
            "mulai dari catatan sederhana: gejala apa, muncul sejak kapan, seberapa sering, dan apa dampaknya ke aktivitas.",
            "kalau ada nyeri berat, sesak, pingsan, keinginan menyakiti diri, atau kondisi terasa darurat, cari bantuan langsung sekarang.",
        ],
    },
    'future': {
        'default': (
            "kamu tidak perlu langsung menemukan jawaban untuk seluruh masa depan. Pilih satu bidang yang membuat kamu penasaran, "
            "coba satu langkah kecil yang bisa dievaluasi, lalu lihat apakah arahnya cocok atau perlu diganti."
        ),
        'situations': {
            'future_anxiety': (
                "jangan memaksa diri menjawab seluruh masa depan sekaligus. Buat target pendek yang bisa diukur, "
                "misalnya mencoba satu kegiatan, satu keterampilan, atau satu percakapan dengan orang yang lebih berpengalaman."
            ),
            'uncertain_future': (
                "ubah pertanyaan besar menjadi percobaan kecil. Bukan 'hidupku harus jadi apa', tapi 'hal apa yang bisa aku coba minggu ini untuk mengenal arahku lebih baik'."
            ),
        },
        'followups': [
            "mulai dari satu daftar kecil: bidang yang bikin penasaran, keterampilan yang ingin dicoba, dan langkah yang bisa dilakukan minggu ini.",
            "kalau kamu merasa tertinggal, kurangi dulu membandingkan timeline. Fokus ke percobaan kecil yang bisa memberi data tentang arahmu.",
        ],
    },
}


class AdvancedResponseBuilder:
    """
    Build contextually intelligent responses based on comprehensive analysis.
    """
    
    def __init__(self):
        self.reasoning_engine = ReasoningEngine()
        self.advice_builder = AdviceSupportBuilder()
        self.emotional_memory = EmotionalMemory()
        self.solution_fingerprints: List[str] = []
        
        # Situation to Indonesian translation for natural language
        self.situation_translations = {
            'exam_coming': 'ujian mendatang',
            'payment_issue': 'masalah pembayaran',
            'school_payment': 'pembayaran sekolah',
            'sleep_problem': 'masalah tidur',
            'job_stress': 'stress kerja',
            'bad_grades': 'nilai jelek',
            'acne_problem': 'masalah jerawat',
            'no_friends': 'tidak ada teman',
            'breakup': 'putus',
            'relationship_conflict': 'konflik hubungan',
            'weight_concern': 'masalah berat badan',
            'family_conflict': 'konflik keluarga',
            'insufficient_money': 'uang yang belum cukup untuk semua tagihan',
            'bill_pressure': 'tagihan yang menumpuk',
            'debt_problem': 'utang yang menekan',
            'parent_pressure': 'tekanan dan perbandingan dari keluarga',
            'friendship_exclusion': 'rasa tersisih dari lingkungan teman',
            'job_search_pressure': 'tekanan mencari kerja',
            'career_confusion': 'kebingungan arah kerja',
            'future_anxiety': 'kecemasan tentang masa depan',
            'uncertain_future': 'ketidakpastian arah hidup',
            'relationship_distance': 'perubahan jarak dalam hubungan',
            'stress_health': 'keluhan tubuh yang dipengaruhi stres',
        }
        
        # Response templates for each mode
        self.listening_starters = [
            "Aku denger kok.",
            "Iya, aku paham.",
            "Hmm, cerita lanjut.",
            "Aku mengerti.",
            "Pasti berat ya.",
            "Aku ada untuk dengarkan.",
            "Baik, lanjut ceritanya.",
        ]
        
        self.understanding_starters = [
            "Dari cerita kamu, aku mulai ngerti bahwa...",
            "Jadi dari yang kamu ceritain, sepertinya...",
            "Kalau aku lihat dari sudut pandang kamu...",
            "Sejauh ini aku tangkap bahwa...",
            "Berdasarkan apa yang kamu cerita, kayaknya...",
            "Aku rasa yang sedang kamu hadapi itu...",
        ]
        
        self.guidance_starters = [
            "Menurut aku, situasi kamu ini menunjukkan bahwa...",
            "Yang aku lihat dari semuanya adalah...",
            "Kayaknya apa yang terjadi adalah...",
            "Aku rasa yang sedang kamu alami itu normal karena...",
            "Dari cerita kamu, aku merasa perlu kamu tahu bahwa...",
            "Menurut aku ini penting kamu pahami...",
        ]
        
        self.advice_starters = [
            "Langkah pertama yang bisa kamu lakukan:",
            "Menurut aku, kamu bisa coba:",
            "Saran aku untuk kamu:",
            "Aku pikir kamu bisa:",
            "Gimana kalau kamu coba:",
            "Ini yang bisa kamu lakuin:",
        ]
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        emotional_memory: Optional[EmotionalMemory] = None
    ) -> str:
        """
        Generate complete response based on comprehensive analysis.
        PHASE 3: Uses STORY REASONING RULE - connects 3+ messages into one narrative.
        """
        if conversation_history is None:
            conversation_history = []
        
        # 1. BUILD STORY ARC from last 3+ messages
        story_arc = self.reasoning_engine.build_story_arc(conversation_history)
        story_reasoning = {}
        if story_arc.get('has_story'):
            story_reasoning = self.reasoning_engine.extract_story_reasoning(story_arc)
        # 2. COMPREHENSIVE ANALYSIS of current message
        analysis = self.reasoning_engine.analyze(user_message, conversation_history)
        
        # 3. VALIDATE ANALYSIS
        if not self.reasoning_engine.validate_analysis(analysis):
            return self._get_fallback_response(user_message)

        if self._is_solution_request(user_message, analysis):
            topic_solution = self._build_topic_specific_solution(
                analysis=analysis,
                user_message=user_message,
                conversation_history=conversation_history
            )
            if topic_solution:
                return topic_solution
        
        # 3.5 PHASE 3: Attach story context to analysis
        analysis.story_arc = story_arc if story_arc.get('has_story') else None
        analysis.story_reasoning = story_reasoning if story_reasoning else None
        
        # 4. PHASE 2: LINK CONVERSATION CONTEXT
        context_links = self.reasoning_engine.link_conversation_context(analysis, conversation_history)
        
        # 5. PHASE 2: EXTRACT MEANING
        meaning = self.reasoning_engine.extract_meaning(analysis)
        if meaning:
            analysis.meaning = meaning
        
        # 6. UPDATE EMOTIONAL MEMORY
        if emotional_memory:
            situations = [sit[0] for sit in analysis.situations]
            emotional_memory.record_message(
                text=user_message,
                emotions=analysis.emotions,
                implied_emotions=[f for f in analysis.fears.keys()],
                details={},
                topic=analysis.topic,
                situations=situations
            )

        topic_response = self._build_topic_routed_response(analysis, user_message)
        if topic_response:
            return topic_response
        
        # V3: CHECK FOR THIRD MESSAGE RULE
        if self._should_give_interpretation(analysis) and analysis.intent_type != 'advice_seeking':
            # Give interpretation instead of just listening
            return self._build_third_message_interpretation(analysis, user_message)
        
        # 7. BUILD RESPONSE BASED ON MODE (with STORY AWARENESS)
        if analysis.response_mode == 'LISTENING':
            return self._build_listening_response(analysis, user_message)
        
        elif analysis.response_mode == 'UNDERSTANDING':
            return self._build_understanding_response(analysis, user_message, context_links)
        
        elif analysis.response_mode == 'GUIDANCE':
            return self._build_guidance_response(analysis, user_message, emotional_memory, context_links)
        
        elif analysis.response_mode == 'ADVICE':
            return self._build_advice_response(analysis, user_message)
        
        else:
            return self._build_listening_response(analysis, user_message)
    
    def _build_listening_response(self, analysis: AnalysisResult, user_message: str) -> str:
        """
        LISTENING MODE: Build coherent narrative, not fragmented templates.
        Seamlessly combine opening + reflection into one flow.
        """
        narrative = []
        
        # Opening + Reflection blend naturally
        opening = random.choice(self.listening_starters)
        reflection = self._create_reflection(analysis, user_message)
        
        if reflection:
            narrative.append(f"{opening} {reflection}")
        else:
            narrative.append(opening)
        
        # Add emotion acknowledgment
        emotion_ack = self._acknowledge_emotion(analysis.primary_emotion)
        if emotion_ack:
            narrative.append(emotion_ack)
        
        # Add presence/support
        support = random.choice([
            "Aku di sini buat nemenin dan dengarkan kamu.",
            "Aku ada untuk dengarkan apa pun yang ingin kamu cerita.",
            "Santai aja, aku mengerti.",
            "Nggak masalah, lanjutin ceritanya ya.",
        ])
        narrative.append(support)
        
        response = " ".join(narrative)
        return response if response.strip() else self._get_fallback_response(user_message)
    
    def _build_understanding_response(self, analysis: AnalysisResult, user_message: str, context_links: Optional[Dict] = None) -> str:
        """
        UNDERSTANDING MODE: Build narrative that shows real understanding.
        PHASE 3: Uses story arc to connect current message to full narrative.
        """
        if context_links is None:
            context_links = {}
        
        narrative = []
        
        # PHASE 3: If we have a story, acknowledge the full narrative
        if (hasattr(analysis, 'story_arc') and analysis.story_arc and analysis.story_arc.get('has_story') 
            and hasattr(analysis, 'story_reasoning') and analysis.story_reasoning):
            story_reasoning = analysis.story_reasoning
            
            # Build understanding response that shows comprehension of the full story
            opening = random.choice(self.understanding_starters)
            
            # Reference the story progression safely
            progression = story_reasoning.get('progression', '') or ''
            main_issue = story_reasoning.get('main_problem', '') or ''
            
            if progression and main_issue:
                main_clean = main_issue.replace('masalah utama: ', '')
                narrative.append(f"{opening} Dari cerita tiga pesan kamu: {main_clean}, terus {progression}.")
            elif main_issue:
                main_clean = main_issue.replace('masalah utama: ', '')
                narrative.append(f"{opening} Dari cerita yang kamu cerita, aku paham bahwa {main_clean} ini jadi beban besar.")
            else:
                narrative.append(opening)
        else:
            # Fallback to regular understanding mode
            opening = random.choice(self.understanding_starters)
            
            # Use meaning extraction if available
            if hasattr(analysis, 'meaning') and analysis.meaning:
                narrative.append(f"{opening} {analysis.meaning.lower()}.")
            else:
                situation_emotion_link = self._link_situation_to_emotion(analysis)
                if situation_emotion_link:
                    narrative.append(f"{opening} {situation_emotion_link.lower()}")
                else:
                    narrative.append(opening)
        
        # PHASE 2: Check if this is part of a pattern
        if context_links.get('is_progression'):
            narrative.append("Dari cerita sebelumnya, aku lihat ini pattern yang berulang dan anxiety-nya bertambah.")
        
        # Surface the underlying fear
        if analysis.primary_fear:
            fear_recognition = self._recognize_fear(analysis.primary_fear)
            if fear_recognition:
                narrative.append(f"Ada rasa {fear_recognition} di balik semuanya ini.")
        
        # Normalize: Show they're not alone
        normalization = self._normalize_feelings(analysis.primary_emotion, analysis.situations)
        if normalization:
            narrative.append(normalization)
        
        # Invitation to continue
        narrative.append("Cerita terus ya, aku siap dengarkan.")
        
        response = " ".join(narrative)
        return response if response.strip() else self._get_fallback_response(user_message)
    
    def _build_guidance_response(
        self,
        analysis: AnalysisResult,
        user_message: str,
        emotional_memory: Optional[EmotionalMemory] = None,
        context_links: Optional[Dict] = None
    ) -> str:
        """
        GUIDANCE MODE: Build coherent interpretation narrative.
        PHASE 3: Uses story arc to provide guidance based on full narrative.
        """
        if context_links is None:
            context_links = {}
        
        narrative = []
        
        # PHASE 3: If we have a story arc, use it for guidance
        if (hasattr(analysis, 'story_arc') and analysis.story_arc and analysis.story_arc.get('has_story')
            and hasattr(analysis, 'story_reasoning') and analysis.story_reasoning):
            story_reasoning = analysis.story_reasoning
            
            # Strong opening that shows story understanding
            opening = random.choice(self.guidance_starters)
            main_problem = (story_reasoning.get('main_problem') or '').replace('masalah utama: ', '')
            root_cause = (story_reasoning.get('root_cause') or '').replace('penyebabnya: ', '')
            
            # Build guidance narrative from story
            narrative.append(f"{opening} Dari tiga pesan kamu, aku lihat cerita begini:")
            if root_cause and main_problem:
                narrative.append(f"Awal-awalnya ada {root_cause}, terus berkembang jadi {main_problem}.")
            elif main_problem:
                narrative.append(f"Cerita kamu ada tentang {main_problem}.")
            
            # Add the fear dimension
            primary_fear = (story_reasoning.get('primary_fear') or '').replace('ketakutan terbesar: ', '')
            if primary_fear and primary_fear != 'belum jelas':
                narrative.append(f"Di balik semua itu ada {primary_fear} yang membuat kamu overthinking.")
            
            # Mechanism explanation
            explanation = self._explain_mechanism(analysis)
            if explanation:
                narrative.append(explanation)
        else:
            # Fallback to regular guidance mode
            opening = random.choice(self.guidance_starters)
            
            # Create meaningful understanding
            interpretation = self._create_interpretation(analysis, user_message)
            if interpretation:
                narrative.append(f"{opening} {interpretation}.")
            else:
                narrative.append(opening)
            
            # PHASE 2: Show pattern recognition if detected
            if context_links.get('connections', {}).get('repeating_situation'):
                narrative.append("Ini adalah situasi yang kamu hadapi berulang kali, dan aku lihat anxiety-nya bertambah.")
            
            # Mechanism explanation
            explanation = self._explain_mechanism(analysis)
            if explanation:
                narrative.append(explanation)
        
        # Insight: Meaningful perspective
        insight = self._generate_insight(analysis)
        if insight:
            narrative.append(insight)
        
        # Light support: Path forward
        support = self._offer_light_support(analysis)
        if support:
            narrative.append(support)
        
        response = " ".join(narrative)
        return response if response.strip() else self._get_fallback_response(user_message)

    def _is_solution_request(self, user_message: str, analysis: AnalysisResult) -> bool:
        text = user_message.lower()
        signals = [
            'harus gimana', 'harus bagaimana', 'aku harus apa', 'harus apa',
            'menurut kamu aku harus', 'solusinya apa', 'solusi apa',
            'minta saran', 'kasih saran', 'gimana caranya', 'bagaimana caranya',
            'mulai dari mana', 'apa yang harus aku lakukan', 'apa yang harus kulakukan',
            'aku harus bayar yang mana', 'harus mulai dari mana',
        ]
        return (
            analysis.intent == 'advice_seeking'
            or analysis.intent_type == 'advice_seeking'
            or any(signal in text for signal in signals)
        )

    def _build_topic_specific_solution(
        self,
        analysis: AnalysisResult,
        user_message: str,
        conversation_history: List[Dict]
    ) -> str:
        topic = self._resolve_solution_topic(analysis, user_message, conversation_history)
        if topic not in TOPIC_SOLUTION_KB:
            return self._build_contextual_solution_fallback(user_message)

        combined_text = self._combined_recent_user_text(user_message, conversation_history)
        situations = self._resolve_solution_situations(analysis, combined_text)
        solution_data = TOPIC_SOLUTION_KB[topic]
        selected_solution = self._select_solution_text(solution_data, situations)
        selected_solution = self._avoid_repeated_solution(solution_data, selected_solution)
        selected_solution = self._capitalize_solution(selected_solution)

        detail = self._solution_detail(topic, situations, combined_text)
        response = f"Menurut aku {detail}. {selected_solution}"
        response = self._clean_solution_language(response)
        return response if response.strip() else self._build_contextual_solution_fallback(user_message)

    def _resolve_solution_topic(
        self,
        analysis: AnalysisResult,
        user_message: str,
        conversation_history: List[Dict]
    ) -> Optional[str]:
        if analysis.topic in TOPIC_SOLUTION_KB and analysis.topic_confidence >= 0.65:
            return analysis.topic

        combined_text = self._combined_recent_user_text(user_message, conversation_history)
        heuristic_topic = self._infer_solution_topic_by_keywords(combined_text)
        if heuristic_topic:
            return heuristic_topic

        if analysis.topic in TOPIC_SOLUTION_KB and analysis.topic_confidence >= 0.35:
            return analysis.topic

        topic, confidence = self.reasoning_engine.topic_detector.detect(combined_text)
        if topic in TOPIC_SOLUTION_KB and confidence >= 0.12:
            return topic

        for msg in reversed(conversation_history or []):
            if msg.get('role') != 'user':
                continue
            topic, confidence = self.reasoning_engine.topic_detector.detect(msg.get('message', ''))
            if topic in TOPIC_SOLUTION_KB and confidence >= 0.12:
                return topic

        return analysis.topic

    def _infer_solution_topic_by_keywords(self, combined_text: str) -> Optional[str]:
        text = combined_text.lower()
        topic_signals = [
            ('relationship', ['pacar', 'pasangan', 'gebetan', 'mantan', 'chat singkat', 'lama bales', 'hubungan']),
            ('education', ['ujian', 'tugas', 'sekolah', 'kuliah', 'nilai', 'belajar', 'dosen', 'wali kelas']),
            ('career', ['kerja', 'pekerjaan', 'lamaran', 'cv', 'interview', 'karier', 'karir', 'nganggur']),
            ('finance', ['tagihan', 'utang', 'hutang', 'cicilan', 'uang', 'duit', 'bayar', 'pemasukan', 'penghasilan']),
            ('self_esteem', ['nggak layak', 'gak layak', 'tidak layak', 'nggak cukup', 'minder', 'percaya diri', 'kalah dibanding']),
            ('family', ['orang tua', 'ayah', 'ibu', 'keluarga', 'rumah', 'anak orang lain', 'dibandingkan', 'dibanding']),
            ('loneliness', ['tetap merasa sendiri', 'punya teman tapi', 'tempat cerita', 'dianggap berlebihan', 'takut cerita', 'merasa sendiri', 'kesepian']),
            ('friendship', ['circle', 'sirkel', 'numpang ada', 'masuk obrolan', 'dikucilkan', 'pertemanan', 'teman-teman']),
            ('appearance', ['jerawat', 'gendut', 'kurus', 'gigi', 'wajah', 'penampilan', 'malu ketemu']),
            ('health', ['susah tidur', 'sulit tidur', 'badan', 'gejala', 'penyakit', 'dokter', 'kesehatan']),
            ('future', ['masa depan', 'arah hidup', 'salah jalan', 'tujuan', 'tertinggal']),
        ]
        for topic, signals in topic_signals:
            if any(signal in text for signal in signals):
                return topic
        return None

    def _build_topic_routed_response(self, analysis: AnalysisResult, user_message: str) -> str:
        topic = analysis.topic
        situations = [s[0] for s in analysis.situations]
        text = user_message.lower()

        if topic == 'friendship':
            if 'friendship_exclusion' in situations or 'no_friends' in situations or any(signal in text for signal in ['circle', 'sirkel', 'numpang ada']):
                if analysis.conversation_depth <= 2:
                    return (
                        "Rasanya sepi ya ketika orang lain seperti sudah punya tempat masing-masing, "
                        "sementara kamu merasa cuma berada di pinggirnya. Yang bikin berat mungkin bukan sekadar jumlah teman, "
                        "tapi belum ada rasa benar-benar diterima di lingkungan itu."
                    )

                return (
                    "Kalau kamu sering diam karena bingung masuk dari mana, itu bukan berarti kamu membosankan atau tidak ingin bergabung. "
                    "Mungkin kamu sedang terlalu hati-hati karena takut ucapanmu terasa canggung. Coba mulai dari satu orang yang paling terasa aman, "
                    "lalu tanggapi satu bagian kecil dari obrolan. Kamu tidak harus langsung masuk ke satu kelompok sekaligus."
                )

        if topic == 'family':
            if 'parent_pressure' in situations or any(signal in text for signal in ['dibanding', 'anak orang lain', 'di rumah']):
                return (
                    "Capek ya ketika rumah yang seharusnya jadi tempat istirahat justru membuat kamu terus merasa dibandingkan. "
                    "Yang paling berat mungkin bukan cuma perkataannya, tapi karena usaha kamu terasa tidak benar-benar dilihat. "
                    "Kalau situasinya cukup aman, pilih waktu yang lebih tenang untuk bilang bahwa perbandingan seperti itu bikin kamu makin kehilangan fokus. "
                    "Kalau bicara langsung terasa sulit, mulai dari pesan singkat dulu."
                )

        if topic == 'future':
            if 'uncertain_future' in situations or 'future_anxiety' in situations or any(signal in text for signal in ['arah hidup', 'masa depan', 'tujuan']):
                return (
                    "Bingung soal arah hidup memang bisa terasa besar, apalagi ketika teman-teman terlihat sudah punya tujuan masing-masing. "
                    "Tapi kamu tidak harus menemukan jawaban seluruh hidup sekaligus. Mulai dari satu bidang yang ingin kamu coba, "
                    "satu keterampilan kecil, atau satu pengalaman baru, lalu evaluasi pelan-pelan apakah arahnya cocok untuk kamu."
                )

        return ""

    def _combined_recent_user_text(self, user_message: str, conversation_history: List[Dict]) -> str:
        recent = []
        for msg in reversed(conversation_history or []):
            if msg.get('role') == 'user':
                recent.append(msg.get('message', ''))
            if len(recent) >= 2:
                break
        return " ".join(list(reversed(recent)) + [user_message])

    def _resolve_solution_situations(self, analysis: AnalysisResult, combined_text: str) -> List[str]:
        situation_scores = {}
        for situation, score in analysis.situations:
            situation_scores[situation] = max(situation_scores.get(situation, 0), score)
        for situation, score in self.reasoning_engine.situation_detector.detect(combined_text):
            situation_scores[situation] = max(situation_scores.get(situation, 0), score * 0.95)
        return [
            situation for situation, _ in sorted(
                situation_scores.items(),
                key=lambda item: item[1],
                reverse=True
            )
        ]

    def _select_solution_text(self, solution_data: Dict, situations: List[str]) -> str:
        for situation in situations:
            if situation in solution_data.get('situations', {}):
                return solution_data['situations'][situation]
        return solution_data.get('default', '')

    def _avoid_repeated_solution(self, solution_data: Dict, selected_solution: str) -> str:
        fingerprint = self._solution_fingerprint(selected_solution)
        if fingerprint not in self.solution_fingerprints:
            self.solution_fingerprints.append(fingerprint)
            self.solution_fingerprints = self.solution_fingerprints[-8:]
            return selected_solution

        for followup in solution_data.get('followups', []):
            followup_fingerprint = self._solution_fingerprint(followup)
            if followup_fingerprint not in self.solution_fingerprints:
                self.solution_fingerprints.append(followup_fingerprint)
                self.solution_fingerprints = self.solution_fingerprints[-8:]
                return followup

        return selected_solution

    def _solution_fingerprint(self, text: str) -> str:
        words = re.sub(r'\W+', ' ', text.lower()).strip().split()
        return " ".join(words[:16])

    def _capitalize_solution(self, text: str) -> str:
        text = text.strip()
        if not text:
            return text
        return text[:1].upper() + text[1:]

    def _solution_detail(self, topic: str, situations: List[str], combined_text: str) -> str:
        if topic == 'relationship':
            return "masalah utamanya adalah perubahan sikap atau komunikasi yang bikin kamu merasa hubungan ini tidak seaman dulu"
        if topic == 'education':
            return "yang perlu kamu hadapi bukan semua beban sekolah sekaligus, tapi bagian yang paling dekat dan paling mendesak"
        if topic == 'career':
            return "kamu sedang butuh arah kerja yang lebih jelas, bukan sekadar disuruh terus berusaha tanpa rencana"
        if topic == 'finance':
            return "masalah uang ini bikin kamu merasa tidak aman karena kewajiban terus menumpuk sementara jalan keluarnya belum jelas"
        if topic == 'family':
            return "tekanan keluarga ini perlu dibahas dengan cara yang aman, karena kamu sudah cukup lama menahan dampaknya sendiri"
        if topic == 'friendship':
            return "masalahnya ada pada cara membangun kedekatan sosial yang terasa aman, bukan pada nilai diri kamu sebagai teman"
        if topic == 'self_esteem':
            return "yang sedang berat adalah cara kamu menilai diri sendiri terlalu keras"
        if topic == 'appearance':
            return "yang perlu dijaga adalah supaya kondisi fisik tidak berubah menjadi kesimpulan tentang nilai diri kamu"
        if topic == 'loneliness':
            return "yang kamu butuhkan bukan sekadar ramai di sekitar, tapi koneksi yang terasa aman untuk berbagi"
        if topic == 'health':
            return "keluhan tubuh atau tidur ini perlu ditangani hati-hati tanpa langsung menyimpulkan diagnosis sendiri"
        if topic == 'future':
            return "kamu tidak perlu menjawab seluruh masa depan sekaligus"
        return "situasi ini perlu dipecah supaya langkah berikutnya lebih jelas"

    def _clean_solution_language(self, response: str) -> str:
        replacements = {
            'support': 'dukungan',
            'trust': 'percaya',
            'capable': 'mampu',
            'vicious cycle': 'pola yang berulang',
            'insufficient_money': 'masalah uang',
            'uncertainty': 'ketidakpastian',
            'fear_of_abandonment': 'takut ditinggalkan',
            'emotional_exhaustion': 'kelelahan emosional',
            'self_esteem_issue': 'cara menilai diri sendiri',
            'relationship_distress': 'tekanan dalam hubungan',
            'pattern': 'pola',
        }
        for source, target in replacements.items():
            response = re.sub(re.escape(source), target, response, flags=re.IGNORECASE)
        return response

    def _build_contextual_solution_fallback(self, user_message: str) -> str:
        detail = user_message.strip()
        if len(detail) > 90:
            detail = detail[:87].rstrip() + "..."
        return (
            f"Menurut aku bagian tentang '{detail}' perlu dipecah dulu supaya tidak terasa seperti satu beban besar. "
            "Coba tulis satu hal yang paling mendesak, satu hal yang masih bisa menunggu, dan satu orang atau pihak yang bisa kamu hubungi untuk mendapat kejelasan."
        )
    
    def _build_advice_response(self, analysis: AnalysisResult, user_message: str) -> str:
        """
        ADVICE MODE: Build advice narrative with practical steps.
        Format: Menurut aku [insight], saran dari aku [steps]
        Always 100% Indonesian. No English fallback.
        """
        narrative = []
        
        # Get the comprehensive insight first
        insight = self._build_specific_insight(analysis)
        if insight:
            narrative.append(f"Menurut aku {insight}")
        else:
            # Fallback opening
            narrative.append(random.choice(self.advice_starters))
        
        # Add practical steps
        steps = self._get_practical_steps(analysis)
        if steps:
            narrative.extend(steps)
        else:
            # FULL INDONESIAN FALLBACK - never English
            narrative.extend([
                "1. Pecahin masalah ini jadi bagian-bagian yang lebih kecil.",
                "2. Fokus ke hal yang bisa kamu kontrol sekarang.",
                "3. Jangan coba solve semuanya langsung."
            ])
        
        # Strong ending
        narrative.append("Kamu pasti bisa. Aku percaya pada kamu.")
        
        response = " ".join([p for p in narrative if p])
        return response if response.strip() else self._get_fallback_response(user_message)
    
    # =====================================================================
    # V3: THIRD MESSAGE RULE & REASONING-BASED RESPONSES
    # =====================================================================
    
    def _should_give_interpretation(self, analysis: AnalysisResult) -> bool:
        """
        V3: Third Message Rule - should bot give interpretation/insight?
        Requires: 3+ messages OR 2+ situations/fears
        """
        if analysis.conversation_depth < 3:
            return False
        
        situation_count = len(analysis.situations)
        fear_count = len(analysis.fears)
        
        # Trigger on 3+ messages with content
        return analysis.conversation_depth >= 3
    
    def _build_third_message_interpretation(self, analysis: AnalysisResult, user_message: str) -> str:
        """
        V3: Build interpretation response for third message onwards.
        Format: Menurut aku kamu sedang mengalami [X], saran dari aku kamu harus [Y]
        """
        narrative = []
        
        # Get the comprehensive insight that already has "kamu sedang mengalami..." format
        insight = self._build_specific_insight(analysis)
        
        if insight:
            # Insight already has the full format, just add "Menurut aku" prefix
            narrative.append(f"Menurut aku {insight}")
        else:
            # Fallback: build basic interpretation
            opening = "Menurut aku dari cerita kamu,"
            situation_desc = self._build_situation_description(analysis)
            if situation_desc:
                narrative.append(f"{opening} {situation_desc}")
            else:
                narrative.append(opening + " ada sesuatu yang membuat kamu merasa berat.")
        
        # Add support/normalization
        support = self._normalize_feelings(analysis.primary_emotion, analysis.situations)
        if support:
            narrative.append(support)
        
        # Invitation to continue or ask for help
        if analysis.intent == 'advice_seeking':
            narrative.append("Mau aku bantu cari langkah kecil untuk mulai?")
        else:
            narrative.append("Lanjutin cerita kamu, aku siap dengarkan.")
        
        return " ".join([p for p in narrative if p])
    
    def _build_situation_description(self, analysis: AnalysisResult) -> str:
        """
        V3: Describe the actual situation from pattern/emotion/fear
        NOT just listing keywords
        """
        if not analysis.situations:
            return ""
        
        situation = analysis.situations[0][0]
        emotion = analysis.primary_emotion
        
        # Translate situations to human descriptions
        situation_descriptions = {
            # Education
            'school_payment': "ada masalah biaya sekolah yang belum terselesai, dan itu bikin pikiran kamu jadi terus menempel pada masalah ini",
            'exam_coming': "ada ujian yang bikin kamu khawatir, terutama karena ada masalah lain yang juga harus dipikirkan",
            'bad_grades': "nilai kamu tidak sesuai harapan, dan itu membuat kamu merasa tidak cukup pintar atau cukup baik",
            'school_dropout': "kamu merasa tertinggal atau gagal dalam akademik, dan itu bikin rasa malu",
            
            # Health & Sleep
            'sleep_problem': "susah tidur karena pikiran kamu tidak bisa berhenti dari semua kekhawatiran yang menumpuk",
            'health_issue': "masalah kesehatan membuat kamu cemas tentang masa depan dan apa yang bisa terjadi",
            
            # Appearance & Body
            'acne_problem': "kamu nggak nyaman sama penampilan, terutama karena khawatir bagaimana orang lain menilai kamu",
            'teeth_problem': "kamu insecure tentang gigi, dan itu bikin kamu tidak percaya diri saat berbicara atau tersenyum",
            'weight_concern': "kamu khawatir tentang berat badan, dan itu terus mengganggu pikiran dan kepercayaan diri kamu",
            'beauty_insecurity': "ada ketidakpuasan tentang penampilan yang membuat kamu merasa tidak cukup baik",
            'social_anxiety_shame': "kamu merasa malu dan tidak percaya diri ketika bertemu orang, dan itu bikin kamu ingin menghindari interaksi sosial",
            
            # Relationships
            'breakup': "ada perpisahan atau putus yang membuat hati terasa sakit dan confused tentang masa depan",
            'relationship_conflict': "sering ada pertengkaran atau cekcok yang bikin hubungan terasa tegang dan melelahkan",
            'relationship_distance': "merasa jarak atau perubahan dalam hubungan, dan itu bikin kamu khawatir apakah semuanya masih baik",
            'partner_cheating': "ada kecurigaan atau ketakuan akan pengkhianatan, yang membuat trust menjadi goyah",
            
            # Career
            'job_stress': "kerja membuat kamu lelah dan stress berkepanjangan, sampai sulit untuk relax",
            'job_conflict': "ada konflik dengan boss atau rekan kerja yang membuat lingkungan kerja jadi tidak enak",
            'job_loss': "kamu kehilangan pekerjaan atau sedang mencari pekerjaan, yang bikin kamu merasa tidak stabil",
            'interview_fail': "interview tidak berhasil, dan itu membuat kamu meragukan kemampuan diri sendiri",
            
            # Family
            'family_conflict': "ada konflik keluarga yang membuat suasana rumah jadi tegang dan tidak nyaman",
            'parent_pressure': "orang tua memberi tekanan atau ekspektasi tinggi yang bikin kamu merasa terbeban",
            'parent_unsupported': "dukungan dari keluarga terasa kurang, dan itu membuat kamu merasa usaha kamu tidak terlihat",
            
            # Social & Friends
            'no_friends': "merasa sendirian di tengah orang-orang yang punya circle mereka sendiri",
            'friend_conflict': "ada pertengkaran atau konflik dengan teman, dan itu bikin hubungan jadi awkward",
            'feeling_excluded': "merasa diabaikan atau dikucilkan dari grup atau lingkungan sosial",
            'friendship_exclusion': "merasa tersisih dari obrolan atau circle teman, seolah kamu hanya numpang ada",
            
            # Finance
            'payment_issue': "ada beban finansial yang membuat kamu stres tentang bagaimana caranya",
            
            # Future & Direction
            'uncertain_future': "tidak tahu apa yang harus dilakukan dengan masa depan, dan itu bikin kamu cemas",
        }
        
        if situation in situation_descriptions:
            return situation_descriptions[situation]
        
        # Fallback: use topic + emotion
        return f"ada situasi tentang {situation} yang membuat kamu merasa {emotion}"
    
    def _build_fear_reflection(self, analysis: AnalysisResult) -> str:
        """
        V3: Reflect the underlying fear (not the surface problem)
        Make it human, specific, not clinical
        """
        if not analysis.primary_fear:
            return ""
        
        fear = analysis.primary_fear
        
        fear_reflections = {
            'fear_of_failure': "kamu takut kalau kegagalan ini akan berakibat pada masa depan kamu",
            'fear_of_rejection': "kamu takut ditolak atau dianggap tidak layak",
            'fear_of_abandonment': "ada ketakutan kalau orang-orang penting bakal pergi",
            'fear_of_judgment': "kamu takut bagaimana orang lain akan menilai atau menghakimi",
            'insecurity': "ada keragu-raguan tentang diri sendiri atau kemampuan kamu",
            'shame': "ada rasa malu yang membuat kamu ingin menyembunyikan segalanya",
            'loneliness': "takut kalau kamu bakal selamanya sendirian",
            'helplessness': "merasa tidak ada yang bisa kamu lakukan untuk mengubah situasi",
        }
        
        if fear in fear_reflections:
            return fear_reflections[fear]
        
        return f"ada ketakutan tersembunyi di balik semua ini"
    
    def _build_specific_insight(self, analysis: AnalysisResult) -> str:
        """
        V3: Build specific insight from topic + situation + fear
        Format: "menurut aku kamu sedang mengalami [kondisi], saran dari aku kamu harus [solusi]"
        """
        topic = analysis.topic
        situations = [s[0] for s in analysis.situations]
        fear = analysis.primary_fear
        
        # ===== COMBINED SITUATIONS - PRIORITIZE THESE FIRST =====
        
        # Acne + Social Anxiety: SPECIFIC insight for this combo
        if 'acne_problem' in situations and 'social_anxiety_shame' in situations:
            if fear == 'fear_of_judgment':
                return "kamu sedang mengalami kombinasi: insecurity tentang jerawat + takut dinilai ketika bertemu orang, yang membuat kamu avoid interaksi. Saran dari aku kamu harus tahu bahwa orang lain jauh lebih fokus ke diri mereka sendiri, dan jerawat BUKAN alasan valid untuk mengisolasi diri. Mulai dari hal kecil - satu teman, satu event - dan skincare konsisten juga membantu confidence."
            return "kamu sedang mengalami jerawat yang bikin tidak pede bertemu orang, dan ini menciptakan lingkaran: semakin tidak pede, semakin isolasi, semakin stress, semakin parah jerawat. Saran dari aku kamu harus break lingkaran ini dengan skincare routine + small social interactions. Stress adalah musuh besar jerawat."
        
        # Exam + Sleep: SPECIFIC
        if 'exam_coming' in situations and 'sleep_problem' in situations:
            if fear == 'fear_of_failure':
                return "kamu sedang mengalami anxiety ujian yang membuat otak nggak bisa tidur, yang membuat kamu semakin tired dan nggak siap ujian. Saran dari aku kamu harus prioritas sleep dulu sebelum last-minute study - otak yang rest adalah otak yang bisa retain informasi."
            return "kamu sedang mengalami double pressure ujian + insomnia, dan ini create vicious cycle. Saran dari aku kamu harus wind down routine sebelum tidur - 30 menit tanpa screen, breathing exercise, tapi juga accept bahwa satu malam tidur kurang tidak akan destroy ujian kamu."
        
        # Exam + Payment: SPECIFIC
        if 'exam_coming' in situations and ('payment_issue' in situations or 'school_payment' in situations):
            return "kamu sedang mengalami double pressure ujian plus masalah biaya, dan kepikiran biaya membuat fokus belajar jadi terpotong. Saran dari aku kamu harus pisahkan: tackle ujian sekarang (3-7 hari ke depan), biaya bisa di-discuss dengan keluarga SETELAH ujian. Satu hal at a time, jangan overload."
        
        # Job Stress + Sleep: SPECIFIC
        if 'job_stress' in situations and 'sleep_problem' in situations:
            return "kamu sedang mengalami kerja yang tidak sehat sampai stresnya terbawa ke rumah dan mengganggu tidur. Saran dari aku, buat batas jam kerja yang jelas, siapkan rutinitas untuk menutup hari, dan pertimbangkan apakah pekerjaan ini masih sepadan untuk kesehatan mental kamu."
        
        # ===== SINGLE SITUATIONS =====
        if topic == 'friendship' or 'friendship_exclusion' in situations:
            return "kamu sedang merasa belum punya tempat yang benar-benar aman di lingkungan teman. Saran dari aku, mulai dari satu orang yang paling terasa aman dan tanggapi satu bagian kecil dari obrolan, tanpa memaksa diri langsung masuk ke kelompok besar."

        if topic == 'family' or 'parent_pressure' in situations:
            return "kamu sedang menghadapi tekanan keluarga yang membuat usaha kamu terasa tidak dilihat. Saran dari aku, pilih waktu bicara yang lebih tenang, gunakan kalimat yang fokus pada perasaan kamu, atau mulai lewat pesan singkat kalau bicara langsung terasa sulit."

        if topic == 'future' and ('uncertain_future' in situations or 'future_anxiety' in situations):
            return "kamu sedang bingung soal arah hidup dan membandingkan perjalananmu dengan orang lain. Saran dari aku, jangan paksa diri menjawab semuanya sekaligus; pilih satu hal kecil untuk dicoba dulu, lalu evaluasi dari pengalaman itu."
        
        # EDUCATION TOPICS
        if 'exam_coming' in situations:
            if fear == 'fear_of_failure':
                return "kamu sedang mengalami anxiety berlebihan tentang ujian yang akan datang karena takut gagal. Saran dari aku kamu harus belajar dengan fokus tapi juga istirahat cukup, karena otak yang lelah tidak bisa absorb informasi dengan baik."
            return "kamu sedang mengalami tekanan ujian yang membuat pikiran jadi tegang. Saran dari aku kamu harus break sejenak dari belajar, ambil nafas dalam, dan ingat bahwa usaha kamu sudah cukup."
        
        if 'bad_grades' in situations:
            if fear == 'fear_of_failure' or fear == 'shame':
                return "kamu sedang mengalami rasa gagal dan malu karena nilai tidak sesuai harapan, padahal nilai itu bukan ukuran kemampuan kamu. Saran dari aku kamu harus fokus ke pembelajaran berikutnya, bukan terus dwell di nilai lama."
            return "kamu sedang mengalami kecewa dengan hasil akademik. Saran dari aku kamu harus lihat apa yang menjadi hambatan dan cari bantuan, karena belajar dengan support lebih efektif."
        
        if 'school_payment' in situations:
            if len(situations) > 1 and 'sleep_problem' in situations:
                return "kamu sedang mengalami double pressure: ujian plus tekanan finansial yang membuat pikiran tidak bisa tenang. Saran dari aku kamu harus pisahkan prioritas - ujian hari ini, pembayaran bisa dibicarakan setelah ujian selesai."
            return "kamu sedang mengalami tekanan finansial tentang biaya sekolah, dan ini biasanya bukan hanya soal uang tapi juga rasa bersalah pada keluarga. Saran dari aku kamu harus bicarakan dengan orang tua, cari opsi cicilan atau beasiswa bersama-sama."
        
        # CAREER TOPICS
        if 'job_stress' in situations:
            return "kamu sedang mengalami burnout dari pekerjaan yang menekan, dan ini sudah memengaruhi kesehatan mental kamu. Saran dari aku, buat batas yang jelas antara jam kerja dan waktu pribadi, lalu kurangi membawa stres kerja ke rumah."
        
        if 'job_conflict' in situations:
            return "kamu sedang mengalami konflik dengan atasan atau rekan kerja yang membuat lingkungan kerja tidak nyaman. Saran dari aku kamu harus coba komunikasi yang jelas atau pertimbangkan mencari lingkungan kerja yang lebih supportive."
        
        if 'interview_fail' in situations:
            if fear == 'fear_of_inadequacy':
                return "kamu sedang meragukan diri setelah interview gagal, dan itu membuat kamu mempertanyakan kemampuan sendiri. Saran dari aku, ingat bahwa satu interview gagal bukan berarti kamu tidak mampu. Catat pelajarannya, lalu coba lagi dengan persiapan yang lebih jelas."
            return "kamu sedang mengalami kekecewaan karena interview tidak berhasil. Saran dari aku kamu harus minta feedback, improve, dan terus apply ke tempat lain tanpa give up."
        
        # RELATIONSHIP TOPICS
        if 'breakup' in situations:
            return "kamu sedang mengalami putus yang nyakitin hati, dan sekarang dunia terasa sepi dan tidak jelas. Saran dari aku kamu harus beri waktu pada diri sendiri untuk heal, jangan langsung cari pengalihan atau orang baru."
        
        if 'relationship_conflict' in situations:
            return "kamu sedang mengalami pertengkaran terus-menerus dalam hubungan yang membuat mental kamu tegang. Saran dari aku kamu harus ajak partner communicate tentang apa yang benar-benar jadi masalah, atau pertimbangkan couples counseling."
        
        if 'social_anxiety_shame' in situations:
            if fear == 'fear_of_judgment':
                return "kamu sedang mengalami malu berlebihan tentang bagaimana orang lain menilai kamu, dan ini membuat kamu avoid interaksi sosial. Saran dari aku kamu harus inget bahwa orang lain sebenarnya nggak se-kritis yang kamu bayangkan - mulai dengan small social interactions."
            return "kamu sedang mengalami ketidakpercayaan diri saat bertemu orang karena rasa malu yang mendalam. Saran dari aku kamu harus expose diri sedikit demi sedikit ke situasi sosial, dimulai dari yang comfortable."
        
        # APPEARANCE TOPICS
        if 'acne_problem' in situations:
            if fear == 'fear_of_judgment':
                return "kamu sedang mengalami insecurity tentang jerawat yang membuat kamu overthinking tentang bagaimana orang lain menilai penampilan kamu. Saran dari aku kamu harus skincare konsisten tapi juga ingat bahwa orang lain jauh lebih fokus ke diri mereka sendiri daripada ke jerawat kamu."
            return "kamu sedang mengalami tidak nyaman dengan jerawat di wajah yang mempengaruhi kepercayaan diri. Saran dari aku kamu harus coba skincare routine yang tepat, atau konsultasi dengan dermatolog kalau masalahnya serious."
        
        if 'weight_concern' in situations:
            return "kamu sedang mengalami insecurity tentang berat badan yang membuat kamu tidak percaya diri. Saran dari aku kamu harus fokus ke kesehatan bukan angka - exercise untuk feel good, bukan untuk punish diri sendiri."
        
        if 'beauty_insecurity' in situations:
            return "kamu sedang mengalami ketidakpuasan dengan penampilan yang membuat kamu merasa tidak cukup baik. Saran dari aku kamu harus inget bahwa beauty standard itu liar dan subjektif - appreciate diri sendiri sebagaimana adanya."
        
        # FAMILY TOPICS
        if 'family_conflict' in situations:
            return "kamu sedang mengalami konflik keluarga yang membuat rumah jadi tidak nyaman dan tegang. Saran dari aku kamu harus coba komunikasi yang calm atau minta pihak ketiga yang neutral untuk mediasi."
        
        if 'parent_pressure' in situations:
            return "kamu sedang mengalami tekanan ekspektasi dari orang tua yang membuat kamu merasa terbeban dan nggak bisa be yourself. Saran dari aku kamu harus coba bicarakan dengan orang tua tentang apa yang bener-bener kamu inginkan, bukan apa yang mereka inginkan."
        
        # LONELINESS & FRIENDSHIP
        if 'no_friends' in situations:
            if fear == 'fear_of_abandonment':
                return "kamu sedang mengalami kesepian yang membuat kamu imagine kamu bakal sendirian selamanya, padahal isolasi saat ini bukan prediksi masa depan. Saran dari aku kamu harus mulai connect with satu orang, atau join komunitas dengan interest yang sama."
            return "kamu sedang mengalami kesepian karena tidak punya teman dekat yang bisa kamu percaya. Saran dari aku kamu harus be yourself dulu, quality over quantity, genuine connection akan datang dengan waktu."
        
        if 'friend_conflict' in situations:
            return "kamu sedang mengalami pertengkaran atau distance dengan teman yang membuat hati sedih. Saran dari aku kamu harus clear the air - bicarakan apa yang jadi masalah atau beri waktu sebelum decide end friendship."
        
        # FINANCIAL TOPICS
        if 'payment_issue' in situations:
            return "kamu sedang mengalami beban finansial yang membuat kamu stress dan merasa tidak capable membantu keluarga. Saran dari aku kamu harus make a plan bersama keluarga - list semua debt, prioritize, dan cari cara solve step by step."
        
        # HEALTH TOPICS
        if 'sleep_problem' in situations:
            return "kamu sedang mengalami insomnia karena pikiran terus aktif dengan kekhawatiran. Saran dari aku kamu harus relaxation technique seperti deep breathing atau meditation sebelum tidur, dan avoid screen 30 menit sebelumnya."
        
        # FUTURE & UNCERTAINTY
        if 'uncertain_future' in situations or 'future_anxiety' in situations:
            return "kamu sedang mengalami anxiety tentang masa depan karena nggak tahu arah atau pilihan apa yang harus diambil. Saran dari aku kamu harus focus ke saat ini dulu, bukan overthink masa depan yang masih jauh. Satu step at a time."
        
        # SELF-ESTEEM - only when no other situation matches
        if not situations or (not situations and analysis.primary_emotion == 'shame'):
            if fear == 'fear_of_inadequacy':
                return "kamu sedang mengalami rasa nggak layak dan nggak cukup yang membuat kamu doubt semua achievement kamu. Saran dari aku kamu harus list sedikit-sedikit hal yang udah kamu achieve atau kamu bagus, remind diri sendiri kalau kamu NOT inadequate."
            return "kamu sedang mengalami low self-worth yang membuat kamu nggak percaya diri sama diri sendiri. Saran dari aku kamu harus practice self-compassion - treat yourself sama cara kamu treat friend yang kamu sayangi."
        
        # Generic fallback based on emotion
        if analysis.primary_emotion == 'anxiety':
            return "kamu sedang mengalami overthinking tentang hal yang belum tentu terjadi. Saran dari aku kamu harus ground yourself ke present moment, bukan terus anticipate kemungkinan buruk."
        
        if analysis.primary_emotion == 'sadness':
            return "kamu sedang mengalami sedih dan mersasa down. Saran dari aku kamu harus allow yourself untuk feel, jangan repress, tapi juga reach out ke people yang care tentang kamu."
        
        # Generic fallback
        return ""
    
    # =====================================================================
    # RESPONSE COMPONENTS
    # =====================================================================
    
    def _create_reflection(self, analysis: AnalysisResult, user_message: str) -> str:
        """Reflect back user's situation with specific details - natural, personal reflection"""
        if not analysis.situations:
            return ""
        
        # Translate situations to natural Indonesian
        situation_names = []
        for sit, conf in analysis.situations[:2]:
            # Try direct translation first
            if sit in self.situation_translations:
                situation_names.append(self.situation_translations[sit])
            else:
                situation_names.append("situasi yang sedang kamu hadapi")
        
        # Build natural reflection based on number of situations
        if len(situation_names) == 1:
            # Single situation: more personal reflection
            return f"Jadi {situation_names[0]}, gitu. Aku paham itu berat."
        else:
            # Multiple situations: acknowledge the overwhelm
            sit_str = " dan ".join(situation_names)
            return f"Jadi {sit_str}. Itu datang bersamaan, wajar kalau kamu merasa kewalahan."
    
    def _acknowledge_emotion(self, emotion: str) -> str:
        """Acknowledge the primary emotion"""
        emotion_acknowledgments = {
            'anxiety': "Rasa khawatir dan cemas itu natural.",
            'sadness': "Pasti sedih banget dengan situasi ini.",
            'shame': "Ada rasa malu yang dalam, itu aku paham.",
            'guilt': "Ada beban rasa bersalah yang kamu bawa.",
            'insecurity': "Rasa nggak percaya diri itu nyata.",
            'loneliness': "Kesepian itu terasa berat.",
            'fear': "Ada ketakutan yang mendalam di sini.",
            'overwhelm': "Terasa kewalahan dengan semuanya.",
            'exhaustion': "Energi kamu udah habis.",
        }
        
        return emotion_acknowledgments.get(emotion, "Perasaan kamu valid.")
    
    def _link_situation_to_emotion(self, analysis: AnalysisResult) -> str:
        """Link situation to emotion, show understanding"""
        if not analysis.situations or not analysis.primary_emotion:
            return ""
        
        situation = analysis.situations[0][0]
        emotion = analysis.primary_emotion
        
        links = {
            ('breakup', 'sadness'): "Putus dari pacar pasti nyakitin hati.",
            ('breakup', 'fear_of_abandonment'): "Ditinggal orang yang kita sayangi itu nyakitin banget.",
            ('exam_coming', 'anxiety'): "Ujian yang akan datang pasti bikin cemas.",
            ('bad_grades', 'shame'): "Nilai jelek bikin malu dan kecil di mata sendiri.",
            ('job_stress', 'exhaustion'): "Kerja yang berat bikin tenaga habis.",
            ('acne_problem', 'shame'): "Jerawat bikin malu ketemu orang.",
            ('weight_concern', 'insecurity'): "Berat badan bikin nggak percaya diri.",
            ('no_friends', 'loneliness'): "Tidak ada teman bikin sendirian dan sepi.",
        }
        
        return links.get((situation, emotion), "Situasi ini pasti berat.")
    
    def _recognize_fear(self, fear: str) -> str:
        """Recognize underlying fear in natural language"""
        fear_recognitions = {
            'fear_of_abandonment': "takut ditinggal",
            'fear_of_rejection': "takut nggak diterima",
            'fear_of_inadequacy': "takut nggak cukup",
            'fear_of_failure': "takut gagal",
            'fear_of_judgment': "takut dinilai orang lain",
            'fear_of_change': "takut sesuatu berubah",
            'fear_of_future': "takut tentang masa depan",
        }
        
        return fear_recognitions.get(fear, "takut sesuatu")
    
    def _normalize_feelings(self, emotion: str, situations: List[Tuple[str, float]]) -> str:
        """Normalize that these feelings are common"""
        normalizations = [
            "Rasa kayak ini emang banyak orang alami.",
            "Kamu nggak sendirian yang merasa gini.",
            "Ini adalah respon normal dari situasi yang berat.",
            "Banyak orang dalam posisi seperti kamu.",
            "Perasaan ini wajar dan masuk akal.",
        ]
        
        return random.choice(normalizations)
    
    def _create_interpretation(self, analysis: AnalysisResult, user_message: str) -> str:
        """
        Create interpretation based on MEANING EXTRACTION (Phase 2).
        First use reasoning_engine's extracted meaning, then fallback to patterns.
        """
        # PHASE 2: Use meaning extracted from reasoning engine if available
        if hasattr(analysis, 'meaning') and analysis.meaning:
            return analysis.meaning
        
        user_lower = user_message.lower()
        
        # Fallback: Extract what user really needs/fears
        if analysis.primary_fear and analysis.situations:
            situation = analysis.situations[0][0]
            fear = analysis.primary_fear
            
            # MAP: situation + fear = meaning
            meaning_map = {
                ('exam_coming', 'fear_of_failure'): "yang sedang terjadi adalah takut gagal ujian yang akan datang membuat kamu panik",
                ('payment_issue', 'fear_of_inadequacy'): "yang sedang terjadi adalah beban finansial membuat kamu merasa tidak cukup atau gagal menolong keluarga",
                ('sleep_problem', 'anxiety'): "kepikiran tentang masalah membuat otak kamu terus aktif sampai susah tidur",
                ('bad_grades', 'shame'): "nilai jelek membuat kamu merasa malu dan meragukan kemampuan diri sendiri",
                ('job_stress', 'emotional_exhaustion'): "kerja yang toxic sudah menguras tenaga mental kamu sampai nggak bersisa",
                ('acne_problem', 'shame'): "jerawat membuat kamu nggak percaya diri dan takut orang lain menilai penampilan kamu",
                ('no_friends', 'loneliness'): "tidak ada teman membuat kamu merasa sendirian dan ditinggal orang lain",
                ('breakup', 'fear_of_abandonment'): "putus membuat kamu menghadapi rasa kehilangan dan ditinggal orang yang kamu sayangi",
            }
            
            # Check if we have a specific meaning mapping
            for (sit_key, fear_key), meaning in meaning_map.items():
                if sit_key in situation and fear_key == fear:
                    return meaning
            
            # FALLBACK: Build generic meaning from situation + fear
            return f"ada kombinasi antara situasi yang berat dan ketakutan yang nyata"
        
        # If no fear or situation, extract meaning from emotion patterns
        if 'gabisa tidur' in user_lower or 'nggak tidur' in user_lower:
            return "kepikiran terus-terusan membuat otak kamu nggak bisa stop dan tidur jadi sulit"
        
        if 'ga lulus' in user_lower or 'gagal' in user_lower:
            return "takut gagal membuat kamu overthinking tentang kemungkinan buruk"
        
        if 'jerawat' in user_lower or 'jelek' in user_lower:
            return "insecure tentang penampilan membuat kamu merasa tidak worthy"
        
        return ""
    
    def _explain_mechanism(self, analysis: AnalysisResult) -> str:
        """Explain WHY this emotion/fear manifests - situation-aware explanations"""
        
        if not analysis.primary_fear or not analysis.situations:
            # Generic explanation by emotion/fear type
            explanations = {
                'anxiety': "Ketika khawatir, otak kamu terus cari jalan keluar dari masalah yang belum tentu terjadi.",
                'shame': "Shame membuat kita pengen menyembunyikan diri dari orang lain karena merasa ada yang salah.",
                'fear_of_abandonment': "Takut kehilangan itu terjadi karena orang itu berarti banget buat kita.",
                'insecurity': "Rasa nggak cukup sering muncul karena kita bandingin diri sama standar yang terlalu tinggi.",
                'emotional_exhaustion': "Ketika terus menanggung beban, energi mental kita habis dan semuanya terasa berat.",
            }
            emotion_or_fear = analysis.primary_emotion or analysis.primary_fear
            return explanations.get(emotion_or_fear, "")
        
        # Situation-specific explanations
        situation = analysis.situations[0][0]
        fear = analysis.primary_fear
        
        mechanisms = {
            ('exam_coming', 'fear_of_failure'): 
                "Ini karena otak kamu automatically teranticipation kegagalan di ujian. Itu protection mechanism yang berlebihan.",
            
            ('payment_issue', 'fear_of_inadequacy'):
                "Tekanan finansial membuat kamu merasa tidak cukup atau tidak mampu menolong orang yang kamu sayangi.",
            
            ('sleep_problem', 'anxiety'):
                "Ketika overthinking, otak terus active dan nggak bisa relax. Itu why tidur jadi sulit.",
            
            ('bad_grades', 'shame'):
                "Nilai jelek jadi simbol dari tidak worthiness, bukan hanya masalah akademis. Makanya malu jadi dalam.",
            
            ('acne_problem', 'shame'):
                "Insecure tentang penampilan membuat kamu avoid interaksi. Itu amplify the shame dan loneliness.",
            
            ('no_friends', 'loneliness'):
                "Ketika sendirian, brain kamu jadi hyperfocus pada kekurangan sosial. Itu why loneliness terasa intense.",
            
            ('breakup', 'fear_of_abandonment'):
                "Putus jadi confirmation dari fear yang udah exist bahwa kamu bakal ditinggal. Itu deep wound.",
        }
        
        # Try to find specific match
        for (sit_key, fear_key), mechanism in mechanisms.items():
            if situation == sit_key and fear == fear_key:
                return mechanism
        
        # Partial match on fear type
        if fear == 'fear_of_failure':
            return "Ketakutan gagal membuat otak kamu terus anticipate hal-hal buruk yang mungkin terjadi."
        if fear == 'fear_of_abandonment':
            return "Ada ketakutan mendalam tentang ditinggal yang membuat kamu sensitif dengan kehadiran orang lain."
        
        return ""
    
    def _generate_insight(self, analysis: AnalysisResult) -> str:
        """Generate meaningful insight from situation"""
        insights = [
            "Yang penting adalah menyadari apa yang sedang terjadi, dan kamu udah mulai sadar.",
            "Seringkali masalah yang kita pikir akan berat ternyata bisa dihadapi step by step.",
            "Ada wisdom dalam setiap kesulitan yang kita lalui.",
            "Perjalanan untuk memahami diri sendiri adalah proses yang memakan waktu dan itu totally okay.",
        ]
        
        return random.choice(insights)
    
    def _offer_light_support(self, analysis: AnalysisResult) -> str:
        """Offer supportive guidance"""
        supports = [
            "Yang penting sekarang adalah fokus ke hal yang kamu bisa kontrol hari ini.",
            "Tidak ada tekanan untuk solve semuanya sekarang. Step by step aja.",
            "Kamu udah strong untuk deal dengan ini, trust yourself.",
            "Ambil satu langkah kecil, dan itu sudah cukup.",
        ]
        
        return random.choice(supports)
    
    def _validate_situation(self, analysis: AnalysisResult) -> str:
        """Validate the situation before giving advice"""
        if analysis.situations:
            sit = analysis.situations[0][0]
            validations = {
                'exam_coming': "Ujian memang bikin stress dan normal kalau kamu khawatir.",
                'job_stress': "Kerja yang toxic memang berat dan valid untuk merasa kewalahan.",
                'bad_grades': "Nilai jelek memang bikin kecil hati, tapi bukan define kemampuan kamu.",
                'acne_problem': "Jerawat emang bikin nggak PD, tapi temporary dan bisa diobati.",
            }
            
            return validations.get(sit, "Perasaan kamu totally valid.")
        
        return ""
    
    def _get_practical_steps(self, analysis: AnalysisResult) -> List[str]:
        """Get practical, actionable steps for advice mode - highly context aware per topic"""
        message_text = analysis.user_message.lower() if hasattr(analysis, 'user_message') else ""
        
        if not analysis.situations:
            # No situations detected, use general steps
            return [
                "1. Identifikasi apa yang benar-benar jadi masalah utama, bukan semuanya.",
                "2. Buat plan kecil yang feasible untuk hari ini.",
                "3. Reach out ke someone yang kamu trust untuk support."
            ]
        
        situations_list = [s[0] for s in analysis.situations]
        situation = situations_list[0]
        
        # ===== COMBINED SITUATIONS - PRIORITIZE THESE FIRST =====
        
        # Acne + Social Anxiety - SPECIFIC STEPS
        if 'acne_problem' in situations_list and 'social_anxiety_shame' in situations_list:
            return [
                "1. SKINCARE ROUTINE: Start simple - gentle cleanser, moisturizer, sunscreen. Consistency di sini penting untuk confidence.",
                "2. GRADUAL SOCIAL EXPOSURE: Begin dengan social situations yang comfortable (1-on-1 dgn teman, online chat), bukan langsung crowd.",
                "3. BREAK THE CYCLE: Stress membuat jerawat lebih parah. Jadi minimize stress melalui social interaction paradoxically membantu cure jerawat."
            ]
        
        # Exam + Payment
        if 'exam_coming' in situations_list and ('payment_issue' in situations_list or 'school_payment' in situations_list):
            return [
                "1. PRIORITIZE EXAM: Fokus 100% ke ujian sekarang (3-7 hari depan). Financial stress bisa dihandle setelah.",
                "2. SPLIT ATTENTION: Pisahkan mental energy - study time pure for exam, problem-solving time untuk pembayaran.",
                "3. COMMUNICATE EARLY: Bilang ke keluarga/sekolah tentang pembayaran issue sekarang, jadi mereka prepare solusi untuk setelah ujian."
            ]
        
        # Exam + Sleep
        if 'exam_coming' in situations_list and 'sleep_problem' in situations_list:
            return [
                "1. PRIORITIZE SLEEP: Sacrifice last-minute study untuk sleep dulu. Tired brain cannot focus atau retain info.",
                "2. WIND DOWN ROUTINE: 30 menit sebelum tidur: no phone, deep breathing, maybe gentle stretching atau reading.",
                "3. ACCEPT IMPERFECTION: Satu malam kurang tidur tidak akan destroy ujian kamu. Trust in what kamu sudah study."
            ]
        
        # Job Stress + Sleep
        if 'job_stress' in situations_list and 'sleep_problem' in situations_list:
            return [
                "1. WORK BOUNDARY: Set firm hours - kerja stops at X o'clock. No work calls/email setelah jam itu.",
                "2. TRANSITION RITUAL: Between work dan sleep - exercise, shower, hobi - helps mind shift dari 'work mode'.",
                "3. RECONSIDER JOB: Kalau job consistently affecting sleep dan health, maybe it's not worth it. Start job search."
            ]
        
        # ============ EDUCATION TOPICS ============
        if situation == 'exam_coming':
            return [
                "1. Buat jadwal study yang realistis - fokus ke materi yang paling challenging.",
                "2. Latihan dengan soal-soal, bukan hanya baca teori. Belajar aktif biasanya lebih efektif.",
                "3. Jamin tidur cukup malam sebelum ujian - otak yang fresh lebih absorb informasi."
            ]
        
        if situation == 'bad_grades':
            return [
                "1. Analyze apa yang menjadi hambatan - sulit paham materi, atau kurang study time?",
                "2. Reach out ke guru atau senior yang bisa bantu explain, don't struggle alone.",
                "3. Fokus ke next exam/test, jangan terus dwell di nilai lama. Forward looking mindset."
            ]
        
        if situation == 'school_payment':
            # Check if combined with sleep problem
            if 'sleep_problem' in [s[0] for s in analysis.situations]:
                return [
                    "1. PRIORITAS: Fokus ke ujian kamu hari ini 100%, pikiran pembayaran off dulu.",
                    "2. SETELAH ujian: Bicarakan dengan orang tua tentang payment options - cicilan, beasiswa, bantuan.",
                    "3. MAKE A PLAN: Target kapan bisa bayar dan step-by-step gimana caranya."
                ]
            return [
                "1. Jangan simpen masalah ini sendiri - bicarakan dengan orang tua/keluarga dengan jujur.",
                "2. Explore options: Cicilan ke sekolah, beasiswa, bantuan dari keluarga lain, atau part-time income.",
                "3. Buatkan timeline dan plan: Kapan bisa bayar, dari mana uangnya, dan step apa yang perlu diambil."
            ]
        
        # ============ CAREER TOPICS ============
        if situation == 'job_stress':
            return [
                "1. SET BOUNDARIES: Kerja hours berakhir pada jam tertentu. Pulang kerja, HP off dari work chat.",
                "2. FIND JOY OUTSIDE WORK: Minimal 30 menit sehari untuk hobby atau exercise. Mental health maintenance.",
                "3. COMMUNICATE: Bicarakan dengan atasan tentang beban kerja yang nggak realistic. Minta adjustment."
            ]
        
        if situation == 'job_conflict':
            return [
                "1. Coba komunikasi 1-on-1 dengan atasan/rekan kerja - clarify apa yang jadi masalah dan expect.",
                "2. Jangan burn bridge - professional communication, bukan emosional outburst.",
                "3. Kalau nggak improve, consider switching tim atau cari pekerjaan lain yang lebih supportive."
            ]
        
        if situation == 'interview_fail':
            return [
                "1. REQUEST FEEDBACK: Tanya ke recruiter atau interviewer apa yang kurang - belajar dari sini.",
                "2. PRACTICE: Do mock interviews dengan friend, improve soft skills dan technical knowledge.",
                "3. APPLY LAGI: Satu interview gagal bukan bukti kamu nggak capable. Terus apply dengan confidence."
            ]
        
        # ============ RELATIONSHIP TOPICS ============
        if situation == 'breakup':
            return [
                "1. ALLOW YOURSELF TO FEEL: Sedih, marah, semua feelings itu valid. Don't rush healing.",
                "2. NO CONTACT: Jangan contact ex, don't check socials. Give clean break untuk move on.",
                "3. LEAN ON PEOPLE WHO CARE: Spend time dengan teman/keluarga, jangan isolate diri."
            ]
        
        if situation == 'relationship_conflict':
            return [
                "1. HAVE THE TALK: Bicarakan dengan partner apa yang benar-benar jadi issue - tidak blame tapi honest.",
                "2. LISTEN: Jangan hanya vent, dengarkan juga perspective partner. Understand both sides.",
                "3. DECIDE: Mau compromis dan kerja untuk relationship, atau perlu break? Tapi decide together."
            ]
        
        if situation == 'social_anxiety_shame':
            return [
                "1. START SMALL: Expose diri ke social situations yang manageable - cafe, kelas, gathering kecil.",
                "2. PRACTICE SELF-COMPASSION: Talk to yourself like kamu talk to a good friend, bukan inner critic.",
                "3. REMEMBER: Orang lain jauh lebih fokus ke diri mereka sendiri daripada judge kamu. Kamu overthinking."
            ]
        
        # ============ APPEARANCE TOPICS ============
        if situation == 'acne_problem':
            return [
                "1. SKINCARE ROUTINE: Keep it simple - cleanser, moisturizer, sunscreen. Consistency > kompleks produk.",
                "2. NO PICKING: Jangan squeeze atau touch jerawat terus. Biarkan sembuh natural atau konsultasi dermatolog.",
                "3. MENTAL HEALTH: Jerawat temporary, kamu tetap worthy. Stop linking appearance ke self-worth."
            ]
        
        if situation == 'weight_concern':
            return [
                "1. FOCUS ON HEALTH: Exercise karena feel good, bukan punishment. Choose activity yang kamu enjoy.",
                "2. BALANCED EATING: Jangan extreme diet. Makan sehat tapi also allow yourself treats.",
                "3. STOP COMPARING: Social media body standards itu lie. Appreciate your own body exactly as is."
            ]
        
        if situation == 'beauty_insecurity':
            return [
                "1. CHALLENGE BEAUTY STANDARD: Realize beauty itu subjective dan constantly changing. There's no 'one right way'.",
                "2. APPRECIATE YOURSELF: List things your body CAN DO, bukan hanya gimana tampilannya.",
                "3. REDUCE SOCIAL MEDIA: Limit exposure ke filtered images dan comparison. Protect mental health."
            ]
        
        # ============ FAMILY TOPICS ============
        if situation == 'family_conflict':
            return [
                "1. CALM DOWN DULU: Jangan argue saat emosi tinggi. Wait sampai everyone cool off.",
                "2. COMMUNICATE RESPECTFULLY: Bicarakan apa yang jadi masalah tanpa blame. 'Aku merasa...' bukan 'Kamu selalu...'",
                "3. FIND COMMON GROUND: Semua pihak punya need. Cari compromise yang bisa satisfy semua orang."
            ]
        
        if situation == 'parent_pressure':
            return [
                "1. HAVE HONEST CONVERSATION: Tell orang tua apa yang bener-bener kamu mau, bukan apa yang mereka expect.",
                "2. EXPLAIN YOUR REASONING: Jangan hanya bilang 'aku mau ini', tapi explain kenapa dan rencana kamu.",
                "3. BUILD TRUST: Show melalui action bahwa kamu serious dan capable dengan pilihan kamu sendiri."
            ]
        
        # ============ LONELINESS & FRIENDSHIP ============
        if situation == 'no_friends':
            return [
                "1. START WITH ONE: Jangan cari 10 teman. Focus ke satu person yang connection-nya genuine.",
                "2. JOIN COMMUNITIES: Find groups dengan interest yang sama - hobby, class, volunteer, gaming, etc.",
                "3. BE YOURSELF: Authentic connection datang dari being yourself, bukan trying hard to fit in."
            ]
        
        if situation == 'friend_conflict':
            return [
                "1. CLEAR THE AIR: Reach out, bicarakan apa yang jadi masalah. Maybe ada misunderstanding.",
                "2. APOLOGIZE IF NEEDED: Tapi also be honest kalau kamu rasa kamu nggak salah.",
                "3. TAKE TIME: Kalau masih panas, give it time. Sometimes friendship needs space untuk heal."
            ]
        
        # ============ FINANCIAL TOPICS ============
        if situation == 'payment_issue':
            return [
                "1. FACE THE SITUATION: List semua hutang/payment yang outstanding dan priority mana yang urgent.",
                "2. MAKE A PLAN: Dari mana uang bisa datang? Side income, cut expenses, atau minta bantuan?",
                "3. COMMUNICATE: Bicarakan dengan creditor/keluarga tentang situation dan payment plan kamu."
            ]
        
        # ============ HEALTH TOPICS ============
        if situation == 'sleep_problem':
            return [
                "1. CONSISTENT SCHEDULE: Tidur dan bangun jam yang sama setiap hari, even weekends.",
                "2. WIND DOWN: No screens 30 menit sebelum tidur. Try deep breathing, meditation, atau reading.",
                "3. ENVIRONMENT: Kamar harus cool, dark, dan quiet. Invest ke comfortable pillow/bedsheet."
            ]
        
        # ============ FUTURE & UNCERTAINTY ============
        if situation == 'uncertain_future' or situation == 'future_anxiety':
            return [
                "1. FOCUS ON NOW: Stop overthinking tahun depan atau 5 tahun depan. What can kamu do today?",
                "2. EXPLORE GRADUALLY: Try different things, tidak harus decide semuanya sekarang.",
                "3. TALK TO PEOPLE: Mentors, counselor, orang yang udah go through similar path. Learn dari mereka."
            ]
        
        # ============ SELF-ESTEEM ============
        if not situation or 'self_esteem' in situation:
            return [
                "1. JOURNAL YOUR ACHIEVEMENTS: List kecil apa yang udah kamu achieve atau kamu bagus in.",
                "2. PRACTICE SELF-COMPASSION: Talk to yourself like kamu talk to orang yang kamu sayangin.",
                "3. LIMIT COMPARISON: Reduce time on social media. Focus ke your own progress, bukan orang lain punya."
            ]
        
        # Generic fallback
        return [
            "1. Ambil satu langkah kecil yang bisa kamu lakukan hari ini.",
            "2. Cari support dari orang yang kamu trust.",
            "3. Fokus ke apa yang bisa kamu kontrol, bukan yang tidak."
        ]
    
    def _topic_to_description(self, topic: str) -> str:
        """Convert topic code to human description"""
        descriptions = {
            'relationship': 'hubungan',
            'education': 'sekolah/kuliah',
            'career': 'pekerjaan',
            'finance': 'keuangan',
            'family': 'keluarga',
            'friendship': 'pertemanan',
            'self_esteem': 'percaya diri',
            'appearance': 'penampilan',
            'loneliness': 'kesepian',
            'health': 'kesehatan',
            'future': 'masa depan',
        }
        
        return descriptions.get(topic, topic)
    
    def _get_fallback_response(self, user_message: str) -> str:
        """
        CRITICAL: Generate meaningful fallback response.
        NEVER return empty response.
        """
        fallbacks = [
            "Aku dengar kamu, dan kamu nggak sendiri dalam hal ini.",
            "Cerita kamu penting buat aku. Lanjut cerita lagi kalau ada yang mau kamu sampaikan.",
            "Walau nggak sepenuhnya aku paham, aku tahu ini berat buat kamu.",
            "Aku di sini buat dengarkan dan nemenin kamu.",
            "Thank you sudah percaya cerita ke aku.",
        ]
        
        return random.choice(fallbacks)
