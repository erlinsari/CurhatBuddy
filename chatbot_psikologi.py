import re
from typing import Dict, List, Optional, Tuple

class ThemeManager:
    themes = {
        'teman_curhat': {
            'name': 'Teman Curhat',
            'greeting': 'Hai! Aku teman curhatmu di sini. Cerita aja apa yang lagi mengganjal di pikiranmu, santai aja ya.',
            'supportive': [
                'Wah, pasti capek ya kamu ngejalaninnya.',
                'Iya, aku denger kok. Lanjutin ceritanya kalau kamu masih mau.',
                'Aku di sini buat nemenin kamu.',
                'Kalau kamu mau, aku bisa bantu nyusun lagi apa yang kamu rasain.',
            ],
            'analysis_permission': 'Dari cerita kamu sejauh ini, aku udah mulai nangkep beberapa hal. Boleh nggak aku share dulu apa yang aku rasa? Nanti kalau kamu suka, aku bisa kasih solusi juga.',
            'ask_later': 'Oke, santai aja. Kalau kamu mau aku analisanya nanti, bilang aja ya. Kita bisa lanjut curhat dulu.',
            'no_analysis': 'Gak masalah, kita lanjut curhat aja. Yang penting kamu ngerasa didengerin.',
            'final_thanks': 'Makasih ya udah cerita jujur. Aku ada di sini kalau kamu mau curhat lagi kapan pun.',
            'permission_positive': ['boleh', 'iya', 'yap', 'oke', 'ok', 'yes', 'silakan', 'silahkan', 'ya', 'lanjut'],
            'permission_negative': ['nggak', 'gak', 'tidak', 'nanti', 'belum', 'belum dulu', 'belum aja', 'enggak', 'lebih baik nggak'],
            'ask_for_solution': ['solusi', 'saran', 'bantu', 'cara', 'tips', 'apa yang harus', 'apa baiknya', 'ada ide', 'bisa nggak'],
            'follow_up': 'Kalau kamu mau lanjut, ceritain lagi aja tentang apa yang bikin kamu ngerasa gini.',
        },
        'supportive_sahabat': {
            'name': 'Supportive Sahabat',
            'greeting': 'Hai! Aku di sini buat dengerin semua curhatan kamu, jadi santai aja ceritanya.',
            'supportive': [
                'Gak apa-apa kok kalau kamu ngerasa campur aduk.',
                'Aku denger, dan kamu nggak sendirian.',
                'Lanjut aja kalau kamu masih pengen cerita.',
            ],
            'analysis_permission': 'Menurut aku, aku udah mulai ngumpulin beberapa pola dari cerita kamu. Mau aku share dulu atau kita terusin curhat?',
            'ask_later': 'Santuy, kita lanjut curhat dulu aja. Nanti kalau kamu siap, aku kasih insight ya.',
            'no_analysis': 'Yoi, kita lanjut aja tanpa analisis. Aku tetap di sini buat nemenin.',
            'final_thanks': 'Terima kasih udah percaya curhat di sini. Kapan pun kamu butuh, aku siap.',
            'permission_positive': ['boleh', 'iya', 'oke', 'ok', 'yes', 'silakan', 'ya', 'lanjut'],
            'permission_negative': ['nggak', 'gak', 'tidak', 'nanti', 'belum', 'belum dulu', 'enggak'],
            'ask_for_solution': ['solusi', 'saran', 'bantu', 'cara', 'tips', 'apa yang harus'],
            'follow_up': 'Kalau kamu mau, ceritain lagi soal hari-hari terakhir ini.',
        },
        'coach_santai': {
            'name': 'Coach Santai',
            'greeting': 'Halo! Aku di sini buat dengerin dan bantu kamu ngerapihin perasaan dengan cara yang santai.',
            'supportive': [
                'Sip, kamu udah mulai cerita. Lanjut aja ya.',
                'Keren kamu berani curhat, aku dengerin terus.',
                'Gue di sini buat nemenin kamu sampai kamu ngerasa lebih lega.',
            ],
            'analysis_permission': 'Kalau kamu mau, aku bisa bagi insight dulu. Atau kita terusin curhat sampai kamu ngerasa lebih lega.',
            'ask_later': 'Oke, kita tunda analisis dulu. Curhat aja dulu, aku dengerin.',
            'no_analysis': 'Gapapa, yang penting kamu ngerasa ditemani. Kita bisa analisis nanti kapan aja.',
            'final_thanks': 'Makasih ya udah curhat. Semoga obrolan ini bikin kamu ngerasa agak lebih enteng.',
            'permission_positive': ['boleh', 'iya', 'oke', 'ok', 'yes', 'silakan', 'ya', 'lanjut'],
            'permission_negative': ['nggak', 'gak', 'tidak', 'nanti', 'belum', 'belum dulu', 'enggak'],
            'ask_for_solution': ['solusi', 'saran', 'bantu', 'tips', 'cara', 'apa yang harus'],
            'follow_up': 'Kalau kamu mau, kita bisa bahas lagi bagian mana yang paling ngerepotin.',
        },
        'pendengar_santuy': {
            'name': 'Pendengar Santuy',
            'greeting': 'Eh, santai aja. Cerita apa pun boleh di sini, tanpa dinilai.',
            'supportive': [
                'Aku di sini buat dengerin aja, nggak perlu buru-buru selesai.',
                'Lanjut cerita kalau kamu masih pengen.',
                'Gak apa-apa kalau kamu butuh sedikit waktu buat ngomong.',
            ],
            'analysis_permission': 'Dari cerita kamu, aku ngerasa ada beberapa hal yang bisa dibahas. Mau aku share dulu atau kita tetap santai aja curhat?',
            'ask_later': 'Baiklah, kita curhat dulu aja. Kalau kamu mau, nanti aku bantu rangkum ya.',
            'no_analysis': 'Gak masalah. Kita keep it chill dulu, analisis bisa kapan-kapan.',
            'final_thanks': 'Terima kasih udah cerita. Semoga obrolan ini bikin kamu ngerasa sedikit lebih ringan.',
            'permission_positive': ['boleh', 'iya', 'oke', 'ok', 'yes', 'silakan', 'ya', 'lanjut'],
            'permission_negative': ['nggak', 'gak', 'tidak', 'nanti', 'belum', 'enggak'],
            'ask_for_solution': ['solusi', 'saran', 'bantu', 'tips', 'cara', 'apa yang harus'],
            'follow_up': 'Kamu bisa cerita lagi tentang apa yang masih nempel di pikiranmu.',
        },
        'sahabat_ringan': {
            'name': 'Sahabat Ringan',
            'greeting': 'Yo! Aku siap jadi sahabat curhat yang enak diajak ngobrol kapan pun.',
            'supportive': [
                'Kalem aja, cerita kamu penting buat aku dengerin.',
                'Enggak usah mikirin gaya, bilang aja apa adanya.',
                'Aku nemenin kamu sampai kamu ngerasa lebih enteng.',
            ],
            'analysis_permission': 'Gimana, mau aku share dulu apa yang aku tangkep dari cerita kamu, atau kita terusin aja sampai kamu puas curhat?',
            'ask_later': 'Oke, santai. Curhat dulu deh, solusinya bisa kita bahas nanti.',
            'no_analysis': 'Gak usah dipaksa. Kita curhat dulu aja, aku tetap di sini.',
            'final_thanks': 'Makasih udah cerita. Kapan pun kamu butuh lagi, panggil aja.',
            'permission_positive': ['boleh', 'iya', 'oke', 'ok', 'yes', 'silakan', 'ya', 'lanjut'],
            'permission_negative': ['nggak', 'gak', 'tidak', 'nanti', 'belum', 'enggak'],
            'ask_for_solution': ['solusi', 'saran', 'bantu', 'tips', 'cara', 'apa yang harus'],
            'follow_up': 'Kalau kamu mau, cerita lagi tentang situasi yang bikin kamu nggak enak.',
        },
    }

    @classmethod
    def get_theme(cls, name: str) -> Dict:
        return cls.themes.get(name, cls.themes['teman_curhat'])

    @classmethod
    def list_themes(cls) -> List[str]:
        return list(cls.themes.keys())


class KnowledgeBase:
    def __init__(self):
        self.facts = self._build_facts()
        self.rules = self._build_rules()

    def _build_facts(self) -> Dict[str, Dict]:
        return {
            'G1': {
                'nama': 'Mudah marah/tersinggung',
                'keywords': ['marah', 'emosi', 'tersinggung', 'sensitif', 'kesel', 'baper', 'gampang meledak'],
                'pertanyaan': 'Akhir-akhir ini kamu ngerasa lebih gampang emosi atau tersinggung gak sih?',
            },
            'G2': {
                'nama': 'Perasaan sedih/hampa',
                'keywords': ['sedih', 'hampa', 'kosong', 'nangis', 'murung', 'galau', 'depresi', 'gak berguna', 'putus asa'],
                'pertanyaan': 'Apa kamu belakangan ini sering ngerasa sedih yang dalem banget atau ngerasa kosong gitu aja?',
            },
            'G3': {
                'nama': 'Kesulitan fokus',
                'keywords': ['fokus', 'konsentrasi', 'lupa', 'blank', 'gak nyambung', 'bingung', 'ga fokus', 'mudah lupa'],
                'pertanyaan': 'Kerjaan atau tugasmu keganggu gak sih? Maksudku, kamu jadi susah fokus atau gampang lupa?',
            },
            'G4': {
                'nama': 'Gangguan tidur',
                'keywords': ['tidur', 'insomnia', 'begadang', 'gak bisa tidur', 'bangun tengah malem', 'susah tidur', 'nggak bisa tidur', 'tidur nggak nyenyak'],
                'pertanyaan': 'Pola tidurmu gimana belakangan ini? Sering susah tidur atau malah pengen tidur terus?',
            },
            'G5': {
                'nama': 'Capek fisik',
                'keywords': ['lelah', 'capek', 'lemes', 'lesu', 'nggak ada tenaga', 'letih', 'kaku', 'pusing', 'ogah-gerak'],
                'pertanyaan': 'Kamu ngerasa fisik kamu cepet capek atau kayak nggak ada tenaga belakangan ini?',
            },
            'G6': {
                'nama': 'Hilang minat/kenikmatan',
                'keywords': ['gak ada motivasi', 'gak semangat', 'bosan', 'gak mau ngapa-ngapain', 'hilang minat', 'gak enjoy', 'kayak ga niat'],
                'pertanyaan': 'Kamu masih ngerasa nikmat nggak sama hal-hal yang biasanya bikin kamu seneng?',
            },
            'G7': {
                'nama': 'Sering cemas atau khawatir',
                'keywords': ['cemas', 'khawatir', 'gelisah', 'takut', 'deg-degan', 'panik', 'was-was', 'gelisah terus'],
                'pertanyaan': 'Kamu ngerasa gampang cemas atau khawatir, bahkan untuk hal kecil?',
            },
            'G8': {
                'nama': 'Perubahan nafsu makan',
                'keywords': ['makan banyak', 'makan sedikit', 'nafsu makan', 'gak lapar', 'overeat', 'malas makan', 'makan terus', 'gak selera makan'],
                'pertanyaan': 'Nafsu makanmu gimana, biasanya berubah jadi lebih banyak atau malah sedikit banget?',
            },
            'G9': {
                'nama': 'Menarik diri dari orang lain',
                'keywords': ['menjauh', 'ga mau ketemu', 'sendiri', 'isolasi', 'ga ada energi buat social', 'ngurung diri', 'sosial withdrawal'],
                'pertanyaan': 'Kamu lagi merasa mager buat ketemu orang atau ngerasa pengen sendirian terus?',
            },
            'G10': {
                'nama': 'Mudah putus asa',
                'keywords': ['putus asa', 'gak ada harapan', 'gak ada jalan', 'nyerah', 'capek banget', 'sudah nggak sanggup'],
                'pertanyaan': 'Kadang kamu ngerasa putus asa atau merasa nggak ada harapan buat perbaikan?',
            },
            'G11': {
                'nama': 'Pikiran berputar terus (overthinking)',
                'keywords': ['overthinking', 'kepikiran', 'gak berhenti mikir', 'otak ngaco', 'pusing mikir'],
                'pertanyaan': 'Sering nggak kamu nggak bisa stop mikir, sampai overthinking terus?',
            },
            'G12': {
                'nama': 'Khawatir dinilai orang',
                'keywords': ['malu', 'gak pede', 'takut dinilai', 'gak nyaman', 'gengsi', 'tidak percaya diri'],
                'pertanyaan': 'Kamu ngerasa ribet sama apa kata orang atau takut dinilai salah?',
            },
            'G13': {
                'nama': 'Perasaan bersalah atau menyesal',
                'keywords': ['bersalah', 'salah', 'menyalahkan diri', 'gak pantas', 'menyesal', 'salah sendiri'],
                'pertanyaan': 'Ada perasaan bersalah atau menyesal yang susah dilepas akhir-akhir ini?',
            },
            'G14': {
                'nama': 'Beban tugas/pekerjaan menumpuk',
                'keywords': ['kewalahan', 'deadline', 'kerjaan numpuk', 'tugas numpuk', 'banyak kerjaan', 'stress kerja'],
                'pertanyaan': 'Kerjaanmu lagi numpuk atau kamu lagi ngerasa kewalahan banget sama tugas?',
            },
            'G15': {
                'nama': 'Perubahan mood cepat',
                'keywords': ['nangis terus', 'meledak', 'gak terkendali', 'mood swing', 'mood naik turun'],
                'pertanyaan': 'Kamu ngerasa mood kamu gampang banget berubah, kadang meledak kadang lemes?',
            },
            'G16': {
                'nama': 'Transisi hidup atau perubahan besar',
                'keywords': ['pindah kerja', 'putus', 'pindah rumah', 'transisi', 'mulai baru', 'perubahan hidup'],
                'pertanyaan': 'Ada perubahan besar atau fase baru yang lagi kamu jalani akhir-akhir ini?',
            },
        }

    def _build_rules(self) -> List[Dict]:
        return [
            {
                'nama': 'Depresi Maior (MDD)',
                'deskripsi': 'Ada kecenderungan depresi dengan energi turun, minat berkurang, gangguan tidur, dan perasaan putus asa.',
                'kondisi': ['G2', 'G4', 'G6', 'G8', 'G10'],
                'solusi': 'Mulai dari rutinitas tidur lebih teratur, beri ruang buat hal-hal kecil yang biasanya bikin kamu seneng, dan pertimbangkan bicara ke profesional jika ini sudah mengganggu keseharian.',
            },
            {
                'nama': 'Burnout ringan sampai sedang',
                'deskripsi': 'Tanda-tanda stres berlebihan dari pekerjaan atau tanggung jawab: lelah, sulit fokus, motivasi turun, dan mudah kesal.',
                'kondisi': ['G1', 'G3', 'G5', 'G6', 'G14'],
                'solusi': 'Istirahatkan diri, atur prioritas tugas, batasi jam kerja, dan coba cerita ke teman atau kolega tentang bebanmu.',
            },
            {
                'nama': 'Kecemasan berlebih (Anxiety)',
                'deskripsi': 'Perasaan cemas, khawatir, dan overthinking yang mempengaruhi mood serta kualitas tidur.',
                'kondisi': ['G4', 'G7', 'G11', 'G12'],
                'solusi': 'Latihan napas, tulis faktor yang bikin kamu cemas, dan coba bicara ke orang terdekat agar pikiranmu nggak berputar sendiri.',
            },
            {
                'nama': 'Withdrawal sosial',
                'deskripsi': 'Menjauh dari orang sekitar dan memilih sendiri bisa jadi tanda kamu lagi butuh ruang, tapi juga bisa bikin beban makin berat.',
                'kondisi': ['G5', 'G9', 'G13', 'G15'],
                'solusi': 'Coba mulai dengan ngobrol ringan sama satu orang deket dulu, dan ingatkan diri kalau istirahat sosial itu boleh, tapi jangan sampai kamu merasa terisolasi.',
            },
            {
                'nama': 'Stres hubungan atau emosional',
                'deskripsi': 'Hubungan yang beresiko bikin kamu merasa salah sendiri, bersalah, atau mudah berubah mood.',
                'kondisi': ['G13', 'G15', 'G9', 'G12'],
                'solusi': 'Coba ungkapin perasaanmu yang paling berat ke orang yang kamu percaya, atau catat dulu supaya kamu bisa lihat pola emosi tanpa langsung nyalahin diri.',
            },
            {
                'nama': 'Transisi hidup yang berat',
                'deskripsi': 'Perubahan besar seperti pindah, putus, atau mulai fase baru dapat bikin kamu merasa nggak stabil dan kewalahan.',
                'kondisi': ['G11', 'G14', 'G16', 'G5'],
                'solusi': 'Beri waktu buat adaptasi, atur ekspektasi jadi lebih realistis, dan temani diri dengan rutinitas kecil yang bikin kamu merasa lebih aman.',
            },
        ]

    def get_fact_ids(self) -> List[str]:
        return list(self.facts.keys())

    def get_fact(self, fact_id: str) -> Optional[Dict]:
        return self.facts.get(fact_id)

    def match_keywords(self, text: str) -> List[str]:
        lowered = text.lower()
        matched = []
        for fact_id, content in self.facts.items():
            for kw in content['keywords']:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, lowered):
                    matched.append(fact_id)
                    break
        return matched


class SessionState:
    def __init__(self):
        self.facts: Dict[str, bool] = {}
        self.asked_questions: List[str] = []
        self.history: List[Tuple[str, str]] = []
        self.analysis_requested: bool = False
        self.analysis_shared: bool = False
        self.ready_for_analysis: bool = False

    def update_facts(self, fact_ids: List[str]):
        for fact_id in fact_ids:
            self.facts[fact_id] = True

    def record_message(self, speaker: str, text: str):
        self.history.append((speaker, text))

    def mark_question_asked(self, fact_id: str):
        if fact_id not in self.asked_questions:
            self.asked_questions.append(fact_id)

    def has_asked(self, fact_id: str) -> bool:
        return fact_id in self.asked_questions


class InferenceEngine:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def infer(self, facts: Dict[str, bool]) -> List[Dict]:
        conclusions = []
        for rule in self.knowledge_base.rules:
            satisfied = [fact for fact in rule['kondisi'] if facts.get(fact)]
            if satisfied:
                score = len(satisfied) / len(rule['kondisi'])
                conclusions.append({
                    'rule': rule,
                    'score': score,
                    'satisfied': satisfied,
                    'remaining': [fact for fact in rule['kondisi'] if fact not in satisfied],
                })
        conclusions.sort(key=lambda item: item['score'], reverse=True)
        return conclusions

    def best_candidate(self, facts: Dict[str, bool]) -> Optional[Dict]:
        conclusions = self.infer(facts)
        return conclusions[0] if conclusions else None

    def needs_more_info(self, facts: Dict[str, bool]) -> List[str]:
        candidate = self.best_candidate(facts)
        if not candidate:
            return []
        return candidate['remaining']

    def get_available_conclusions(self, facts: Dict[str, bool]) -> List[Dict]:
        conclusions = self.infer(facts)
        return [item for item in conclusions if item['score'] >= 0.5]


class CurhatBot:
    def __init__(self, theme_name: str = 'teman_curhat'):
        self.theme = ThemeManager.get_theme(theme_name)
        self.kb = KnowledgeBase()
        self.state = SessionState()
        self.engine = InferenceEngine(self.kb)

    def _is_positive_answer(self, text: str) -> bool:
        lowered = text.lower()
        return any(token in lowered for token in self.theme['permission_positive'])

    def _is_negative_answer(self, text: str) -> bool:
        lowered = text.lower()
        return any(token in lowered for token in self.theme['permission_negative'])

    def _wants_solution(self, text: str) -> bool:
        lowered = text.lower()
        return any(token in lowered for token in self.theme['ask_for_solution'])

    def _pick_supportive(self) -> str:
        return self.theme['supportive'][len(self.state.history) % len(self.theme['supportive'])]

    def _best_missing_fact(self) -> Optional[str]:
        missing = self.engine.needs_more_info(self.state.facts)
        for fact_id in missing:
            if not self.state.has_asked(fact_id):
                return fact_id
        for fact_id in missing:
            return fact_id
        all_fact_ids = self.kb.get_fact_ids()
        for fact_id in all_fact_ids:
            if fact_id not in self.state.facts and not self.state.has_asked(fact_id):
                return fact_id
        return None

    def _target_question(self) -> Optional[str]:
        fact_id = self._best_missing_fact()
        if fact_id is None:
            return None
        self.state.mark_question_asked(fact_id)
        return self.kb.get_fact(fact_id)['pertanyaan']

    def _format_analysis(self, conclusion: Dict) -> str:
        rule = conclusion['rule']
        facts = [self.kb.get_fact(fid)['nama'] for fid in conclusion['satisfied']]
        facts_text = ', '.join(facts)
        return (
            f"Dari cerita kamu, aku melihat beberapa pola seperti {facts_text}.\n"
            f"Sepertinya ada kecenderungan: {rule['nama']}.",
            f"{rule['deskripsi']}\n",
            f"Kalau kamu mau, aku bisa bantu kasih solusi ringan.",
        )

    def get_analysis_text(self) -> str:
        conclusions = self.engine.get_available_conclusions(self.state.facts)
        if not conclusions:
            return ('Aku masih rasa belum cukup data buat taruh label yang jelas, tapi dari cerita kamu ada beberapa sinyal stres dan kelelahan. ' 
                    'Kalau kamu mau, kita bisa lanjut ngobrol supaya aku bisa bantu susun apa yang lagi kamu rasakan.')
        lines = []
        for item in conclusions[:2]:
            rule = item['rule']
            satisfied = [self.kb.get_fact(fid)['nama'] for fid in item['satisfied']]
            lines.append(f"- {rule['nama']}: {rule['deskripsi']}\n  (Gejala utama: {', '.join(satisfied)})")
        lines.append('Kalau kamu mau, aku bisa kasih solusi yang santai dan ringan buat coba dicoba sehari-hari.')
        return '\n'.join(lines)

    def get_solution_text(self) -> str:
        conclusions = self.engine.get_available_conclusions(self.state.facts)
        if not conclusions:
            return ('Kalau kamu minta solusi, aku bisa bantu mulai dari hal kecil: atur waktu tidur, coba cerita ke orang deket, dan istirahatkan diri kalau udah capek banget. ' 
                    'Itu lebih ke tempat awal, jadi kamu gak langsung ngerasa kewalahan.')
        lines = []
        for item in conclusions[:2]:
            rule = item['rule']
            lines.append(f"{rule['nama']}: {rule['solusi']}")
        return '\n'.join(lines)

    def is_insight_available(self) -> bool:
        return self.state.analysis_shared and bool(self.engine.get_available_conclusions(self.state.facts))

    def get_insight_data(self) -> dict:
        conclusions = self.engine.get_available_conclusions(self.state.facts)
        if not conclusions:
            return {
                'emotional': {
                    'title': 'Kondisi Emosional',
                    'content': 'Aku lihat ada tekanan emosional yang muncul dari cerita kamu.',
                    'color': '#FFD6D6',
                },
                'patterns': {
                    'title': 'Pola yang Terlihat',
                    'content': 'Cerita kamu menunjukkan pola kelelahan dan overthinking.',
                    'color': '#CDE7FF',
                },
                'factors': {
                    'title': 'Faktor Penyebab',
                    'content': 'Beberapa faktor tekanan yang mungkin berperan adalah beban tugas dan kurang istirahat.',
                    'color': '#FFF4D6',
                },
                'suggestions': [
                    'Istirahat yang cukup dan buat waktu khusus untuk diri sendiri.',
                    'Coba tulis apa yang kamu rasakan supaya lebih tertata.',
                    'Bicarakan bebanmu sama orang dekat kalau kamu siap.',
                ],
                'summary': 'Ini adalah insight awal berdasarkan cerita kamu. Kalau kamu butuh, kita bisa lihat lebih lanjut lagi.',
            }

        top = conclusions[0]
        rule = top['rule']
        satisfied = [self.kb.get_fact(fid)['nama'] for fid in top['satisfied']]
        return {
            'emotional': {
                'title': 'Kondisi Emosional',
                'content': f"Dari cerita kamu, aku nangkep ada beban emosional yang muncul dari {', '.join(satisfied)}.",
                'color': '#FFD6D6',
            },
            'patterns': {
                'title': 'Pola yang Terlihat',
                'content': f"Terdapat pola cerita tentang {', '.join(satisfied)} yang berulang.",
                'color': '#CDE7FF',
            },
            'factors': {
                'title': 'Faktor Penyebab',
                'content': f"Kondisi ini biasanya dipicu oleh {rule['deskripsi'].lower()}",
                'color': '#FFF4D6',
            },
            'suggestions': [rule['solusi']] + [item['rule']['solusi'] for item in conclusions[1:2]],
            'summary': f"Sepertinya ada kecenderungan: {rule['nama']}. Ini bukan diagnosis medis, tapi semoga bisa bantu kamu lihat apa yang lagi terjadi.",
        }

    def get_greeting(self) -> str:
        greeting = self.theme['greeting']
        self.state.record_message('bot', greeting)
        return greeting

    def process_message(self, text: str) -> str:
        text = text.strip()
        self.state.record_message('user', text)

        if self.state.analysis_requested and not self.state.analysis_shared:
            if self._is_positive_answer(text):
                self.state.analysis_shared = True
                analysis = self.get_analysis_text()
                self.state.record_message('bot', analysis)
                return analysis
            if self._is_negative_answer(text):
                response = self.theme['ask_later']
                self.state.record_message('bot', response)
                return response
            if self._wants_solution(text):
                solution = self.get_solution_text()
                self.state.analysis_shared = True
                self.state.record_message('bot', solution)
                return solution
            response = self.theme['supportive'][0]
            self.state.record_message('bot', response)
            return response

        matched_facts = self.kb.match_keywords(text)
        self.state.update_facts(matched_facts)

        if self._wants_solution(text) and self.state.ready_for_analysis:
            self.state.analysis_requested = True
            return self.theme['analysis_permission']

        if not self.state.ready_for_analysis:
            candidate = self.engine.best_candidate(self.state.facts)
            if candidate and candidate['score'] >= 0.5:
                self.state.ready_for_analysis = True

        if self.state.ready_for_analysis:
            self.state.analysis_requested = True
            return self.theme['analysis_permission']

        question = self._target_question()
        if question:
            self.state.record_message('bot', question)
            return question

        supportive = self._pick_supportive()
        self.state.record_message('bot', supportive)
        return supportive

    def reset(self):
        self.state = SessionState()
        self.engine = InferenceEngine(self.kb)


if __name__ == '__main__':
    bot = CurhatBot()
    print(bot.theme['greeting'])
    while True:
        user_input = input('Kamu: ').strip()
        if user_input.lower() in ('exit', 'keluar', 'bye', 'quit'):
            print('Bot: Makasih ya udah cerita. Semoga harimu lebih enteng.')
            break
        response = bot.process_message(user_input)
        print(f'Bot: {response}')
