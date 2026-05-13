import { useEffect } from "react";
import { useNavigate } from "react-router";
import { motion } from "motion/react";
import { Heart, Sparkles } from "lucide-react";

export default function Splash() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/onboarding");
    }, 3000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#F8EDED] via-[#FFD6D6] to-[#CDE7FF] flex flex-col items-center justify-center p-6 relative overflow-hidden">
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative z-10"
      >
        <div className="w-32 h-32 bg-white/80 rounded-full flex items-center justify-center shadow-lg backdrop-blur-sm mb-8">
          <motion.div
            initial={{ rotate: 0 }}
            animate={{ rotate: [0, -10, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatDelay: 1 }}
          >
            <Heart className="w-16 h-16 text-[#FFB5B5] fill-[#FFB5B5]" />
          </motion.div>
        </div>

        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="text-center"
        >
          <h1 className="text-4xl mb-3 text-[#2D2D2D]">CurhatBuddy</h1>
          <p className="text-lg text-[#6B6B6B] max-w-xs mx-auto">
            Cerita aja dulu, aku dengerin :)
          </p>
        </motion.div>
      </motion.div>

      <motion.div
        className="absolute top-20 left-10"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: [0.4, 0.8, 0.4], y: [-20, 0, -20] }}
        transition={{ duration: 3, repeat: Infinity }}
      >
        <Sparkles className="w-8 h-8 text-[#FFF4D6]" />
      </motion.div>

      <motion.div
        className="absolute bottom-32 right-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: [0.4, 0.8, 0.4], y: [20, 0, 20] }}
        transition={{ duration: 3, repeat: Infinity, delay: 1 }}
      >
        <Sparkles className="w-6 h-6 text-[#E5D9F2]" />
      </motion.div>

      <motion.div
        className="absolute top-1/3 right-1/4"
        initial={{ scale: 0 }}
        animate={{ scale: [0, 1, 0] }}
        transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
      >
        <div className="w-3 h-3 bg-[#FFD6D6] rounded-full" />
      </motion.div>

      <motion.div
        className="absolute bottom-1/3 left-1/4"
        initial={{ scale: 0 }}
        animate={{ scale: [0, 1, 0] }}
        transition={{ duration: 2, repeat: Infinity, delay: 1.5 }}
      >
        <div className="w-4 h-4 bg-[#CDE7FF] rounded-full" />
      </motion.div>
    </div>
  );
}
