import { useState } from "react";
import { useNavigate } from "react-router";
import { motion } from "motion/react";
import { MessageCircle, Calendar, Smile, Meh, Frown, Heart, Sparkles, TrendingUp } from "lucide-react";
import DarkModeToggle from "./DarkModeToggle";
import EmergencyButton from "./EmergencyButton";

const moodOptions = [
  { emoji: "😊", label: "Senang", icon: Smile, color: "#FFD6D6" },
  { emoji: "😐", label: "Biasa aja", icon: Meh, color: "#CDE7FF" },
  { emoji: "😢", label: "Sedih", icon: Frown, color: "#E5D9F2" },
];

const chatHistory = [
  { id: 1, preview: "Hari ini aku merasa sedikit lebih baik...", time: "2 jam lalu", mood: "😊" },
  { id: 2, preview: "Kerjaannya banyak banget, rasanya...", time: "Kemarin", mood: "😐" },
  { id: 3, preview: "Aku nggak tau harus cerita ke siapa...", time: "3 hari lalu", mood: "😢" },
];

const affirmations = [
  "Kamu udah keren banget bertahan sampai hari ini 💪",
  "Perasaan kamu valid, dan itu oke banget buat dirasain ✨",
  "Langkah kecil itu tetap langkah maju, kok 🌱",
  "Kamu nggak sendirian, aku di sini buat dengerin 💙",
  "Bad days happen, tapi kamu stronger than you think 🌟",
];

export default function Home() {
  const navigate = useNavigate();
  const [selectedMood, setSelectedMood] = useState<number | null>(null);
  const [dailyAffirmation] = useState(affirmations[Math.floor(Math.random() * affirmations.length)]);

  const currentHour = new Date().getHours();
  const greeting = currentHour < 12 ? "Selamat pagi" : currentHour < 18 ? "Selamat siang" : "Selamat malam";

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] to-[#F8EDED] dark:from-[#1A1A1A] dark:to-[#2D2D2D] pb-24">
      <div className="max-w-md mx-auto px-6 pt-12">
        <div className="fixed top-6 right-6 z-40">
          <DarkModeToggle />
        </div>

        <EmergencyButton />
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl text-[#2D2D2D] dark:text-[#F5F5F5] mb-2">{greeting} 👋</h1>
          <p className="text-lg text-[#6B6B6B] dark:text-[#A0A0A0]">Gimana kabarnya hari ini?</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-[#FFD6D6] to-[#FFB5B5] rounded-3xl p-6 mb-6 shadow-lg"
        >
          <div className="flex items-start gap-3 mb-4">
            <Sparkles className="w-6 h-6 text-[#2D2D2D] dark:text-[#2D2D2D] flex-shrink-0 mt-1" />
            <p className="text-lg text-[#2D2D2D] dark:text-[#2D2D2D] leading-relaxed">{dailyAffirmation}</p>
          </div>
        </motion.div>

        <motion.button
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => navigate("/chat")}
          className="w-full bg-[#FFB5B5] dark:bg-[#FFB5B5] text-[#2D2D2D] dark:text-[#1A1A1A] py-5 rounded-3xl flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transition-shadow mb-8"
        >
          <MessageCircle className="w-6 h-6" />
          <span className="text-xl">Mulai Curhat</span>
        </motion.button>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-8"
        >
          <h3 className="text-lg text-[#2D2D2D] dark:text-[#F5F5F5] mb-4 flex items-center gap-2">
            <Heart className="w-5 h-5 text-[#FFB5B5]" />
            Mood kamu hari ini
          </h3>
          <div className="flex gap-3">
            {moodOptions.map((mood, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setSelectedMood(index)}
                className="flex-1 bg-white dark:bg-[#2D2D2D] rounded-2xl p-4 shadow-md flex flex-col items-center gap-2 transition-all"
                style={{
                  borderWidth: selectedMood === index ? "2px" : "0px",
                  borderColor: selectedMood === index ? mood.color : "transparent",
                }}
              >
                <span className="text-3xl">{mood.emoji}</span>
                <span className="text-sm text-[#6B6B6B] dark:text-[#A0A0A0]">{mood.label}</span>
              </motion.button>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h3 className="text-lg text-[#2D2D2D] dark:text-[#F5F5F5] mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-[#CDE7FF]" />
            Riwayat Obrolan
          </h3>
          <div className="space-y-3">
            {chatHistory.map((chat, index) => (
              <motion.button
                key={chat.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => navigate("/chat")}
                className="w-full bg-white dark:bg-[#2D2D2D] rounded-2xl p-4 shadow-md flex items-center gap-3 text-left hover:shadow-lg transition-shadow"
              >
                <span className="text-2xl">{chat.mood}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-[#2D2D2D] dark:text-[#F5F5F5] truncate mb-1">{chat.preview}</p>
                  <p className="text-sm text-[#6B6B6B] dark:text-[#A0A0A0]">{chat.time}</p>
                </div>
                <TrendingUp className="w-5 h-5 text-[#6B6B6B] dark:text-[#A0A0A0] flex-shrink-0" />
              </motion.button>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
