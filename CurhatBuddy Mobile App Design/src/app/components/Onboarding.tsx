import { useState } from "react";
import { useNavigate } from "react-router";
import { motion, AnimatePresence } from "motion/react";
import { Shield, MessageCircle, Lightbulb, ChevronRight } from "lucide-react";

const slides = [
  {
    icon: Shield,
    title: "Di sini kamu bebas cerita tanpa takut dihakimi.",
    description: "Semua yang kamu ceritakan aman dan privat. Nggak ada yang bakal menghakimi kamu.",
    color: "#FFD6D6",
  },
  {
    icon: MessageCircle,
    title: "Aku bakal nemenin ngobrol, bukan langsung menggurui.",
    description: "Aku di sini buat dengerin kamu. Kamu bisa cerita apa aja dengan nyaman.",
    color: "#CDE7FF",
  },
  {
    icon: Lightbulb,
    title: "Kalau kamu mau, nanti aku juga bisa bantu kasih saran pelan-pelan.",
    description: "Setelah kamu merasa lebih baik, kita bisa sama-sama cari solusinya.",
    color: "#FFF4D6",
  },
];

export default function Onboarding() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const navigate = useNavigate();

  const handleNext = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1);
    } else {
      navigate("/home");
    }
  };

  const slide = slides[currentSlide];
  const Icon = slide.icon;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] to-[#F8EDED] flex flex-col p-6">
      <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.4 }}
            className="text-center w-full"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="mb-12"
            >
              <div
                className="w-28 h-28 rounded-full mx-auto flex items-center justify-center shadow-lg"
                style={{ backgroundColor: slide.color }}
              >
                <Icon className="w-14 h-14 text-[#2D2D2D]" />
              </div>
            </motion.div>

            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-2xl mb-4 text-[#2D2D2D] px-4 leading-relaxed"
            >
              {slide.title}
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-lg text-[#6B6B6B] px-6 leading-relaxed"
            >
              {slide.description}
            </motion.p>
          </motion.div>
        </AnimatePresence>
      </div>

      <div className="space-y-4 max-w-md mx-auto w-full">
        <div className="flex justify-center gap-2 mb-6">
          {slides.map((_, index) => (
            <motion.div
              key={index}
              className="h-2 rounded-full transition-all duration-300"
              style={{
                width: currentSlide === index ? "32px" : "8px",
                backgroundColor: currentSlide === index ? "#FFB5B5" : "#E0E0E0",
              }}
            />
          ))}
        </div>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleNext}
          className="w-full bg-[#FFB5B5] text-[#2D2D2D] py-4 rounded-3xl flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transition-shadow"
        >
          <span className="text-lg">{currentSlide === slides.length - 1 ? "Mulai Cerita" : "Lanjut"}</span>
          <ChevronRight className="w-5 h-5" />
        </motion.button>

        {currentSlide < slides.length - 1 && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            onClick={() => navigate("/home")}
            className="w-full text-[#6B6B6B] py-3 rounded-3xl"
          >
            Lewati
          </motion.button>
        )}
      </div>
    </div>
  );
}
