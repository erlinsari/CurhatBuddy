"""
Advice & Support Builder
- Handles advice-seeking requests specifically
- Provides practical, realistic small steps
- Not just validation, but actual support
- Maintains human tone while giving guidance
"""

from typing import Dict, List, Tuple, Optional
import re
import random


class AdviceSupportBuilder:
    """Build responses when user asks for advice or practical support"""
    
    def __init__(self):
        # Validasi responses - not generic, tied to context
        self.validation_responses = {
            'body_image_shame': [
                'Malu dengan penampilan itu emang rasa yang dalam dan bisa bikin kita jadi tertutup dari orang lain.',
                'Ketika ada yang mengganggu tentang penampilan kita, itu bisa jadi berat banget dan bikin nggak percaya diri.',
                'Rasa malu dengan wajah atau badan itu valid, tapi penting diingat kalau itu bukan penentu siapa kamu.',
                'Jerawat atau masalah penampilan lainnya itu hal yang banyak orang alami, tapi rasanya kayak cuma kamu yang punya.',
            ],
            'insecurity': [
                'Rasa nggak cukup itu nyata dan biasanya muncul pas kita ada keraguan tentang diri sendiri.',
                'Rasa kurang dari orang lain itu emang berat, tapi penting diingat kalau perasaan itu bukan fakta.',
                'Rasa minder adalah cara hati kita bilang "aku takut nggak diterima", dan itu valid.',
            ],
            'fear_of_abandonment': [
                'Takut kehilangan orang yang penting itu salah satu rasa paling pedih yang ada.',
                'Ketakutan ditinggal itu nyata, terutama kalau orang itu penting untuk kamu.',
                'Rasa nggak aman dalam hubungan adalah respons wajar terhadap perubahan yang kamu lihat.',
            ],
            'overwhelm': [
                'Merasa kewalahan berarti emosi kamu sedang penuh dan butuh ruang lega.',
                'Ketika terlalu banyak tekanan, normal kalau kamu merasa nggak sanggup.',
                'Kewalahan adalah tanda bahwa kamu perlu istirahat dan dukungan, bukan tanda kelemahan.',
            ],
            'overthinking': [
                'Pikiran yang berputar terus adalah cara pikiran kamu mencoba melindungi diri dari ketidakpastian.',
                'Pikiran yang terus berputar itu melelahkan, dan itu valid untuk dirasakan.',
                'Ketika pikiran terus berputar, kamu sebenarnya sedang mencoba mengendalikan hal yang belum tentu bisa dikendalikan.',
            ],
            'burnout': [
                'Kelelahan total bukan malas, tapi tanda bahwa kamu sudah memaksa diri terlalu keras terlalu lama.',
                'Kelelahan yang mendalam butuh istirahat nyata, bukan motivasi.',
                'Ketika energi habis, itu berarti kamu benar-benar perlu jeda dan memulihkan tenaga.',
            ],
        }
        
        # Insight responses - practical understanding
        self.insight_responses = {
            'body_image_shame': [
                'Sering kali kita fokus ke satu hal yang "salah" dengan penampilan, padahal orang lain nggak lihat itu seberat yang kita pikir.',
                'Jerawat atau masalah kulit itu bisa berubah dan bisa dirawat, tapi rasa malu yang muncul sering terasa paling berat.',
                'Ketika malu dengan penampilan, kita cenderung menjauh dari orang lain, padahal hubungan yang aman bisa membantu rasa malu itu berkurang.',
                'Penampilan itu cuma satu bagian dari kamu, bukan seluruh identitas kamu. Tapi ketika rasa malu muncul, rasanya seperti itu yang paling penting.',
            ],
            'insecurity': [
                'Sering kali rasa minder muncul bukan karena kamu benar-benar kurang, tapi karena kamu membandingkan diri dengan standar yang terlalu tinggi.',
                'Rasa minder sering dipicu oleh orang lain, tapi yang paling menyakitkan adalah suara di kepala sendiri yang terus menyalahkan diri.',
                'Ketika minder, perhatian kita fokus ke apa yang salah, padahal banyak hal yang sudah berjalan baik.',
            ],
            'fear_of_abandonment': [
                'Ketakutan ditinggal sering membuat kita terlalu ketat dalam hubungan, padahal itu justru bisa membuat hubungan terasa makin tertekan.',
                'Sering kali perubahan kecil di hubungan kita tafsirkan sebagai tanda ditinggal, padahal mungkin itu cuma dinamika normal.',
                'Ketakutan akan penolakan membuat kita menunggu hal buruk terjadi, dan itu melelahkan.',
            ],
            'overwhelm': [
                'Kewalahan terjadi ketika kita mencoba menangani semuanya sendirian dan tidak minta bantuan.',
                'Tekanan itu menumpuk sedikit demi sedikit, lalu tiba-tiba terasa menghantam semuanya.',
                'Kewalahan adalah tanda bahwa kita perlu fokus ke hal yang benar-benar penting dan menunda sisanya dulu.',
            ],
            'overthinking': [
                'Pikiran yang terus berputar adalah kecemasan yang mencari kepastian dari kemungkinan buruk yang belum tentu terjadi.',
                'Pikiran kita kuat, tapi pikiran yang berputar terus itu seperti berlari di tempat: capek tapi tidak benar-benar maju.',
                'Yang penting bukan memaksa berhenti berpikir, tapi memutus putarannya dan kembali ke saat ini.',
            ],
            'burnout': [
                'Kelelahan total terjadi saat kita terus mendahulukan kerja atau pencapaian dibanding istirahat dan menjaga diri.',
                'Ketika kelelahan total, yang dibutuhkan bukan produktivitas, tapi izin untuk berhenti sebentar dan bernapas.',
                'Pulih dari kelelahan total butuh istirahat yang sungguh-sungguh, bukan cuma menunggu akhir pekan.',
            ],
        }
        
        # Practical steps - small, realistic, actionable
        self.practical_steps = {
            'body_image_shame': [
                'Mulai dengan perawatan kulit yang sederhana dan konsisten. Bukan untuk memperbaiki semuanya semalam, tapi untuk menunjukkan bahwa kamu peduli pada diri sendiri.',
                'Coba cerita ke orang yang kamu percaya. Sering kali rasa malu berkurang saat kita berbagi dan sadar orang lain tidak menilai sekeras yang kita takutkan.',
                'Batasi kebiasaan mengecek cermin. Kalau kamu terus memeriksa jerawat, rasa malu bisa makin kuat.',
                'Mulai lakukan hal yang bikin kamu merasa baik tentang diri sendiri, bukan hanya soal penampilan. Hobi, pencapaian kecil, atau hubungan yang aman.',
                'Tantang pikiran: "Orang akan menilai aku karena jerawat." Tanya balik: "Apa aku menilai orang lain seberat ini karena jerawat mereka?"',
                'Coba bertemu orang sedikit demi sedikit. Nggak harus langsung banyak orang. Mulai dari satu teman yang kamu percaya.',
            ],
            'insecurity': [
                'Mulai perhatikan ketika suara yang mengkritik diri muncul. Cukup sadari dulu, jangan tambah menghakimi diri.',
                'Latih menantang satu pikiran negatif per hari. Tanya ke diri sendiri: "Ini benar-benar fakta atau kecemasan yang sedang bicara?"',
                'Mulai catat hal-hal kecil yang sudah kamu berhasil lakukan. Buka lagi saat kamu butuh menguatkan percaya diri.',
                'Berhenti mengikuti akun yang membuat kamu terus membandingkan diri. Jaga perhatian kamu.',
                'Coba bicara ke diri sendiri dengan realistis, bukan positif palsu. Bukan "aku paling hebat", tapi "aku cukup dan masih belajar".',
            ],
            'fear_of_abandonment': [
                'Mulai komunikasi lebih jelas tentang apa yang kamu butuhkan. Daripada langsung berasumsi saat dia lama membalas, coba bilang bahwa kamu butuh komunikasi yang lebih konsisten.',
                'Kembangkan hobi atau minat yang tetap milik kamu sendiri. Hubungan yang sehat butuh ruang pribadi dari dua sisi.',
                'Lawan pikiran: cuma karena mereka nggak bales cepat bukan berarti mereka pergi. Kecil-kecil ingetin diri sendiri ini.',
                'Catat kapan rasa takut muncul paling kuat dan apa pemicunya. Biasanya dari situ kamu bisa melihat polanya.',
                'Coba teknik grounding ketika fear intense: 5 hal yang kamu lihat, 4 yang bisa kamu sentuh, 3 yang kamu dengar, 2 yang kamu cium, 1 yang kamu rasa.',
            ],
            'overwhelm': [
                'Pilih cuma 3 hal yang HARUS selesai hari ini. Yang lain bisa tunggu. Serius, cuma 3.',
                'Pecah tugas besar jadi langkah-langkah kecil. Daripada "membereskan hidup", pecah jadi "hubungi teman", "makan yang benar", atau "tidur cukup".',
                'Belajar bilang "nggak bisa hari ini" tanpa rasa bersalah. Tenaga dan pikiran kamu juga ada batasnya.',
                'Buat rutinitas sederhana yang menenangkan: 5 menit ritual pagi dan 10 menit menutup hari sebelum tidur. Konsistensi membantu menstabilkan suasana hati.',
                'Minta bantuan spesifik ke satu orang. Bukan hanya "aku kewalahan", tapi permintaan konkret seperti "bisa bantu aku hari Jumat?"',
            ],
            'overthinking': [
                'Alokasikan waktu khusus: 10 menit untuk menuliskan semua pikiran. Setelah itu, pindah ke aktivitas lain.',
                'Putuskan putaran pikiran lewat tubuh: jalan sebentar, lompat kecil, atau cuci muka dengan air dingin.',
                'Kembali ke saat ini: perhatikan 3 hal yang sedang terjadi sekarang. Momen ini aman.',
                'Tulis semua kemungkinan buruk yang kamu takutkan. Biasanya ketika ditaruh di kertas, rasanya lebih bisa dihadapi.',
                'Tanya "terus apa?": kalau kemungkinan itu terjadi, langkah apa yang bisa kamu lakukan? Biasanya masih ada pilihan.',
            ],
            'burnout': [
                'Jadwalkan istirahat seperti janji penting. Bukan "kapan ada waktu", tapi waktu konkret untuk tidak melakukan apa-apa.',
                'Coba satu aktivitas istirahat tanpa layar. Jalan, membaca, hobi, atau apa pun yang benar-benar mengisi ulang tenaga kamu.',
                'Buat batas kerja yang jelas: ada jam berhenti, dan jangan cek pesan kerja di luar jam itu.',
                'Lakukan sesuatu yang murni untuk rasa senang, tanpa target produktif. Menyanyi, corat-coret, menari, atau hal ringan lain.',
                'Cerita ke teman, konselor, atau orang yang kamu percaya tentang bebanmu. Kadang sudut pandang dari luar sangat membantu.',
            ],
        }
        
        # Supportive closing - encouraging without toxic positivity
        self.supportive_closings = {
            'body_image_shame': [
                'Jerawat itu bisa berubah, tapi nilai diri kamu tidak hilang karena itu.',
                'Percaya diri bukan tentang penampilan sempurna, tapi tentang menerima diri sambil tetap merawat diri.',
                'Orang yang layak dekat dengan kamu tidak akan menilai kamu hanya dari jerawat. Mereka melihat kamu sebagai pribadi utuh.',
                'Malu itu normal, tapi kamu tidak harus mengurung diri. Kamu tetap layak punya hubungan dan dukungan.',
                'Pulih dari rasa malu ini butuh waktu dan kesabaran pada diri sendiri. Tapi kamu bisa pelan-pelan melewatinya.',
            ],
            'insecurity': [
                'Perjalanan menghadapi rasa minder itu panjang, dan perbaikannya tidak selalu lurus. Tapi kamu sudah mulai dengan menyadarinya.',
                'Percaya sama diri itu keterampilan yang bisa dilatih pelan-pelan.',
                'Kamu cukup seperti sekarang, sambil tetap boleh bertumbuh. Dua hal itu bisa benar bersamaan.',
                'Perubahan kecil itu menumpuk. Suatu hari kamu bisa menyadari keraguan diri muncul lebih jarang.',
            ],
            'fear_of_abandonment': [
                'Ketakutan itu manusiawi, dan kamu tidak berlebihan karena merasakannya. Itu kebutuhan emosional yang normal.',
                'Hubungan yang sehat butuh keberanian untuk terbuka dan tetap punya ruang diri. Kamu sedang belajar dua-duanya sekarang.',
                'Kepercayaan dalam hubungan dibangun pelan-pelan lewat konsistensi. Bersabarlah dengan diri sendiri.',
                'Aku harap kamu bisa menemukan orang yang menghargai kamu, termasuk kedalaman emosi kamu.',
            ],
            'overwhelm': [
                'Menjaga diri sendiri bukan egois, itu kebutuhan dasar.',
                'Minta bantuan bukan kelemahan. Itu keberanian dan kebijaksanaan.',
                'Kamu nggak harus memahami semuanya hari ini. Pelan-pelan juga tetap termasuk proses.',
                'Rasa kewalahan akan berlalu. Kamu sudah melewati banyak momen sulit sampai sekarang.',
            ],
            'overthinking': [
                'Pikiran yang mudah berputar sering kali sensitif, dan itu bisa jadi kekuatan kalau diarahkan dengan baik.',
                'Belajar quiet mind itu skill, bukan failure. Be gentle sa diri sendiri in the process.',
                'Kamu tidak rusak karena sering berpikir berlebihan. Kamu hanya butuh cara yang lebih pas untuk mengelolanya.',
                'Kecil-kecil kamu probably akan notice thoughts jadi less sticky.',
            ],
            'burnout': [
                'Istirahat bukan pilihan, itu kebutuhan. Kamu layak mendapatkannya.',
                'Pulih butuh waktu. Bersabarlah dengan proses dan diri sendiri.',
                'Hal yang kamu pelajari dari kelelahan ini penting. Ke depan, kamu bisa lebih sadar kapan perlu membuat batas.',
                'Kamu nggak lemah. Kamu hanya sudah memaksa diri terlalu keras dalam waktu yang terlalu lama.',
            ],
        }
    
    def build_advice_response(
        self,
        user_message: str,
        primary_emotion: Optional[str] = None,
        primary_intent: Optional[str] = None,
        previous_topic: Optional[str] = None
    ) -> str:
        """Build complete advice/support response"""
        
        lines = []
        
        # Determine which category of advice is needed
        # If current message doesn't have enough context, use previous_topic
        advice_category = self._determine_advice_category(user_message, primary_emotion, previous_topic)
        
        # 1. VALIDATION - show understanding
        if advice_category in self.validation_responses:
            validation = random.choice(self.validation_responses[advice_category])
            lines.append(validation)
        
        # 2. INSIGHT - provide practical understanding
        if advice_category in self.insight_responses:
            lines.append("")  # spacing
            insight = random.choice(self.insight_responses[advice_category])
            lines.append(insight)
        
        # 3. PRACTICAL STEPS - give realistic small action
        if advice_category in self.practical_steps:
            lines.append("")  # spacing
            lines.append("Langkah kecil yang bisa kamu lakukan:")
            steps = self.practical_steps[advice_category]
            selected_steps = random.sample(steps, min(2, len(steps)))  # Pick 2 random steps
            for step in selected_steps:
                lines.append(f"• {step}")
        
        # 4. SUPPORTIVE CLOSING - encouraging
        if advice_category in self.supportive_closings:
            lines.append("")  # spacing
            closing = random.choice(self.supportive_closings[advice_category])
            lines.append(closing)
        
        return "\n".join(lines)
    
    def _determine_advice_category(self, user_message: str, primary_emotion: Optional[str], previous_topic: Optional[str] = None) -> str:
        """Determine which advice category applies"""
        text_lower = user_message.lower()
        
        # Check explicit categories in message - APPEARANCE/BODY IMAGE FIRST
        if any(word in text_lower for word in ['jerawat', 'acne', 'pimple', 'malu', 'wajah', 'penampilan', 'jelek', 'gendut', 'gemuk', 'berat', 'kulit', 'rambut', 'gigi', 'ompong', 'nggak cantik', 'nggak ganteng', 'males ketemu', 'nggak pede ngobrol', 'shame', 'embarrassed']):
            return 'body_image_shame'
        elif any(word in text_lower for word in ['insecure', 'percaya diri', 'nggak cukup', 'kurang', 'minder']):
            return 'insecurity'
        elif any(word in text_lower for word in ['takut ditinggal', 'takut kehilangan', 'fear of abandonment', 'pacar']):
            return 'fear_of_abandonment'
        elif any(word in text_lower for word in ['overwhelm', 'kewalahan', 'banyak banget', 'terlalu banyak']):
            return 'overwhelm'
        elif any(word in text_lower for word in ['overthink', 'terus pikir', 'ngebas-ngebis', 'apa kalau']):
            return 'overthinking'
        elif any(word in text_lower for word in ['burnout', 'capek', 'lelah', 'exhausted', 'nggak kuat lagi']):
            return 'burnout'
        
        # Fallback to primary emotion if available
        if primary_emotion == 'body_image_shame' or primary_emotion == 'shame':
            return 'body_image_shame'
        elif primary_emotion == 'insecurity':
            return 'insecurity'
        elif primary_emotion == 'fear_of_abandonment':
            return 'fear_of_abandonment'
        elif primary_emotion == 'emotional_exhaustion':
            return 'overwhelm'
        elif primary_emotion == 'overthinking':
            return 'overthinking'
        
        # Fallback to previous_topic if current message doesn't have enough context
        if previous_topic == 'shame' or previous_topic == 'body_image_issue':
            return 'body_image_shame'
        elif previous_topic == 'insecurity':
            return 'insecurity'
        elif previous_topic == 'fear_of_abandonment':
            return 'fear_of_abandonment'
        elif previous_topic == 'emotional_exhaustion':
            return 'overwhelm'
        elif previous_topic == 'overthinking':
            return 'overthinking'
        
        # Default category
        return 'overwhelm'
    
    def build_validation_only(self, text_emotion: str) -> str:
        """Build just validation part (short response)"""
        if text_emotion in self.validation_responses:
            return random.choice(self.validation_responses[text_emotion])
        return "Apa yang kamu rasain adalah valid dan wajar."
    
    def build_insight_only(self, text_emotion: str) -> str:
        """Build just insight part"""
        if text_emotion in self.insight_responses:
            return random.choice(self.insight_responses[text_emotion])
        return None
    
    def build_practical_only(self, text_emotion: str) -> str:
        """Build just practical steps part"""
        if text_emotion not in self.practical_steps:
            return None
        
        steps = self.practical_steps[text_emotion]
        selected_steps = random.sample(steps, min(2, len(steps)))
        
        lines = ["Mungkin kamu bisa coba:"]
        for step in selected_steps:
            lines.append(f"• {step}")
        
        return "\n".join(lines)
