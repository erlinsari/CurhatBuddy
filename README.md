# Chatbot Psikologi: Teman Curhat

Proyek ini adalah prototipe sistem pakar chatbot psikologi dengan pendekatan "teman curhat". Bot dirancang untuk:

- Mendengarkan cerita pengguna secara bebas.
- Menandai gejala psikologis dari keyword extraction.
- Mengajukan pertanyaan hanya untuk gejala yang belum jelas.
- Memberi analisis hanya setelah meminta izin.
- Memberi solusi ringan ketika diminta.
- Bisa dijalankan secara CLI atau lewat antarmuka web.

## Struktur

- `chatbot_psikologi.py`: Modul utama dengan logika knowledge base, inference engine, sesi, dan persona.
- `run_chatbot.py`: Antarmuka CLI sederhana untuk menjalankan bot secara lokal.
- `web_app.py`: Aplikasi web berbasis Flask dengan UI chat modern.
- `templates/index.html`: Halaman web untuk chat.
- `static/style.css`: Gaya tampilan antarmuka web.
- `static/app.js`: Logika chat untuk UI web.
- `requirements.txt`: Daftar dependensi Python.
- `rancangan_chatbot_psikologi.md`: Dokumen desain awal.

## Fitur utama

- `ThemeManager`: Tema persona bot bisa diganti, sekarang tersedia beberapa gaya seperti Teman Curhat, Supportive Sahabat, Coach Santai, Pendengar Santuy, dan Sahabat Ringan.
- `KnowledgeBase`: Basis gejala dengan lebih banyak fakta dan sinonim.
- `InferenceEngine`: Aturan inferensi lebih lengkap untuk mendeteksi pola seperti depresi, burnout, kecemasan, withdrawal sosial, stres hubungan, dan transisi hidup.
- `CurhatBot`: Alur percakapan yang mendengar dulu dan meminta izin sebelum berbagi analisis.
- `web_app.py`: Web UI yang bisa dipakai langsung di browser.

## Cara pakai lewat CLI

1. Buka terminal di folder ini.
2. Jalankan:

```bash
python run_chatbot.py
```

3. Pilih persona bot, lalu mulai curhat.
4. Ketik `exit`, `keluar`, `bye`, atau `quit` untuk keluar.

## Cara pakai lewat Web

1. Pasang dependensi backend:

```bash
pip install -r requirements.txt
```

2. Masuk ke folder UI:

```bash
cd "CurhatBuddy Mobile App Design"
```

3. Pasang dependensi frontend:

```bash
npm install
```

4. Jalankan backend:

```bash
python ..\web_app.py
```

5. Jalankan frontend:

```bash
npm run dev
```

6. Buka browser dan kunjungi alamat yang ditampilkan oleh Vite, biasanya `http://127.0.0.1:5173`.

Jika kamu ingin deploy secara satu server, build frontend dengan `npm run build` dan jalankan backend Python. Backend akan melayani semua file statis dari folder `CurhatBuddy Mobile App Design/dist`.

4. Pilih tema persona, lalu mulai curhat dengan bot.

## Integrasi ke antarmuka lain

Jika ingin memasang bot ini ke aplikasi lain, gunakan modul `chatbot_psikologi.py`:

```python
from chatbot_psikologi import CurhatBot

bot = CurhatBot(theme_name='teman_curhat')
print(bot.get_greeting())
print(bot.process_message('aku capek banget kerjaan numpuk dan susah tidur'))
```

Nilai `theme_name` bisa diganti dengan salah satu tema yang tersedia di `ThemeManager.list_themes()`.
