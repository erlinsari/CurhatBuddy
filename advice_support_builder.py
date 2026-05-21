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
                'Rasa malu dengan wajah atau badan itu valid, tapi penting diingat kalau itu bukan define siapa kamu.',
                'Jerawat atau masalah penampilan lainnya itu hal yang banyak orang alami, tapi rasanya kayak cuma kamu yang punya.',
            ],
            'insecurity': [
                'Rasa nggak cukup itu nyata dan biasanya muncul pas kita ada keraguan tentang diri sendiri.',
                'Rasa kurang dari orang lain itu emang berat, tapi penting diingat kalau perasaan itu bukan fakta.',
                'Insecure adalah cara hati kita bilang "aku takut nggak diterima", dan itu valid.',
            ],
            'fear_of_abandonment': [
                'Takut kehilangan orang yang penting itu salah satu rasa paling pedih yang ada.',
                'Ketakutan ditinggal itu real, terutama kalau orang itu significant untuk kamu.',
                'Rasa nggak aman dalam hubungan adalah respon natural terhadap perubahan yang kamu lihat.',
            ],
            'overwhelm': [
                'Merasa kewalahan berarti emosi kamu sedang overload dan butuh relief.',
                'Ketika terlalu banyak tekanan, normal kalau kamu merasa nggak sanggup.',
                'Kewalahan adalah tanda bahwa kamu perlu istirahat dan support, bukan tanda kelemahan.',
            ],
            'overthinking': [
                'Overthinking adalah cara pikiran kamu coba protect diri dari ketidakpastian.',
                'Pikiran yang terus berputar itu exhausting, dan itu valid untuk dirasakan.',
                'Ketika overthink, kamu sebenarnya trying to control outcome yang nggak bisa dikontrol.',
            ],
            'burnout': [
                'Burnout bukan lazy, tapi sign bahwa kamu udah push diri terlalu keras terlalu lama.',
                'Kelelahan yang mendalam butuh istirahat nyata, bukan motivasi.',
                'Ketika energi habis, itu berarti kamu benar-benar perlu pause dan regenerate.',
            ],
        }
        
        # Insight responses - practical understanding
        self.insight_responses = {
            'body_image_shame': [
                'Sering kali kita fokus ke satu hal yang "salah" dengan penampilan, padahal orang lain nggak lihat itu seberat yang kita pikir.',
                'Jerawat atau masalah kulit itu temporary dan bisa diobati, tapi shame yang kita rasain itu yang paling berat.',
                'Ketika malu dengan penampilan, kita cenderung isolate diri, padahal connection dengan orang lain itu yang bisa heal shame ini.',
                'Penampilan itu cuma satu bagian dari kamu, bukan seluruh identitas kamu. Tapi ketika shame muncul, rasanya kayak itu yang paling penting.',
            ],
            'insecurity': [
                'Sering kali insecurity muncul bukan karena kamu really nggak cukup, tapi karena kamu bandingkan diri dengan standar yang terlalu tinggi.',
                'Insecurity sering kali dipicu oleh orang lain, tapi yang paling nyakitin adalah suara di kepala kita sendiri yang terus nyalahin diri.',
                'Ketika insecure, perhatian kita fokus ke apa yang salah, padahal banyak hal yang udah bener.',
            ],
            'fear_of_abandonment': [
                'Ketakutan ditinggal sering membuat kita terlalu ketat dalam hubungan, padahal itu justru yang push orang malah pergi.',
                'Seringkali perubahan kecil di hubungan kita interpretasikan sebagai tanda ditinggal, padahal mungkin cuma dinamika normal.',
                'Ketakutan akan penolakan membuat kita anticipate rejection, dan itu exhausting.',
            ],
            'overwhelm': [
                'Kewalahan terjadi ketika kita coba handle semuanya sendirian dan nggak minta bantuan.',
                'Tekanan itu numpuk - kecil-kecil lalu tiba-tiba crushing semuanya.',
                'Kewalahan adalah signal bahwa kita perlu fokus ke apa yang really penting dan sisakan yang lain dulu.',
            ],
            'overthinking': [
                'Overthinking adalah anxiety dalam bentuk pikiran yang terus berputar - kita imagine worst-case scenarios yang belum tentu real.',
                'Pikiran kita kuat, tapi overthinking itu sama kayak berlari di tempat - capek tapi nggak kemana-mana.',
                'Yang penting bukan stop pikir (itu impossible), tapi break the spiral dan kembali ke saat ini.',
            ],
            'burnout': [
                'Burnout terjadi pas kita prioritize kerja/achievement lebih dari istirahat dan self-care.',
                'Ketika burnout, bukan produktivitas yang kita butuh, tapi izin untuk stop dan bernafas.',
                'Recovery dari burnout butuh istirahat yang beneran, bukan cuma weekend.',
            ],
        }
        
        # Practical steps - small, realistic, actionable
        self.practical_steps = {
            'body_image_shame': [
                'Mulai dengan skincare routine yang simple dan konsisten. Bukan untuk "fix" jerawat overnight, tapi untuk show diri sendiri bahwa kamu care.',
                'Coba talk to someone kamu trust tentang ini. Sering kali shame berkurang pas kita share dan realize orang lain nggak judge kita.',
                'Limit mirror checking. Kalau kamu terus lihat jerawat di mirror, shame jadi lebih intense. Coba reduce frequency.',
                'Mulai do things yang bikin kamu feel good tentang diri sendiri - bukan tentang penampilan. Hobby, achievement, connection dengan orang.',
                'Challenge thought: "Orang akan judge aku karena jerawat" - tanya ke diri sendiri: "Apa aku judge orang lain seberat ini karena jerawat mereka?"',
                'Coba bertemu orang sedikit demi sedikit. Nggak harus langsung banyak orang. Mulai dari satu teman yang kamu trust.',
            ],
            'insecurity': [
                'Mulai dengan perhatiin ketika suara self-critical muncul. Cukup observe, jangan judge diri sendiri karena criticizing.',
                'Praktik challenge satu negative thought per hari. Tanya ke diri sendiri: "Ini benar-benar true atau cuma anxiety talking?"',
                'Mulai catat hal-hal kecil yang kamu udah berhasil lakukan. Buat list, lihat kapan perlu boost confidence.',
                'Stop follow akun-akun yang bikin kamu compare. Serius, unfollow mereka. Jaga attention kamu.',
                'Coba self-talk yang realistic, bukan toxic positivity. Bukan "I\'m the best" tapi "Aku cukup dan masih belajar".',
            ],
            'fear_of_abandonment': [
                'Mulai komunikasi lebih jelas tentang apa yang kamu butuh. Daripada assume "lama bales", coba bilang "Aku perlu kita lebih konsisten chat".',
                'Kembangkan hobby atau passion yang independent dari orang itu. Hubungan yang sehat butuh independence dari both sides.',
                'Lawan pikiran: cuma karena mereka nggak bales cepat bukan berarti mereka pergi. Kecil-kecil ingetin diri sendiri ini.',
                'Catat kapan fear muncul paling intense. Apa yang trigger? Biasanya kamu bakal find pattern yang membantu understand trigger.',
                'Coba teknik grounding ketika fear intense: 5 hal yang kamu lihat, 4 yang bisa kamu sentuh, 3 yang kamu dengar, 2 yang kamu cium, 1 yang kamu rasa.',
            ],
            'overwhelm': [
                'Pilih cuma 3 hal yang HARUS selesai hari ini. Yang lain bisa tunggu. Serius, cuma 3.',
                'Pecah task besar jadi langkah-langkah kecil. Daripada "fix life", pecah jadi "call teman", "makan yang bener", "tidur 7 jam".',
                'Belajar bilang "nggak bisa hari ini" tanpa rasa bersalah. Tenaga dan pikiran kamu juga ada batasnya.',
                'Buat routine sederhana yang menenangkan: 5 menit ritual pagi, 10 menit wind-down malam. Konsistensi itu membantu stabilkan mood.',
                'Minta bantuan spesifik ke satu orang. Bukan vague "aku kewalahan" tapi "Bisa bantu aku hari Jumat?" yang konkret.',
            ],
            'overthinking': [
                'Alokasikan waktu khusus: 10 menit dimana kamu boleh overthink semua. Setelah 10 menit, move on ke hal lain.',
                'Interrupt dengan fisik: ketika spiral mulai, lakukan sesuatu yang physical. Jalan, lompat, cuci muka dengan air dingin. Break the mental loop.',
                'Kembali ke saat ini: perhatiin 3 hal yang happening sekarang. Momen ini aman.',
                'Tulis semua worst-case scenarios kamu. Biasanya ketika di kertas, jadi less scary dan lebih manageable.',
                'Tanya "Terus apa?": kalau scenario itu happen, "terus apa?" apa yang bakal kamu lakukan? Biasanya ada solusi kok.',
            ],
            'burnout': [
                'Jadwalkan istirahat seperti appointment. Bukan "kapan ada waktu" tapi waktu konkret untuk nggak ngapa-ngapain.',
                'Coba satu aktivitas istirahat yang bukan screen-based. Jalan, baca, hobby, apapun yang beneran recharge kamu.',
                'Buat boundary kerja: off-time yang strict dari kerja. Stop cek email/slack di luar jam kerja.',
                'Lakukan sesuatu yang purely for joy, zero productivity. Nyanyi, doodle, dance - apapun yang nggak "productive".',
                'Cerita ke teman, therapist, atau mentor tentang workload. Kadang perspective dari luar itu membantu banget.',
            ],
        }
        
        # Supportive closing - encouraging without toxic positivity
        self.supportive_closings = {
            'body_image_shame': [
                'Jerawat itu temporary, tapi kamu itu permanent. Jangan let temporary thing define kamu.',
                'Confidence bukan tentang perfect appearance, tapi tentang accept diri sendiri exactly as is right now.',
                'Orang yang worth knowing itu nggak judge kamu dari jerawat. Mereka lihat kamu sebagai whole person.',
                'Malu itu normal, tapi nggak harus isolate diri. Kamu deserve connection dan support, jerawat atau nggak.',
                'Healing dari shame ini butuh time dan patience sa diri sendiri. Tapi kamu bisa do it.',
            ],
            'insecurity': [
                'Perjalanan insecurity itu panjang, dan improvement nggak linear. Tapi kamu udah di jalan yang bener dengan acknowledge ini.',
                'Percaya sama diri itu skill yang bisa di-practice, dan kamu bisa learn it step by step.',
                'Kamu cukup exactly seperti sekarang, even while working on improvements. Dua-duanya bisa true.',
                'Perubahan kecil itu numpuk. Suatu hari kamu bakal realize self-doubt jadi less frequent.',
            ],
            'fear_of_abandonment': [
                'Ketakutan itu human, dan kamu nggak crazy atau needy karena merasa ini. Itu normal human need.',
                'Hubungan yang sehat butuh both vulnerability dan independence. Kamu lagi learn dua-duanya sekarang.',
                'Trust di hubungan dibangun slow, through consistency. Be patient sa diri sendiri.',
                'Aku harap kamu bisa find yang appreciate kamu exactly for intensity emosi kamu.',
            ],
            'overwhelm': [
                'Jaga diri sendiri bukan selfish, itu essential. Kamu nggak bisa kasih kalau cup kamu kosong.',
                'Minta bantuan bukan weakness. Itu actually courage dan wisdom.',
                'Kamu nggak harus figure everything out hari ini. Pelan-pelan juga tetap termasuk proses.',
                'Rasa kewalahan akan berlalu. Kamu udah survive setiap moment sulit sampai sekarang.',
            ],
            'overthinking': [
                'Pikiran yang overthink adalah pikiran yang sensitive, dan itu strength kalau properly directed.',
                'Belajar quiet mind itu skill, bukan failure. Be gentle sa diri sendiri in the process.',
                'Kamu nggak broken karena overthink. Kamu just perlu tools yang better untuk manage it.',
                'Kecil-kecil kamu probably akan notice thoughts jadi less sticky.',
            ],
            'burnout': [
                'Istirahat bukan pilihan, itu keharusan. Kamu deserve it.',
                'Recovery butuh waktu. Be patient as process dan sa diri sendiri.',
                'Apa yang kamu learn dari burnout ini valuable. Kamu akan more conscious about boundaries next time.',
                'Kamu nggak lemah. Kamu just push diri kamu lebih kuat than humanly possible untuk too long.',
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
            lines.append("Mungkin kamu bisa coba:")
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
