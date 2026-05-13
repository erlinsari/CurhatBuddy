import { useState, useEffect } from "react";
import { useNavigate } from "react-router";
import { motion } from "motion/react";
import { ArrowLeft, Heart, TrendingUp, Lightbulb, AlertCircle, CheckCircle } from "lucide-react";

interface InsightPanel {
  title: string;
  content: string;
  color: string;
}

interface InsightData {
  emotional: InsightPanel;
  patterns: InsightPanel;
  factors: InsightPanel;
  suggestions: string[];
  summary: string;
}

const defaultInsights = {
  emotional: {
    title: "Kondisi Emosional",
    content: "Sepertinya akhir-akhir ini kamu lagi banyak tekanan ya. Ada tanda-tanda kamu mulai kelelahan secara emosional.",
    color: "#FFD6D6",
  },
  patterns: {
    title: "Pola yang Terlihat",
    content: "Dari cerita kamu, keliatan kalau kamu sering overthinking tentang hal-hal kecil, dan itu bikin kamu capek.",
    color: "#CDE7FF",
  },
  factors: {
    title: "Faktor Penyebab",
    content: "Kemungkinan besar karena workload yang terlalu banyak dan ekspektasi yang tinggi dari diri sendiri.",
    color: "#FFF4D6",
  },
};

export default function Insight() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [insightData, setInsightData] = useState<InsightData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    fetchInsight();
  }, []);

  const fetchInsight = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/insight");
      if (!response.ok) {
        throw new Error("Gagal mengambil insight dari server.");
      }
      const data: InsightData = await response.json();
      setInsightData(data);
      setTimeout(() => {
        setShowContent(true);
      }, 300);
    } catch (err) {
      setError("Gagal mengambil insight. Pastikan backend berjalan dan coba lagi.");
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] to-[#F8EDED] dark:from-[#1A1A1A] dark:to-[#2D2D2D] flex flex-col items-center justify-center p-6">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="text-center"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-16 h-16 border-4 border-[#FFD6D6] dark:border-[#FFB5B5] border-t-[#FFB5B5] dark:border-t-[#FFD6D6] rounded-full mx-auto mb-6"
          />
          <h2 className="text-xl text-[#2D2D2D] dark:text-[#F5F5F5] mb-2">Lagi aku analisis ya...</h2>
          <p className="text-[#6B6B6B] dark:text-[#A0A0A0]">Sebentar lagi selesai</p>
        </motion.div>
      </div>
    );
  }

  const insights = insightData || defaultInsights;
  const suggestions = insightData?.suggestions || [
    "Coba luangin waktu 10-15 menit sehari buat journaling. Nulis perasaan kamu bisa bantu.",
    "Jangan lupa istirahat yang cukup. Sleep deprivation bisa bikin emotional regulation menurun.",
    "Kalau memungkinkan, coba komunikasikan beban kerja kamu ke atasan atau tim.",
    "Set boundaries antara waktu kerja dan personal time. Nggak perlu available 24/7.",
    "Consider terapi atau konseling kalau kamu merasa butuh bantuan lebih lanjut.",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] to-[#F8EDED] dark:from-[#1A1A1A] dark:to-[#2D2D2D]">
      <div className="bg-white/80 dark:bg-[#2D2D2D]/80 backdrop-blur-sm border-b border-[#E0E0E0] dark:border-[#3A3A3A] sticky top-0 z-10">
        <div className="max-w-md mx-auto px-6 py-4 flex items-center justify-between">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate("/home")}
            className="p-2 rounded-full hover:bg-[#F8EDED] dark:hover:bg-[#3A3A3A] transition-colors"
          >
            <ArrowLeft className="w-6 h-6 text-[#2D2D2D] dark:text-[#F5F5F5]" />
          </motion.button>

          <h2 className="text-xl text-[#2D2D2D] dark:text-[#F5F5F5]">Insight untuk Kamu</h2>

          <div className="w-10" />
        </div>
      </div>

      <div className="max-w-md mx-auto px-6 py-8 pb-24">
        {error ? (
          <div className="bg-white dark:bg-[#2D2D2D] rounded-3xl p-6 shadow-md text-center">
            <p className="text-[#2D2D2D] dark:text-[#F5F5F5] mb-4">{error}</p>
            <button
              onClick={fetchInsight}
              className="bg-[#FFB5B5] text-[#2D2D2D] dark:text-[#1A1A1A] px-6 py-3 rounded-full shadow-md"
            >
              Coba lagi
            </button>
          </div>
        ) : (
          <>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: showContent ? 1 : 0, y: showContent ? 0 : 20 }}
              transition={{ duration: 0.5 }}
              className="mb-6"
            >
              <div className="bg-gradient-to-br from-[#E5D9F2] to-[#FFD6D6] dark:from-[#5C4D3C] dark:to-[#FFB5B5] rounded-3xl p-6 shadow-lg">
                <Lightbulb className="w-8 h-8 text-[#2D2D2D] dark:text-[#1A1A1A] mb-3" />
                <p className="text-lg text-[#2D2D2D] dark:text-[#1A1A1A] leading-relaxed">
                  {insightData?.summary ||
                    "Aku udah lihat dari cerita-cerita kamu. Ini bukan diagnosis medis ya, tapi lebih ke insight emosional yang mungkin bisa bantu kamu lebih ngerti diri sendiri."}
                </p>
              </div>
            </motion.div>

            <div className="space-y-4 mb-8">
              {(["emotional", "patterns", "factors"] as const).map((key, index) => {
                const insight = insights[key];
                const Icon = key === "emotional" ? Heart : key === "patterns" ? TrendingUp : AlertCircle;
                return (
                  <motion.div
                    key={key}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: showContent ? 1 : 0, x: showContent ? 0 : -20 }}
                    transition={{ delay: 0.2 + index * 0.1, duration: 0.5 }}
                    className="bg-white dark:bg-[#2D2D2D] rounded-3xl p-5 shadow-md"
                  >
                    <div className="flex items-start gap-4">
                      <div
                        className="w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0"
                        style={{ backgroundColor: insight.color }}
                      >
                        <Icon className="w-6 h-6 text-[#2D2D2D]" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg text-[#2D2D2D] dark:text-[#F5F5F5] mb-2">{insight.title}</h3>
                        <p className="text-[#6B6B6B] dark:text-[#A0A0A0] leading-relaxed">{insight.content}</p>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: showContent ? 1 : 0, y: showContent ? 0 : 20 }}
              transition={{ delay: 0.6, duration: 0.5 }}
            >
              <h3 className="text-xl text-[#2D2D2D] dark:text-[#F5F5F5] mb-4 flex items-center gap-2">
                <CheckCircle className="w-6 h-6 text-[#FFB5B5]" />
                Saran dari Aku
              </h3>

              <div className="bg-white dark:bg-[#2D2D2D] rounded-3xl p-5 shadow-md">
                <p className="text-[#6B6B6B] dark:text-[#A0A0A0] mb-4 leading-relaxed">
                  Ini beberapa hal kecil yang mungkin bisa kamu coba. Nggak perlu semuanya sekaligus, pelan-pelan aja ya:
                </p>

                <div className="space-y-3">
                  {suggestions.map((suggestion, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: showContent ? 1 : 0, x: showContent ? 0 : -10 }}
                      transition={{ delay: 0.7 + index * 0.1, duration: 0.4 }}
                      className="flex gap-3"
                    >
                      <div className="w-6 h-6 bg-[#FFD6D6] dark:bg-[#FFB5B5] rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <span className="text-xs text-[#2D2D2D]">{index + 1}</span>
                      </div>
                      <p className="text-[#2D2D2D] dark:text-[#F5F5F5] leading-relaxed flex-1">{suggestion}</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: showContent ? 1 : 0 }}
              transition={{ delay: 1.2, duration: 0.5 }}
              className="mt-8"
            >
              <div className="bg-gradient-to-br from-[#CDE7FF] to-[#E5D9F2] dark:from-[#4A6FA5] dark:to-[#5C4D3C] rounded-3xl p-5 text-center">
                <p className="text-[#2D2D2D] dark:text-[#F5F5F5] leading-relaxed mb-4">
                  Remember, kamu nggak sendirian. Aku selalu di sini kalau kamu butuh temen ngobrol 💙
                </p>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => navigate("/chat")}
                  className="bg-white dark:bg-[#FFB5B5] text-[#2D2D2D] dark:text-[#1A1A1A] px-6 py-3 rounded-full shadow-md"
                >
                  Lanjut Ngobrol
                </motion.button>
              </div>
            </motion.div>
          </>
        )}
      </div>
    </div>
  );
}
