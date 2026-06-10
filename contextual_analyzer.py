"""
Contextual Analyzer - Topic & Situation Detection
Detects what topic user is talking about and what specific situation they face
"""

from typing import Dict, List, Tuple, Optional
import re


class TopicDetector:
    """
    Detects main topic/category of user's issue.
    
    Categories:
    - relationship (romantic)
    - education (school, university, learning)
    - career (job, profession, skills)
    - finance (money, bills, expenses)
    - family (parents, siblings, family dynamics)
    - friendship (friends, social relationships)
    - self_esteem (confidence, worth, identity)
    - appearance (body image, looks, physical)
    - loneliness (isolation, feeling alone)
    - health (physical/mental health)
    - future (career path, life direction, uncertainty)
    """
    
    def __init__(self):
        self.strong_topic_signals = {
            'relationship': [
                'pacar', 'partner', 'pasangan', 'putus', 'mantan', 'selingkuh',
            ],
            'education': [
                'ujian', 'sekolah', 'kuliah', 'kampus', 'nilai', 'raport', 'dosen', 'guru',
            ],
            'career': [
                'kerja', 'pekerjaan', 'kantor', 'atasan', 'boss', 'bos', 'interview', 'resign', 'phk',
            ],
            'finance': [
                'uang', 'duit', 'hutang', 'utang', 'cicilan', 'tagihan', 'bayar',
            ],
            'family': [
                'orang tua', 'ortu', 'ayah', 'ibu', 'mama', 'papa', 'keluarga',
                'di rumah', 'anak orang lain', 'dibandingkan', 'dibandingin',
                'dibanding terus', 'dituntut sukses', 'takut pulang',
            ],
            'friendship': [
                'teman', 'sahabat', 'circle', 'sirkel', 'grup', 'pertemanan',
                'numpang ada', 'masuk obrolan', 'masuk percakapan', 'ngobrol',
                'nongkrong', 'dikucilkan', 'dijauhi',
            ],
            'self_esteem': [
                'nggak layak', 'gak layak', 'tidak layak', 'nggak cukup',
                'tidak cukup', 'minder', 'nilai diri',
            ],
            'appearance': [
                'jerawat', 'acne', 'gendut', 'gemuk', 'kurus', 'wajah',
                'gigi', 'kulit', 'rambut', 'penampilan', 'bentuk tubuh',
            ],
            'loneliness': [
                'kesepian', 'merasa sendiri', 'tidak ada siapa-siapa',
                'nggak ada yang ngerti', 'tidak punya tempat cerita',
                'kosong meskipun ada teman',
            ],
            'health': [
                'sakit', 'dokter', 'rumah sakit', 'insomnia', 'tidak bisa tidur',
                'susah tidur', 'kesehatan', 'psikolog',
            ],
            'future': [
                'masa depan', 'arah hidup', 'tujuan hidup', 'salah jalan',
                'belum tahu mau jadi apa', 'karier ke depan', 'takut tertinggal',
            ],
        }

        self.general_topic_signals = {
            'future': ['bingung', 'takut', 'khawatir', 'cemas', 'tidak tahu', 'nggak tahu'],
            'health': ['capek', 'lelah', 'stres', 'stress', 'panik'],
            'self_esteem': ['percaya diri', 'insecure', 'ragu'],
            'loneliness': ['sendiri', 'sendirian', 'sepi'],
            'appearance': ['malu'],
            'family': ['rumah'],
            'friendship': ['mereka', 'diam'],
        }

        self.topic_conflicts = {
            'future': ['teman', 'circle', 'sirkel', 'numpang ada', 'masuk obrolan', 'di rumah', 'anak orang lain', 'dibandingkan', 'dibandingin'],
            'appearance': ['circle', 'sirkel', 'numpang ada', 'teman', 'masuk obrolan', 'di rumah', 'anak orang lain'],
            'self_esteem': ['circle', 'sirkel', 'numpang ada', 'di rumah', 'anak orang lain'],
            'loneliness': ['di rumah', 'anak orang lain', 'orang tua', 'ayah', 'ibu'],
            'friendship': ['di rumah', 'anak orang lain', 'orang tua', 'ayah', 'ibu'],
        }

        self.topic_patterns = {
            'relationship': {
                'keywords': [
                    'pacar', 'partner', 'pasangan', 'bf', 'gf', 
                    'cinta', 'hubungan', 'pacaran', 'ex', 
                    'putus', 'break up', 'perpisahan',
                    'suami', 'istri', 'suaminya', 'istrinnya',
                    'berubah', 'dingin', 'jauh', 'lama bales',
                    'selingkuh', 'curiga', 'iri', 'cemburu',
                    'komunikasi jelek', 'sering bertengkar',
                    'dia nggak care', 'aku nggak dianggap',
                ],
                'patterns': [
                    r'(pacar|partner|bf|gf|dia|dia sama aku|hubungan kami).{0,40}(bilang|pergi|jauh|berubah|putus|dingin)',
                    r'(putus|break up|break).{0,30}(dan|tapi|sekarang|kemarin|hari ini)',
                    r'(hubungan|relationship).{0,40}(tidak|nggak|gak).{0,20}(baik|bagus|lancar|sama)',
                    r'(pacar|partner|dia).{0,30}(nggak|gak|tidak).{0,20}(care|peduli|perhatian|dianggap)',
                    r'(lama|jarang|sulit).{0,25}(bales|balas|reply|hubungi|chat|kontak)',
                ],
                'confidence': 0.9
            },
            
            'education': {
                'keywords': [
                    'sekolah', 'kuliah', 'universitas', 'kampus',
                    'ujian', 'test', 'exam', 'pr', 'tugas',
                    'nilai', 'grade', 'raport', 'remedial',
                    'guru', 'dosen', 'sekolahan', 'pelajaran',
                    'belajar', 'prestasi', 'jurusan', 'major',
                    'tidak naik kelas', 'mengulang', 'drop out',
                    'biaya sekolah', 'uang sekolah', 'beasiswa',
                    'masuk sma', 'masuk kuliah', 'daftar', 'tes masuk',
                ],
                'patterns': [
                    r'(ujian|test|exam|ulangan).{0,25}(besok|minggu depan|bulan depan|dekat|soon)',
                    r'(nilai|grade|raport|skor).{0,25}(jelek|buruk|nggak|rendah|jelek banget)',
                    r'(sekolah|kuliah|kampus).{0,35}(sulit|berat|capek|stress|banyak tugas)',
                    r'(tidak|nggak|gak).{0,25}(naik|lulus|masuk|diterima)',
                    r'(biaya|uang|bayar).{0,30}(sekolah|kuliah|kampus).{0,20}(belum|nggak|tidak)',
                ],
                'confidence': 0.9
            },
            
            'career': {
                'keywords': [
                    'pekerjaan', 'kerja', 'kerjaan', 'job', 'work',
                    'karir', 'career', 'gaji', 'salary',
                    'boss', 'bos', 'atasan', 'kolega', 'rekan kerja',
                    'resign', 'quit', 'cuti', 'PHK',
                    'nganggur', 'jobless', 'aplikasi kerja',
                    'interview', 'wawancara', 'skills',
                    'presentasi', 'meeting', 'project', 'deadline',
                    'tidak hired', 'ditolak perusahaan', 'telat',
                ],
                'patterns': [
                    r'(pekerjaan|kerja|job|kantor).{0,35}(sulit|berat|capek|stress|toxic|banyak)',
                    r'(boss|atasan|rekan kerja|supervisor).{0,30}(jahat|tidak|galak|menyebalkan|bossy)',
                    r'(ingin|mau|pengen|akan).{0,20}(resign|quit|cuti|stop kerja)',
                    r'(interview|wawancara).{0,25}(gagal|ditolak|tidak lulus|tidak dapat)',
                    r'(gaji|salary|penghasilan).{0,25}(kurang|tidak|rendah).{0,20}(cukup|bagus)',
                ],
                'confidence': 0.85
            },
            
            'finance': {
                'keywords': [
                    'uang', 'money', 'duit', 'rupiah',
                    'hutang', 'debt', 'owe', 'pinjam',
                    'biaya', 'bayar', 'payment', 'cicilan',
                    'miskin', 'bokek', 'boros', 'pengeluaran',
                    'tabungan', 'savings', 'investasi',
                    'tunggakan', 'tagihan', 'berutang',
                    'modal', 'bisnis', 'usaha',
                    'tidak cukup', 'pas-pasan', 'sempit',
                ],
                'patterns': [
                    r'(hutang|piutang|cicilan|tunggakan).{0,30}(banyak|berat|menumpuk)',
                    r'(uang|duit|bokek).{0,25}(tidak|nggak|gak).{0,25}(cukup|ada|tersisa)',
                    r'(belum|nggak).{0,20}(bayar|bisa bayar).{0,20}(biaya|tagihan)',
                    r'(bokek|miskin|sempit|pas pasan).{0,25}(banget|terus|selalu)',
                    r'(pengeluaran|biaya).{0,20}(terlalu|banyak|berat)',
                ],
                'confidence': 0.85
            },
            
            'family': {
                'keywords': [
                    'orang tua', 'ibu', 'ayah', 'bapak', 'mama', 'papa',
                    'ortu', 'parents', 'father', 'mother',
                    'saudara', 'adik', 'kakak', 'abang',
                    'keluarga', 'family', 'rumah',
                    'keributan', 'cekcok', 'berantem', 'bertengkar',
                    'tekanan', 'pressure', 'ekspektasi',
                    'tidak dimengerti', 'diabaikan', 'dimarahi',
                    'mengecewakan', 'tidak bisa', 'kecewa',
                    'dibandingkan', 'dibandingin', 'anak orang lain',
                    'di rumah', 'dituntut sukses', 'takut pulang',
                ],
                'patterns': [
                    r'(orang tua|ibu|ayah|mama|papa).{0,35}(marah|nggak|tidak).{0,25}(setuju|senang|mendukung)',
                    r'(keluarga|saudara|adik|kakak).{0,35}(cekcok|berantem|bertengkar|ribut)',
                    r'(tekanan|pressure|ekspektasi).{0,30}(dari|orang tua|keluarga)',
                    r'(orang tua|keluarga).{0,30}(tidak|nggak|gak).{0,25}(mengerti|support|dukung)',
                    r'(merasa|feel).{0,20}(diabaikan|ditolak).{0,20}(keluarga|orang tua)',
                    r'(dibandingkan|dibandingin|dibanding).{0,40}(anak orang lain|orang lain)',
                    r'(di rumah|rumah).{0,40}(dibandingkan|dibandingin|dibanding|dituntut|dimarahi)',
                    r'(dibandingkan|dibandingin|dibanding).{0,40}(di rumah|keluarga|orang tua|ayah|ibu)',
                ],
                'confidence': 0.9
            },
            
            'friendship': {
                'keywords': [
                    'teman', 'friend', 'teman dekat', 'bestie',
                    'sahabat', 'buddies', 'clique', 'grup',
                    'pertemanan', 'friendship', 'hubungan teman',
                    'ditinggal', 'diisolasi', 'diabaikan', 'dikucilkan',
                    'berantem', 'bertengkar', 'pertengkaran',
                    'gossip', 'gosip', 'dibicarain', 'diejek',
                    'tidak ada teman', 'sendirian', 'aja',
                    'backing stab', 'stabbed', 'betrayed', 'dikhianati',
                    'circle', 'sirkel', 'numpang ada', 'masuk obrolan',
                    'masuk percakapan', 'ngobrol', 'nongkrong',
                ],
                'patterns': [
                    r'(teman|sahabat|bestie).{0,35}(jauh|dingin|berubah|tidak|nggak).{0,20}(peduli|contact|balas)',
                    r'(teman|sahabat).{0,30}(berantem|bertengkar|ribut|putus)',
                    r'(teman|sahabat|bestie).{0,30}(khianat|backing stab|lihat|gosip)',
                    r'(tidak|nggak).{0,25}(punya|ada).{0,20}(teman|sahabat|bestie)',
                    r'(ditinggal|diisolasi|diabaikan|dikucilkan).{0,25}(teman|grup|sahabat)',
                    r'(teman|orang lain|mereka).{0,45}(circle|sirkel|grup)',
                    r'(circle|sirkel|grup).{0,45}(masing-masing|sendiri)',
                    r'(numpang ada|cuma ada|hanya numpang)',
                    r'(nggak|tidak).{0,25}(tahu|tau).{0,35}(masuk|ikut).{0,20}(obrolan|percakapan|ngobrol)',
                    r'(mereka|teman).{0,35}(ngobrol|bercanda).{0,35}(aku|saya).{0,20}(diam|bingung)',
                ],
                'confidence': 0.9
            },
            
            'self_esteem': {
                'keywords': [
                    'percaya diri', 'confidence', 'pede', 'nggak pede',
                    'percaya diri', 'self worth', 'value', 'nilai diri',
                    'nggak cukup', 'nggak layak', 'tidak pantas',
                    'nggak bagus', 'failure', 'gagal', 'loser',
                    'minder', 'malu', 'insecure', 'ragu',
                    'identitas', 'siapa aku', 'tujuan hidup',
                    'imposter syndrome', 'nggak deserve',
                    'kemampuan', 'bakat', 'skill',
                ],
                'patterns': [
                    r'(percaya diri|pede|confidence).{0,30}(tidak|nggak|gak).{0,20}(punya|ada)',
                    r'(nggak|tidak).{0,30}(cukup|layak|bagus|pantas|berharga)',
                    r'(minder|insecure|ragu).{0,30}(banget|selalu|terus)',
                    r'(nggak|tidak|gak).{0,30}(deserve|layak|pantas).{0,20}(dapat|miliki|sukses)',
                    r'(percaya|confidence).{0,20}(pada diri sendiri|dengan diri)',
                ],
                'confidence': 0.8
            },
            
            'appearance': {
                'keywords': [
                    'jerawat', 'acne', 'pimple', 'breakout',
                    'gigi', 'gigi ompong', 'ompong', 'gigi goyang',
                    'berat', 'gemuk', 'gendut', 'badan', 'weight',
                    'jelek', 'nggak cantik', 'nggak ganteng', 'ugly',
                    'rambut', 'kulit', 'penampilan', 'appearance',
                    'mata', 'hidung', 'telinga', 'tangan', 'kaki',
                    'malu', 'embarrassed', 'shame', 'body shame',
                    'diet', 'fitness', 'gym', 'makeup',
                ],
                'patterns': [
                    r'(jerawat|jelek|gendut|gigi).{0,40}(malu|shame|embarrass|tidak nyaman)',
                    r'(penampilan|appearance|badan|berat).{0,40}(nggak|tidak|gak).{0,25}(suka|bagus|nyaman)',
                    r'(jerawat|kulit|rambut|badan).{0,40}(jelek|buruk|tidak).{0,20}(bagus|nyaman)',
                    r'(nggak|tidak|gak).{0,30}(nyaman|percaya diri).{0,20}(penampilan|jerawat|berat)',
                    r'(malu|shame).{0,35}(muncul|ketemu|bertemu).{0,25}(orang|teman|publik)',
                ],
                'confidence': 0.9
            },
            
            'loneliness': {
                'keywords': [
                    'sendirian', 'sepi', 'lonely', 'aja', 'alone',
                    'kesepian', 'isolasi', 'isolation', 'terisolir',
                    'tidak ada teman', 'tidak ada siapa-siapa',
                    'no one cares', 'nggak ada yang care',
                    'diabaikan', 'dilupakan', 'forgotten',
                    'merasa sendiri', 'nggak ada tempat',
                    'nggak fit in', 'tidak cocok', 'outsider',
                ],
                'patterns': [
                    r'(sendirian|sepi|lonely).{0,40}(terus|selalu|banget)',
                    r'(tidak|nggak).{0,30}(punya|ada).{0,25}(teman|orang|siapa)',
                    r'(diabaikan|dilupakan|forgotten|nggak dianggap).{0,25}(semua|orang|teman)',
                    r'(merasa|feel).{0,25}(sendirian|sepi|aja).{0,20}(terus|banget)',
                    r'(nggak|tidak).{0,25}(fit in|cocok|tempat).{0,20}(dimana|dengan siapa)',
                ],
                'confidence': 0.85
            },
            
            'health': {
                'keywords': [
                    'sakit', 'sick', 'ill', 'penyakit', 'disease',
                    'depresi', 'depression', 'anxiety', 'panik',
                    'tidur', 'sleep', 'insomnia', 'tidak bisa tidur',
                    'capek', 'lelah', 'exhausted', 'fatigue',
                    'makan', 'appetite', 'nafsu makan',
                    'stres', 'stress', 'tekanan',
                    'kesehatan mental', 'mental health', 'psikolog',
                    'medicine', 'obat', 'dokter', 'rumah sakit',
                ],
                'patterns': [
                    r'(sakit|penyakit|illness|gangguan).{0,40}(berat|serius|parah)',
                    r'(depresi|anxiety|panik|cemas).{0,40}(terus|sering|banget)',
                    r'(tidur|sleep).{0,30}(tidak bisa|sulit|jadi susah)',
                    r'(capek|exhausted|lelah|kelelahan).{0,40}(terus|banget|selalu)',
                    r'(stres|stress|tekanan).{0,30}(membuat|jadi).{0,20}(sakit|tidak tahan)',
                ],
                'confidence': 0.85
            },
            
            'future': {
                'keywords': [
                    'masa depan', 'future', 'nanti', 'nanti',
                    'jalan', 'path', 'direction', 'arah', 'langkah',
                    'takut', 'khawatir', 'cemas', 'anxious',
                    'rencana', 'plan', 'goals', 'tujuan',
                    'tidak tahu', 'bingung', 'lost', 'tersesat',
                    'akan jadi apa', 'bisa apa', 'bisa jadi apa',
                    'pilihan', 'memilih', 'keputusan', 'decision',
                    'kemungkinan buruk', 'worst case', 'takut gagal',
                ],
                'patterns': [
                    r'(masa depan|future|nanti).{0,40}(takut|khawatir|cemas|tidak yakin)',
                    r'(tidak|nggak).{0,30}(tahu|paham|mengerti).{0,30}(arah hidup|tujuan|masa depan|akan jadi apa|mau jadi apa)',
                    r'(bingung|lost|tersesat).{0,30}(tentang|dengan).{0,20}(masa depan|arah)',
                    r'(takut|khawatir|cemas).{0,30}(gagal|salah|buruk|worst case)',
                    r'(tidak).{0,30}(punya|ada).{0,20}(rencana|tujuan|arah)',
                ],
                'confidence': 0.85
            },
        }
    
    def detect(self, user_message: str) -> Tuple[Optional[str], float]:
        """
        Detect topic from user message.
        Returns: (topic_name, confidence_score)
        """
        user_lower = user_message.lower()
        weighted_scores = self._weighted_topic_scores(user_lower)
        best_topic = None
        best_confidence = 0
        
        for topic_name, topic_config in self.topic_patterns.items():
            confidence = 0
            
            # Check keywords
            keyword_matches = 0
            for keyword in topic_config['keywords']:
                if keyword in user_lower:
                    keyword_matches += 1
            
            if keyword_matches > 0:
                confidence = min(keyword_matches * 0.15, 0.6)
            
            # Check patterns
            for pattern in topic_config['patterns']:
                if re.search(pattern, user_lower):
                    confidence = min(confidence + 0.35, 1.0)
                    break
            
            # Apply base confidence
            if confidence > 0:
                confidence = min(confidence * topic_config['confidence'], 1.0)
            
            confidence = min(confidence + weighted_scores.get(topic_name, 0), 1.0)

            if confidence > best_confidence:
                best_confidence = confidence
                best_topic = topic_name
        
        if best_confidence < 0.25:
            return None, best_confidence

        return best_topic, best_confidence

    def _weighted_topic_scores(self, user_lower: str) -> Dict[str, float]:
        scores = {topic: 0.0 for topic in self.topic_patterns.keys()}

        for topic, signals in self.strong_topic_signals.items():
            for signal in signals:
                if signal in user_lower:
                    scores[topic] += 0.25

        for topic, signals in self.general_topic_signals.items():
            for signal in signals:
                if signal in user_lower:
                    scores[topic] += 0.05

        for topic, conflicts in self.topic_conflicts.items():
            for signal in conflicts:
                if signal in user_lower:
                    scores[topic] -= 0.18

        if ('teman' in user_lower or 'mereka' in user_lower) and ('ngobrol' in user_lower or 'obrolan' in user_lower):
            scores['friendship'] += 0.35
            scores['future'] -= 0.25

        if ('di rumah' in user_lower or 'rumah' in user_lower) and ('dibanding' in user_lower or 'anak orang lain' in user_lower):
            scores['family'] += 0.45
            scores['future'] -= 0.25
            scores['self_esteem'] -= 0.15

        if ('circle' in user_lower or 'sirkel' in user_lower or 'numpang ada' in user_lower) and 'teman' in user_lower:
            scores['friendship'] += 0.45
            scores['appearance'] -= 0.25

        return {topic: max(0.0, score) for topic, score in scores.items()}


class SituationDetector:
    """
    Detects specific situation/problem user is facing.
    Examples:
    - "sudah diputus pacar"
    - "belum bayar biaya sekolah"
    - "besok ujian"
    - "banyak jerawat di wajah"
    """
    
    def __init__(self):
        self.situation_patterns = {
            # RELATIONSHIP
            'breakup': {
                'keywords': ['putus', 'break up', 'perpisahan', 'breaking up', 'putus sama pacar'],
                'patterns': [
                    r'(putus|break up|perpisahan|breaking up)',
                    r'(pacar|partner|bf|gf|dia).{0,20}(putus|pergi|tinggal)',
                ],
            },
            'relationship_distance': {
                'keywords': ['jauh', 'dingin', 'lama bales', 'tidak peduli'],
                'patterns': [
                    r'(pacar|partner|dia).{0,20}(jauh|dingin|berubah)',
                    r'(lama|jarang).{0,20}(bales|hubungi)',
                    r'(tidak|nggak).{0,20}(peduli|care|perhatian)',
                ],
            },
            'relationship_conflict': {
                'keywords': ['cekcok', 'pertengkaran', 'bertengkar', 'berantem'],
                'patterns': [
                    r'(sering|selalu).{0,20}(cekcok|bertengkar|berantem)',
                    r'(pertengkaran|argument|fight)',
                ],
            },
            'partner_cheating': {
                'keywords': ['selingkuh', 'curiga', 'tidak setia', 'mencurangi'],
                'patterns': [
                    r'(selingkuh|selingkuhan|cheating)',
                    r'(curiga|tidak setia|mencurangi)',
                ],
            },
            
            # EDUCATION
            'exam_coming': {
                'keywords': ['besok ujian', 'minggu depan ujian'],
                'patterns': [
                    r'(besok|minggu depan|bulan depan).{0,20}(ujian|test|exam)',
                    r'(ujian|test).{0,20}(besok|soon|dekat)',
                ],
            },
            'bad_grades': {
                'keywords': ['nilai jelek', 'raport buruk', 'tidak lulus'],
                'patterns': [
                    r'(nilai|grade|raport).{0,20}(jelek|buruk|nggak)',
                    r'(tidak|nggak).{0,20}(lulus|naik|pass)',
                ],
            },
            'school_payment': {
                'keywords': ['biaya sekolah belum', 'uang sekolah belum'],
                'patterns': [
                    r'(biaya|uang).{0,20}(sekolah|kuliah).{0,20}(belum|nggak)',
                    r'(belum bayar|nggak bayar).{0,20}(sekolah|kuliah)',
                ],
            },
            'school_dropout': {
                'keywords': ['tidak naik kelas', 'drop out'],
                'patterns': [
                    r'(tidak|nggak).{0,20}(naik|lulus|pass)',
                    r'(drop out|stop sekolah)',
                ],
            },
            
            # CAREER
            'job_stress': {
                'keywords': ['kerja stres', 'pekerjaan berat', 'toxic'],
                'patterns': [
                    r'(kerja|pekerjaan|job).{0,30}(stres|berat|toxic)',
                ],
            },
            'job_conflict': {
                'keywords': ['boss jahat', 'rekan kerja tidak enak'],
                'patterns': [
                    r'(boss|atasan|rekan kerja).{0,20}(jahat|tidak|galak)',
                ],
            },
            'job_loss': {
                'keywords': ['nganggur', 'PHK', 'resign'],
                'patterns': [
                    r'(nganggur|jobless|unemployed)',
                    r'(PHK|resign|quit|cuti)',
                ],
            },
            'interview_fail': {
                'keywords': ['interview gagal', 'ditolak perusahaan'],
                'patterns': [
                    r'(interview|wawancara).{0,20}(gagal|ditolak|tidak)',
                ],
            },
            
            # APPEARANCE
            'acne_problem': {
                'keywords': ['jerawat', 'acne', 'jerawat banyak', 'jerawat parah', 'jerawatku'],
                'patterns': [
                    r'(jerawat|acne).{0,30}(banyak|parah|besar|makin|tambah|bertambah)',
                    r'(nggak|tidak|gak).{0,20}(nyaman|percaya diri).{0,20}(jerawat|penampilan)',
                ],
            },
            'teeth_problem': {
                'keywords': ['gigi ompong', 'gigi jelek'],
                'patterns': [
                    r'(gigi|teeth).{0,20}(ompong|jelek|goyang)',
                ],
            },
            'weight_concern': {
                'keywords': ['gemuk', 'gendut', 'berat badan'],
                'patterns': [
                    r'(gendut|gemuk|berat|weight).{0,20}(banget|terus)',
                ],
            },
            'beauty_insecurity': {
                'keywords': ['jelek', 'tidak cantik', 'tidak ganteng'],
                'patterns': [
                    r'(jelek|tidak cantik|tidak ganteng|ugly)',
                ],
            },
            'social_anxiety_shame': {
                'keywords': ['malu', 'malu ketemu', 'tidak percaya diri', 'malu tampil', 'ga pede', 'tidak pede', 'pede bertemu'],
                'patterns': [
                    r'(malu|shame).{0,30}(ketemu|bertemu|tampil)',
                    r'(ga|gak|nggak|tidak).{0,25}(pede|percaya diri).{0,30}(bertemu|ketemu|orang)',
                    r'(tidak|nggak|gak).{0,20}(percaya diri|pede|confident)',
                    r'(malu|minder|insecure).{0,30}(ketemu|bertemu|muka|tampil)',
                    r'(takut|khawatir).{0,30}(orang lain|teman|orang|dinilai|dilihat)',
                ],
            },
            
            # FAMILY
            'parent_pressure': {
                'keywords': ['orang tua tekanan', 'ibu ayah marah', 'dibandingkan', 'dibandingin', 'anak orang lain'],
                'patterns': [
                    r'(orang tua|ibu|ayah).{0,30}(tekanan|pressure|marah)',
                    r'(dibandingkan|dibandingin|dibanding).{0,40}(anak orang lain|orang lain)',
                    r'(di rumah|rumah).{0,40}(dibandingkan|dibandingin|dibanding|dituntut)',
                ],
            },
            'family_conflict': {
                'keywords': ['keluarga cekcok', 'saudara bertengkar'],
                'patterns': [
                    r'(keluarga|saudara).{0,30}(cekcok|bertengkar|berantem)',
                ],
            },
            'parent_unsupported': {
                'keywords': ['orang tua tidak mendukung'],
                'patterns': [
                    r'(orang tua|ibu|ayah).{0,20}(tidak|nggak).{0,20}(support|setuju|mendukung)',
                ],
            },
            
            # FRIENDSHIP
            'friend_abandoned': {
                'keywords': ['teman ditinggal', 'teman diabaikan'],
                'patterns': [
                    r'(teman|friend).{0,30}(ditinggal|diabaikan|jauh)',
                ],
            },
            'friend_betrayal': {
                'keywords': ['teman khianat', 'backing stab'],
                'patterns': [
                    r'(teman|friend).{0,20}(khianat|backing stab|lihat)',
                ],
            },
            'friend_conflict': {
                'keywords': ['teman bertengkar', 'putus teman'],
                'patterns': [
                    r'(teman|friend).{0,20}(bertengkar|berantem|putus)',
                ],
            },
            'no_friends': {
                'keywords': ['tidak ada teman', 'sendirian', 'circle', 'sirkel', 'numpang ada'],
                'patterns': [
                    r'(tidak|nggak).{0,20}ada.{0,20}(teman|friend)',
                    r'(sendirian|aja).{0,20}(terus|selalu)',
                    r'(teman|orang lain|mereka).{0,45}(circle|sirkel|grup)',
                    r'(numpang ada|cuma ada|hanya numpang)',
                ],
            },
            'friendship_exclusion': {
                'keywords': ['circle', 'sirkel', 'numpang ada', 'masuk obrolan', 'masuk percakapan', 'nggak tahu masuk'],
                'patterns': [
                    r'(circle|sirkel|grup).{0,45}(masing-masing|sendiri)',
                    r'(numpang ada|cuma ada|hanya numpang)',
                    r'(nggak|tidak).{0,25}(tahu|tau).{0,35}(masuk|ikut).{0,20}(obrolan|percakapan|ngobrol)',
                    r'(mereka|teman).{0,35}(ngobrol|bercanda).{0,35}(aku|saya).{0,20}(diam|bingung)',
                ],
            },
            
            # FINANCIAL
            'debt_problem': {
                'keywords': ['hutang banyak', 'tunggakan'],
                'patterns': [
                    r'(hutang|tunggakan|cicilan).{0,20}(banyak|berat)',
                ],
            },
            'insufficient_money': {
                'keywords': ['uang tidak cukup', 'bokek'],
                'patterns': [
                    r'(uang|duit|bokek).{0,20}(tidak|nggak).{0,20}(cukup|ada)',
                ],
            },
            
            # FUTURE
            'uncertain_future': {
                'keywords': ['tidak tahu masa depan', 'bingung mau apa'],
                'patterns': [
                    r'(tidak|nggak).{0,20}(tahu|mengerti|paham).{0,20}(arah hidup|tujuan|masa depan|mau jadi apa|akan jadi apa)',
                    r'(bingung|lost|tersesat).{0,20}(mau|akan).{0,25}(jadi apa|ke mana|kemana|hidup|masa depan)',
                    r'(hidup).{0,30}(arah mana|ke mana|kemana|tujuan)',
                ],
            },
            'future_anxiety': {
                'keywords': ['takut masa depan', 'khawatir akan gagal'],
                'patterns': [
                    r'(takut|khawatir).{0,20}(masa depan|gagal|salah|buruk)',
                ],
            },
            
            # HEALTH SITUATIONS
            'sleep_problem': {
                'keywords': ['tidak bisa tidur', 'ga bisa tidur', 'insomnia', 'tidur berantakan'],
                'patterns': [
                    r'(tidak|nggak|ga).{0,20}(bisa|bisa).{0,20}(tidur|sleep)',
                    r'(insomnia|bangun|terus bangun)',
                    r'(tidur).{0,15}(berantakan|hancur|buruk|jelek)',
                    r'(pola tidur|jam tidur).{0,15}(berantakan|kacau|tidak teratur)',
                ],
            },
            'stress_health': {
                'keywords': ['stres kesehatan', 'stress sakit'],
                'patterns': [
                    r'(stres|stress|panik).{0,20}(sakit|kesehatan)',
                ],
            },
        }
    
    def detect(self, user_message: str) -> List[Tuple[str, float]]:
        """
        Detect situations from user message.
        Returns: [(situation_name, confidence_score), ...]
        """
        user_lower = user_message.lower()
        detected_situations = []
        
        for situation_name, situation_config in self.situation_patterns.items():
            confidence = 0
            
            # Check keywords
            for keyword in situation_config['keywords']:
                if keyword in user_lower:
                    confidence = 0.5
                    break
            
            # Check patterns
            for pattern in situation_config['patterns']:
                if re.search(pattern, user_lower):
                    confidence = max(confidence, 0.8)
                    break
            
            if confidence > 0.3:
                detected_situations.append((situation_name, confidence))
        
        # Sort by confidence
        detected_situations.sort(key=lambda x: x[1], reverse=True)
        return detected_situations
