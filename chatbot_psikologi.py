import re
import random
from typing import Dict, List, Optional, Tuple


class ThemeManager:

    themes = {
        'teman_curhat': {
            'name': 'Teman Curhat',

            'greeting': (
                'Hai! Aku teman curhatmu di sini. '
                'Cerita aja apa yang lagi mengganjal di pikiranmu, santai aja ya.'
            ),

            'supportive': [
                'Wah, pasti capek ya kamu ngejalaninnya.',
                'Iya, aku denger kok. Lanjutin ceritanya kalau kamu masih mau.',
                'Aku di sini buat nemenin kamu.',
                'Kalau kamu mau, aku bisa bantu nyusun lagi apa yang kamu rasain.',
            ],

            'analysis_permission': (
                'Dari cerita kamu sejauh ini, '
                'aku udah mulai nangkep beberapa hal. '
                'Boleh nggak aku share dulu apa yang aku rasa?'
            ),

            'ask_later': (
                'Oke, santai aja. '
                'Kalau kamu mau aku analisanya nanti, bilang aja ya.'
            ),

            'no_analysis': (
                'Gak masalah, kita lanjut curhat aja. '
                'Yang penting kamu ngerasa didengerin.'
            ),

            'final_thanks': (
                'Makasih ya udah cerita jujur. '
                'Aku ada di sini kalau kamu mau curhat lagi kapan pun.'
            ),

            'permission_positive': [
                'boleh',
                'iya',
                'yap',
                'oke',
                'ok',
                'yes',
                'silakan',
                'silahkan',
                'ya',
                'lanjut'
            ],

            'permission_negative': [
                'nggak',
                'gak',
                'tidak',
                'nanti',
                'belum',
                'belum dulu',
                'enggak'
            ],

            'ask_for_solution': [
                'solusi',
                'saran',
                'bantu',
                'cara',
                'tips',
                'apa yang harus'
            ],
        },
    }

    @classmethod
    def get_theme(cls, name: str) -> Dict:
        return cls.themes.get(name, cls.themes['teman_curhat'])


# =========================================================
# KNOWLEDGE BASE
# =========================================================

class KnowledgeBase:

    def __init__(self):

        self.facts = self._build_facts()
        self.rules = self._build_rules()

    def _build_facts(self):

        return {

            'G1': {
                'nama': 'Mudah marah/tersinggung',
                'keywords': [
                    'marah',
                    'emosi',
                    'tersinggung',
                    'kesel'
                ],
                'pertanyaan': (
                    'Belakangan ini kamu jadi lebih gampang emosian '
                    'atau sensitif nggak?'
                ),
            },

            'G2': {
                'nama': 'Perasaan sedih/hampa',
                'keywords': [
                    'sedih',
                    'hampa',
                    'nangis',
                    'murung',
                    'putus asa'
                ],
                'pertanyaan': (
                    'Rasa sedihnya ini udah sering muncul '
                    'belakangan ini?'
                ),
            },

            'G3': {
                'nama': 'Kesulitan fokus',
                'keywords': [
                    'fokus',
                    'konsentrasi',
                    'blank',
                    'bingung'
                ],
                'pertanyaan': (
                    'Hal-hal sehari-hari jadi susah fokus juga '
                    'nggak buat kamu?'
                ),
            },

            'G4': {
                'nama': 'Gangguan tidur',
                'keywords': [
                    'insomnia',
                    'susah tidur',
                    'begadang',
                    'gak bisa tidur'
                ],
                'pertanyaan': (
                    'Tidur kamu belakangan gimana? '
                    'Masih bisa istirahat cukup?'
                ),
            },

            'G5': {
                'nama': 'Capek fisik',
                'keywords': [
                    'capek',
                    'lelah',
                    'lemes',
                    'lesu'
                ],
                'pertanyaan': (
                    'Capeknya lebih ke fisik, pikiran, atau dua-duanya?'
                ),
            },

            'G6': {
                'nama': 'Hilang minat',
                'keywords': [
                    'gak semangat',
                    'bosan',
                    'gak ada motivasi'
                ],
                'pertanyaan': (
                    'Hal-hal yang biasanya bikin kamu seneng sekarang '
                    'masih terasa menyenangkan nggak?'
                ),
            },

            'G7': {
                'nama': 'Cemas berlebih',
                'keywords': [
                    'cemas',
                    'khawatir',
                    'panik',
                    'takut',
                    'overthinking'
                ],
                'pertanyaan': (
                    'Pikiran cemasnya sering muncul terus '
                    'akhir-akhir ini ya?'
                ),
            },

            'G8': {
                'nama': 'Perubahan nafsu makan',
                'keywords': [
                    'gak makan',
                    'ga makan',
                    'gak selera makan',
                    'nafsu makan',
                    'malas makan'
                ],
                'pertanyaan': (
                    'Nafsu makan kamu berubah cukup jauh juga '
                    'ya belakangan ini?'
                ),
            },

            'G9': {
                'nama': 'Menarik diri',
                'keywords': [
                    'sendiri',
                    'menjauh',
                    'ngurung diri'
                ],
                'pertanyaan': (
                    'Kamu jadi lebih pengen sendiri '
                    'dibanding biasanya?'
                ),
            },

            'G10': {
                'nama': 'Putus asa',
                'keywords': [
                    'nyerah',
                    'putus asa',
                    'gak ada harapan'
                ],
                'pertanyaan': (
                    'Kadang sampai ngerasa kehilangan harapan juga nggak?'
                ),
            },
        }

    def _build_rules(self):

        return [

            {
                'nama': 'Burnout ringan',

                'deskripsi': (
                    'Ada tanda kelelahan emosional '
                    'dan tekanan berkepanjangan.'
                ),

                'kondisi': [
                    'G1',
                    'G3',
                    'G5'
                ],

                'solusi': (
                    'Coba kurangi tekanan sedikit demi sedikit, '
                    'kasih waktu istirahat yang cukup, '
                    'dan jangan paksa diri terus jalan tanpa jeda.'
                ),
            },

            {
                'nama': 'Kecemasan berlebih',

                'deskripsi': (
                    'Pikiran cemas dan overthinking '
                    'mulai mengganggu keseharian.'
                ),

                'kondisi': [
                    'G4',
                    'G7'
                ],

                'solusi': (
                    'Coba tarik napas perlahan, '
                    'kurangi memendam semuanya sendirian, '
                    'dan cari aktivitas yang bikin pikiran lebih tenang.'
                ),
            },

            {
                'nama': 'Gejala depresi ringan',

                'deskripsi': (
                    'Ada tanda sedih berkepanjangan, '
                    'energi turun, dan kehilangan semangat.'
                ),

                'kondisi': [
                    'G2',
                    'G5',
                    'G6',
                    'G8',
                    'G10'
                ],

                'solusi': (
                    'Mulai dari rutinitas kecil dulu, '
                    'jangan tuntut diri terlalu keras, '
                    'dan kalau makin berat pertimbangkan cerita ke profesional.'
                ),
            },

        ]

    def get_fact_ids(self) -> List[str]:

        return list(self.facts.keys())

    def get_fact(self, fact_id: str):

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


# =========================================================
# SESSION STATE
# =========================================================

class SessionState:

    def __init__(self):

        self.facts: Dict[str, bool] = {}

        self.asked_questions: List[str] = []

        self.history: List[Tuple[str, str]] = []

        self.analysis_requested = False

        self.analysis_shared = False

        self.ready_for_analysis = False

        # MEMORY KONTEKS

        self.last_topic = None

        self.user_story_count = 0

        self.current_emotion = None

    def update_facts(self, fact_ids: List[str]):

        for fact_id in fact_ids:

            self.facts[fact_id] = True

    def record_message(self, speaker: str, text: str):

        self.history.append((speaker, text))

    def mark_question_asked(self, fact_id: str):

        if fact_id not in self.asked_questions:

            self.asked_questions.append(fact_id)

    def has_asked(self, fact_id: str):

        return fact_id in self.asked_questions


# =========================================================
# INFERENCE ENGINE
# =========================================================

class InferenceEngine:

    def __init__(self, knowledge_base: KnowledgeBase):

        self.knowledge_base = knowledge_base

    def infer(self, facts: Dict[str, bool]):

        conclusions = []

        for rule in self.knowledge_base.rules:

            satisfied = [
                fact for fact in rule['kondisi']
                if facts.get(fact)
            ]

            if satisfied:

                score = len(satisfied) / len(rule['kondisi'])

                conclusions.append({

                    'rule': rule,

                    'score': score,

                    'satisfied': satisfied,

                    'remaining': [
                        fact for fact in rule['kondisi']
                        if fact not in satisfied
                    ],
                })

        conclusions.sort(
            key=lambda item: item['score'],
            reverse=True
        )

        return conclusions

    def best_candidate(self, facts):

        conclusions = self.infer(facts)

        return conclusions[0] if conclusions else None

    def needs_more_info(self, facts):

        candidate = self.best_candidate(facts)

        if not candidate:

            return []

        return candidate['remaining']

    def get_available_conclusions(self, facts):

        conclusions = self.infer(facts)

        return [
            item for item in conclusions
            if item['score'] >= 0.5
        ]


# =========================================================
# CURHAT BOT
# =========================================================

class CurhatBot:

    def __init__(self, theme_name='teman_curhat'):

        self.theme = ThemeManager.get_theme(theme_name)

        self.kb = KnowledgeBase()

        self.state = SessionState()

        self.engine = InferenceEngine(self.kb)

    # =====================================================
    # BASIC HELPERS
    # =====================================================

    def _is_positive_answer(self, text):

        lowered = text.lower()

        return any(
            token in lowered
            for token in self.theme['permission_positive']
        )

    def _is_negative_answer(self, text):

        lowered = text.lower()

        return any(
            token in lowered
            for token in self.theme['permission_negative']
        )

    def _wants_solution(self, text):

        lowered = text.lower()

        return any(
            token in lowered
            for token in self.theme['ask_for_solution']
        )

    def _pick_supportive(self):

        return random.choice(
            self.theme['supportive']
        )

    # =====================================================
    # EMOTION DETECTOR
    # =====================================================

    def _detect_emotion_context(self, text: str):

        text = text.lower()

        sadness = [
            'sedih',
            'capek',
            'hampa',
            'nangis',
            'kecewa',
            'putus',
            'gak kuat',
            'lelah'
        ]

        anxiety = [
            'cemas',
            'takut',
            'khawatir',
            'overthinking',
            'panik'
        ]

        anger = [
            'marah',
            'emosi',
            'kesel',
            'muak'
        ]

        if any(x in text for x in sadness):
            return 'sadness'

        if any(x in text for x in anxiety):
            return 'anxiety'

        if any(x in text for x in anger):
            return 'anger'

        return None

    # =====================================================
    # TOPIC DETECTOR
    # =====================================================

    def _detect_topic(self, text: str):

        text = text.lower()

        topics = {

            'relationship': [
                'putus',
                'pacar',
                'hubungan',
                'mantan'
            ],

            'work': [
                'kerja',
                'kantor',
                'deadline',
                'tugas'
            ],

            'family': [
                'keluarga',
                'orang tua',
                'ayah',
                'ibu'
            ],

            'self': [
                'diri sendiri',
                'gak percaya diri',
                'capek hidup'
            ],
        }

        for topic, keywords in topics.items():

            if any(k in text for k in keywords):
                return topic

        return None

    # =====================================================
    # REFLECTIVE RESPONSE
    # =====================================================

    def _generate_reflective_response(self, text: str):

        text_lower = text.lower()

        # RELATIONSHIP

        if 'putus' in text_lower:

            return (
                "Wah... kehilangan hubungan memang bisa bikin kosong banget ya. "
                "Apalagi kalau sebelumnya kamu banyak berharap sama hubungan itu."
            )

        # SADNESS

        if 'sedih' in text_lower:

            return (
                "Aku denger kamu lagi sedih banget sekarang. "
                "Biasanya ada sesuatu yang cukup berat sampai bikin "
                "perasaan jadi kayak gini. "
                "Kalau kamu nyaman, cerita aja pelan-pelan."
            )

        # TIRED

        if 'capek' in text_lower or 'lelah' in text_lower:

            return (
                "Capek terus-terusan memang bisa bikin semuanya terasa berat ya. "
                "Belakangan ini yang paling nguras energi kamu apa?"
            )

        # CRYING

        if 'nangis' in text_lower:

            return (
                "Kalau sampai nangis terus biasanya emosinya memang "
                "udah kependem cukup lama. "
                "Aku dengerin kok, pelan-pelan aja ceritanya."
            )

        # ANXIETY

        if 'cemas' in text_lower or 'overthinking' in text_lower:

            return (
                "Pikiran yang muter terus memang capek banget rasanya ya. "
                "Biasanya apa yang paling sering kepikiran belakangan ini?"
            )

        # EATING

        if 'gak makan' in text_lower or 'ga makan' in text_lower:

            return (
                "Aku ikut khawatir dengernya. "
                "Biasanya kalau sampai nggak makan gitu, "
                "ada hal yang lagi berat banget kepikiran. "
                "Mau cerita apa yang bikin kamu sesedih ini?"
            )

        # DEFAULT

        return random.choice([

            "Aku dengerin kok. Lanjut aja ceritanya kalau kamu mau.",

            "Hmm... kedengarannya lagi berat buat kamu ya.",

            "Aku ngerti. Terus habis itu gimana?",

            "Yang paling bikin kepikiran dari semua ini apa?",
        ])

    # =====================================================
    # CONTEXTUAL QUESTION
    # =====================================================

    def _generate_contextual_question(self):

        emotion = self.state.current_emotion

        topic = self.state.last_topic

        # RELATIONSHIP

        if topic == 'relationship':

            return random.choice([
                'Sejak kejadian itu, keseharian kamu jadi berubah banyak nggak?',
                'Yang paling berat dari semua ini bagian yang mana buat kamu?',
                'Kamu masih sering kepikiran soal hubungan itu?'
            ])

        # WORK

        if topic == 'work':

            return random.choice([
                'Tekanan kerjaannya udah berlangsung lama ya?',
                'Kamu masih sempat istirahat di tengah semua tekanan itu?',
                'Yang paling bikin kamu kewalahan bagian mana?'
            ])

        # ANXIETY

        if emotion == 'anxiety':

            return random.choice([
                'Pikiran itu biasanya muncul paling kuat kapan?',
                'Kalau lagi cemas banget biasanya kamu ngapain?',
                'Belakangan ini tidur kamu ikut keganggu nggak?'
            ])

        # SADNESS

        if emotion == 'sadness':

            return random.choice([
                'Belakangan ini kamu masih bisa cerita ke orang lain juga nggak?',
                'Rasa beratnya lebih sering muncul malam atau sepanjang hari?',
                'Kamu ngerasa makin dipendem atau sempat lega kalau cerita?'
            ])

        return None

    # =====================================================
    # QUESTION TARGETING
    # =====================================================

    def _best_missing_fact(self):

        missing = self.engine.needs_more_info(
            self.state.facts
        )

        for fact_id in missing:

            if not self.state.has_asked(fact_id):
                return fact_id

        return None

    def _target_question(self):

        contextual = self._generate_contextual_question()

        if contextual:
            return contextual

        fact_id = self._best_missing_fact()

        if fact_id is None:
            return None

        self.state.mark_question_asked(fact_id)

        fact = self.kb.get_fact(fact_id)

        return fact['pertanyaan']

    # =====================================================
    # ANALYSIS
    # =====================================================

    def get_analysis_text(self):

        conclusions = self.engine.get_available_conclusions(
            self.state.facts
        )

        if not conclusions:

            return (
                "Aku belum bisa menyimpulkan banyak hal, "
                "tapi aku lihat kamu lagi bawa beban yang cukup berat."
            )

        lines = []

        for item in conclusions[:2]:

            rule = item['rule']

            satisfied = [
                self.kb.get_fact(fid)['nama']
                for fid in item['satisfied']
            ]

            lines.append(

                f"- {rule['nama']}\n"
                f"  {rule['deskripsi']}\n"
                f"  Gejala yang terlihat: {', '.join(satisfied)}"

            )

        lines.append(
            "\nIni bukan diagnosis medis ya, "
            "tapi mungkin bisa bantu kamu lebih ngerti kondisi diri sendiri."
        )

        return '\n\n'.join(lines)

    def get_solution_text(self):

        conclusions = self.engine.get_available_conclusions(
            self.state.facts
        )

        if not conclusions:

            return (
                "Coba mulai dari hal kecil dulu ya. "
                "Istirahat cukup, jangan pendam semuanya sendiri, "
                "dan kasih ruang buat diri sendiri bernapas."
            )

        lines = []

        for item in conclusions[:2]:

            rule = item['rule']

            lines.append(
                f"{rule['nama']}:\n{rule['solusi']}"
            )

        return '\n\n'.join(lines)

    # =====================================================
    # INSIGHT API
    # =====================================================

    def is_insight_available(self):

        conclusions = self.engine.get_available_conclusions(
            self.state.facts
        )

        return len(conclusions) > 0

    def get_insight_data(self):

        conclusions = self.engine.get_available_conclusions(
            self.state.facts
        )

        if not conclusions:

            return {
                'available': False,
                'summary': (
                    'Belum cukup data untuk membuat insight.'
                ),
            }

        top = conclusions[0]

        rule = top['rule']

        satisfied = [
            self.kb.get_fact(fid)['nama']
            for fid in top['satisfied']
        ]

        return {

            'available': True,

            'title': rule['nama'],

            'description': rule['deskripsi'],

            'detected_facts': satisfied,

            'solution': rule['solusi'],

            'score': round(top['score'], 2),
        }

    # =====================================================
    # GREETING
    # =====================================================

    def get_greeting(self):

        greeting = self.theme['greeting']

        self.state.record_message(
            'bot',
            greeting
        )

        return greeting

    # =====================================================
    # MAIN PROCESS
    # =====================================================

    def process_message(self, text: str):

        text = text.strip()

        self.state.record_message(
            'user',
            text
        )

        # ================================================
        # ANALYSIS PERMISSION FLOW
        # ================================================

        if self.state.analysis_requested and not self.state.analysis_shared:

            if self._is_positive_answer(text):

                self.state.analysis_shared = True

                analysis = self.get_analysis_text()

                self.state.record_message(
                    'bot',
                    analysis
                )

                return analysis

            if self._is_negative_answer(text):

                response = self.theme['ask_later']

                self.state.record_message(
                    'bot',
                    response
                )

                return response

            if self._wants_solution(text):

                solution = self.get_solution_text()

                self.state.analysis_shared = True

                self.state.record_message(
                    'bot',
                    solution
                )

                return solution

        # ================================================
        # DETECT FACTS
        # ================================================

        matched_facts = self.kb.match_keywords(text)

        self.state.update_facts(matched_facts)

        # ================================================
        # STORY COUNT
        # ================================================

        self.state.user_story_count += 1

        # ================================================
        # DETECT EMOTION
        # ================================================

        emotion = self._detect_emotion_context(text)

        if emotion:

            self.state.current_emotion = emotion

        # ================================================
        # DETECT TOPIC
        # ================================================

        topic = self._detect_topic(text)

        if topic:

            self.state.last_topic = topic

        # ================================================
        # PHASE 1 — DENGERIN DULU
        # ================================================

        if self.state.user_story_count <= 3:

            response = self._generate_reflective_response(text)

            self.state.record_message(
                'bot',
                response
            )

            return response

        # ================================================
        # PHASE 2 — MULAI ANALISIS PELAN
        # ================================================

        if not self.state.ready_for_analysis:

            candidate = self.engine.best_candidate(
                self.state.facts
            )

            if candidate and candidate['score'] >= 0.4:

                self.state.ready_for_analysis = True

        if self.state.ready_for_analysis:

            if not self.state.analysis_requested:

                self.state.analysis_requested = True

                response = (
                    "Aku mulai nangkep pola dari cerita kamu sejauh ini. "
                    "Tapi aku masih pengen ngerti sedikit lagi "
                    "biar nggak salah nangkep.\n\n"
                )

                question = self._target_question()

                if question:
                    response += question

                self.state.record_message(
                    'bot',
                    response
                )

                return response

        # ================================================
        # PHASE 3 — PERTANYAAN LANJUT
        # ================================================

        question = self._target_question()

        if question:

            self.state.record_message(
                'bot',
                question
            )

            return question

        supportive = self._pick_supportive()

        self.state.record_message(
            'bot',
            supportive
        )

        return supportive

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.state = SessionState()

        self.engine = InferenceEngine(self.kb)


# =========================================================
# CLI TEST
# =========================================================

if __name__ == '__main__':

    bot = CurhatBot()

    print(f"Bot: {bot.get_greeting()}")

    while True:

        user_input = input('Kamu: ').strip()

        if user_input.lower() in [
            'exit',
            'keluar',
            'bye',
            'quit'
        ]:

            print(
                'Bot: Makasih ya udah cerita. '
                'Semoga harimu lebih enteng.'
            )

            break

        response = bot.process_message(user_input)

        print(f'Bot: {response}')