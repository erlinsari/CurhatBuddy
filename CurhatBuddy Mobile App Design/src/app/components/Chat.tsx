import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router";
import { motion, AnimatePresence } from "motion/react";
import { Send, ArrowLeft, Sparkles, MoreVertical } from "lucide-react";
import EmergencyButton from "./EmergencyButton";

interface Message {
  id: number;
  text: string;
  sender: "user" | "ai";
  timestamp: Date;
}

export default function Chat() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [loading, setLoading] = useState(true);
  const [insightAvailable, setInsightAvailable] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    startConversation();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const startConversation = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const response = await fetch("/api/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ theme: "teman_curhat" }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessages([
          {
            id: Date.now(),
            text: data.reply || "Hai! Aku di sini buat dengerin kamu.",
            sender: "ai",
            timestamp: new Date(),
          },
        ]);
        setInsightAvailable(Boolean(data.analysis_available));
      } else {
        setMessages([
          {
            id: Date.now(),
            text: data.error || "Gagal memulai percakapan. Coba refresh.",
            sender: "ai",
            timestamp: new Date(),
          },
        ]);
      }
    } catch (error) {
      setMessages([
        {
          id: Date.now(),
          text: "Gagal terhubung ke server. Pastikan backend berjalan.",
          sender: "ai",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      text: inputText,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setErrorMessage(null);
    setIsTyping(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: inputText, theme: "teman_curhat" }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            text: data.reply,
            sender: "ai",
            timestamp: new Date(),
          },
        ]);
        setInsightAvailable(Boolean(data.analysis_available));
      } else {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            text: data.error || "Maaf, ada masalah saat mengirim pesan.",
            sender: "ai",
            timestamp: new Date(),
          },
        ]);
      }
    } catch (error) {
      setErrorMessage("Gagal terhubung ke server. Coba lagi nanti.");
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#FAFAFA] to-[#F8EDED] dark:from-[#1A1A1A] dark:to-[#2D2D2D] flex flex-col">
      <EmergencyButton />
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

          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-[#FFD6D6] to-[#FFB5B5] rounded-full flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-[#2D2D2D]" />
            </div>
            <div>
              <h2 className="text-lg text-[#2D2D2D] dark:text-[#F5F5F5]">CurhatBuddy</h2>
              <p className="text-xs text-[#6B6B6B] dark:text-[#A0A0A0]">Online</p>
            </div>
          </div>

          <button className="p-2 rounded-full hover:bg-[#F8EDED] dark:hover:bg-[#3A3A3A] transition-colors">
            <MoreVertical className="w-6 h-6 text-[#2D2D2D] dark:text-[#F5F5F5]" />
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-6 max-w-md mx-auto w-full">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-[#6B6B6B] dark:text-[#A0A0A0]">Memulai percakapan...</div>
          </div>
        ) : (
          <>
            <AnimatePresence>
              {messages.map((message, index) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className={`flex mb-4 ${message.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[75%] rounded-3xl px-5 py-3 shadow-md ${
                      message.sender === "user"
                        ? "bg-[#FFB5B5] text-[#2D2D2D]"
                        : "bg-white dark:bg-[#3A3A3A] text-[#2D2D2D] dark:text-[#F5F5F5]"
                    }`}
                  >
                    <p className="leading-relaxed">{message.text}</p>
                    <p className="text-xs mt-1 opacity-60">
                      {message.timestamp.toLocaleTimeString("id-ID", {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {isTyping && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex justify-start mb-4"
              >
                <div className="bg-white dark:bg-[#3A3A3A] rounded-3xl px-5 py-3 shadow-md">
                  <div className="flex gap-1">
                    <motion.div
                      className="w-2 h-2 bg-[#6B6B6B] rounded-full"
                      animate={{ y: [0, -8, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-[#6B6B6B] rounded-full"
                      animate={{ y: [0, -8, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-[#6B6B6B] rounded-full"
                      animate={{ y: [0, -8, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                    />
                  </div>
                </div>
              </motion.div>
            )}

            {errorMessage && (
              <div className="text-sm text-red-600 dark:text-red-400 mb-4">{errorMessage}</div>
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {insightAvailable && (
        <div className="px-6 pb-2 max-w-md mx-auto w-full">
          <button
            onClick={() => navigate("/insight")}
            className="w-full bg-[#CDE7FF] dark:bg-[#4A6FA5] text-[#2D2D2D] dark:text-[#F5F5F5] py-3 rounded-2xl shadow-md mb-3"
          >
            Lihat Insight
          </button>
        </div>
      )}

      <div className="bg-white/80 dark:bg-[#2D2D2D]/80 backdrop-blur-sm border-t border-[#E0E0E0] dark:border-[#3A3A3A] sticky bottom-0">
        <div className="max-w-md mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
              placeholder="Cerita aja di sini..."
              className="flex-1 bg-[#F8EDED] dark:bg-[#3A3A3A] text-[#2D2D2D] dark:text-[#F5F5F5] placeholder:text-[#6B6B6B] dark:placeholder:text-[#A0A0A0] rounded-full px-5 py-3 outline-none focus:ring-2 focus:ring-[#FFD6D6] dark:focus:ring-[#FFB5B5] transition-all"
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSend}
              disabled={!inputText.trim() || loading || isTyping}
              className="bg-[#FFB5B5] p-3 rounded-full shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5 text-[#2D2D2D]" />
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  );
}
