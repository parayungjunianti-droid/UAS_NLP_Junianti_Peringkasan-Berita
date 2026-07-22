# Sistem Peringkasan Berita Bahasa Indonesia Menggunakan Transformer Abstraktif

Aplikasi web full-stack modern berbasis Flask dan Hugging Face Transformers untuk peringkasan berita Bahasa Indonesia secara otomatis menggunakan metode Abstractive Text Summarization.

## Fitur Utama

- **Peringkasan Abstraktif Otomatis:** Menggunakan model Transformer multi-bahasa (`csebuetnlp/mT5_multilingual_XLSum`) untuk menghasilkan ringkasan berbasis makna.
- **Visualisasi Preprocessing:** Menampilkan tahapan Case Folding, Tokenisasi, Jumlah Token, dan Panjang Kalimat.
- **Metrik Evaluasi NLP:** Pengujian kuantitatif menggunakan ROUGE-1, ROUGE-2, ROUGE-L, dan BLEU Score.
- **Grafik Interaktif:** Visualisasi metrik evaluasi berbasis Chart.js.
- **Export Hasil:** Dukungan Salin Teks, Unduh TXT, dan Unduh PDF.
- **UI/UX SaaS Premium:** Desain modern responsif dengan tema dominan Kuning Terang.

## Teknologi

- **Backend:** Python 3.10+, Flask 3.0, Hugging Face Transformers, PyTorch, Pandas, NumPy
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS), Bootstrap 5, Bootstrap Icons, Chart.js

## Struktur Proyek

```
project/
│
├── app.py
├── requirements.txt
├── model/
│   └── .gitkeep
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── documentation.html
│   └── evaluation.html
├── dataset/
│   └── news_dataset.csv
├── evaluation/
│   ├── __init__.py
│   └── evaluator.py
├── preprocessing.py
├── summarizer.py
├── utils.py
└── README.md
```

## Cara Menjalankan Aplikasi

1. Clone atau ekstrak repository proyek ini.
2. Buka terminal atau command prompt pada direktori proyek.
3. Install seluruh dependensi yang dibutuhkan:

```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi Flask:

```bash
python app.py
```

5. Buka peramban web dan akses alamat:

```
http://localhost:5000
```

## Endpoints API Flask

- `GET /` : Halaman Utama (Home)
- `POST /summarize` : API Endpoint Peringkasan Berita (JSON Payload)
- `GET /evaluation` : Halaman Evaluasi Model & Grafik Benchmarking
- `GET /documentation` : Halaman Dokumentasi Teknis NLP & Transformer
- `GET /about` : Halaman Informasi Proyek & Spesifikasi Software
