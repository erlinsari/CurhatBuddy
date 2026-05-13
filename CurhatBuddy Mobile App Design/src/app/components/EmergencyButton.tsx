import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Phone, X } from "lucide-react";

const emergencyContacts = [
  {
    name: "Hotline Kesehatan Mental",
    number: "119 ext. 8",
    description: "24 jam, gratis, rahasia",
  },
  {
    name: "Into The Light",
    number: "+62 812-9568-5090",
    description: "Konseling via WhatsApp",
  },
  {
    name: "Sejiwa",
    number: "119 ext. 8",
    description: "Pencegahan bunuh diri",
  },
];

export default function EmergencyButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-br from-[#FF6B6B] to-[#FF8E8E] rounded-full shadow-lg flex items-center justify-center z-50"
      >
        <Phone className="w-6 h-6 text-white" />
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            />

            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 50, scale: 0.9 }}
              className="fixed bottom-0 left-0 right-0 bg-white dark:bg-[#2D2D2D] rounded-t-3xl p-6 z-50 max-h-[80vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl text-[#2D2D2D] dark:text-[#F5F5F5]">Butuh Bantuan Segera?</h2>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 rounded-full hover:bg-[#F8EDED] dark:hover:bg-[#3A3A3A] transition-colors"
                >
                  <X className="w-6 h-6 text-[#2D2D2D] dark:text-[#F5F5F5]" />
                </button>
              </div>

              <p className="text-[#6B6B6B] dark:text-[#A0A0A0] mb-6 leading-relaxed">
                Kalau kamu sedang dalam krisis atau butuh bantuan profesional sekarang, hubungi nomor di
                bawah ini:
              </p>

              <div className="space-y-4">
                {emergencyContacts.map((contact, index) => (
                  <motion.a
                    key={index}
                    href={`tel:${contact.number}`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="block bg-[#F8EDED] dark:bg-[#3A3A3A] rounded-2xl p-4 hover:shadow-lg transition-shadow"
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <Phone className="w-5 h-5 text-[#FF6B6B]" />
                      <h3 className="text-lg text-[#2D2D2D] dark:text-[#F5F5F5]">{contact.name}</h3>
                    </div>
                    <p className="text-xl text-[#FF6B6B] mb-1">{contact.number}</p>
                    <p className="text-sm text-[#6B6B6B] dark:text-[#A0A0A0]">{contact.description}</p>
                  </motion.a>
                ))}
              </div>

              <div className="mt-6 bg-gradient-to-br from-[#CDE7FF] to-[#E5D9F2] dark:from-[#4A6FA5] dark:to-[#5C4D3C] rounded-2xl p-4">
                <p className="text-sm text-[#2D2D2D] dark:text-[#F5F5F5] leading-relaxed">
                  💙 Kamu penting dan berharga. Jangan ragu untuk mencari bantuan profesional kalau kamu
                  membutuhkannya.
                </p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
