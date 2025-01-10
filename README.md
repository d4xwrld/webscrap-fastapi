# 🌐 Web Scraper dengan FastAPI

Proyek scraping web canggih untuk mengekstrak konten artikel dari Antara News (antaranews.com) menggunakan FastAPI dan MongoDB. Dirancang untuk performa tinggi dengan pendekatan asynchronous.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🚀 Fitur Unggulan

- **REST API Modern**: Dibangun dengan FastAPI untuk performa tinggi dan dokumentasi otomatis
- **Scraping Cerdas**: Menggunakan requests-html untuk ekstraksi konten yang handal
- **Penyimpanan Terdistribusi**: Integrasi MongoDB untuk penyimpanan data yang scalable
- **Kinerja Optimal**: Operasi asynchronous untuk throughput maksimal
- **Ekstraksi Pintar**: Sistem cerdas untuk mengekstrak dan memfilter link relevan
- **Konten Lengkap**: Mengambil detail artikel termasuk judul, penulis, tanggal, dan konten terkait

## 📋 Prasyarat

Sebelum memulai, pastikan sistem Anda memenuhi kebutuhan berikut:

- Python 3.9 atau lebih baru
- MongoDB (berjalan di localhost:27017)
- Virtual environment Python
- Git

## 🛠️ Panduan Instalasi

### 1. Persiapan Repository

```bash
# Clone repository
git clone https://github.com/d4xwrld/webscrap-fastapi/

# Pindah ke direktori proyek
cd webscrap-fastapi
```

### 2. Konfigurasi Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment
# Untuk Linux/Mac:
source venv/bin/activate

# Untuk Windows:
.\venv\Scripts\activate
```

### 3. Instalasi Dependensi

```bash
# Install semua package yang diperlukan
pip install -r requirements.txt
```

## 📦 Dependensi Utama

Berikut adalah package kunci yang digunakan dalam proyek:

```txt
fastapi==0.73.0      # Framework API modern dan cepat
uvicorn==0.17.4      # Server ASGI yang powerful
requests_html==0.10.0 # Library scraping handal
motor==2.5.1         # Driver MongoDB async
pymongo==3.12.0      # Driver MongoDB sync
```

## 🚀 Menjalankan Aplikasi

### Persiapan Database
1. Pastikan MongoDB sudah berjalan:
   ```bash
   # Verifikasi status MongoDB
   mongod --version
   ```

### Menjalankan Server
```bash
# Mode produksi
python app/main.py

# Mode development dengan auto-reload
uvicorn app.server.app:app --reload --host 0.0.0.0 --port 8000
```

## 🔗 Endpoint API

### Root Endpoint
- `GET /`
  - Deskripsi: Endpoint selamat datang
  - Response: Pesan sambutan dan status API

### Scraper Endpoints
- `POST /scraper/`
  - Deskripsi: Menambahkan URL baru untuk di-scrape
  - Request Body: `{"url": "string"}`
  - Response: Object scraper dengan daftar link yang diekstrak

- `GET /scraper/`
  - Deskripsi: Mengambil seluruh data hasil scraping
  - Response: Array dari object scraper

## 📊 Struktur Data

### Model Scraper
```javascript
{
    "links": [
        [
            "https://www.antaranews.com/berita/4575238/artikel-contoh",
            "https://www.antaranews.com/berita/4575246/artikel-lain"
        ]
    ],
    "metadata": {
        "created_at": "2024-01-10T12:00:00Z",
        "status": "completed"
    }
}
```

[Previous documentation sections remain the same until the Alur Kerja Scraping section...]

## 🔧 Penggunaan Tools Scraper (screverything.py)

### Tentang screverything.py
`screverything.py` adalah tool utama untuk melakukan scraping konten artikel setelah URL dikumpulkan melalui API. Tool ini dirancang untuk mengekstrak konten artikel secara mendalam dan terstruktur.

### Cara Penggunaan

1. **Persiapan Awal**
   ```bash
   # Pastikan berada di direktori proyek
   cd webscrap-fastapi
   
   # Aktifkan virtual environment jika belum
   source venv/bin/activate  # Linux/Mac
   # ATAU
   .\venv\Scripts\activate  # Windows
   ```

2. **Menjalankan Scraper**
   ```bash
   # Scraping semua URL yang ada di database
   python app/screverything.py --mode full
   
   # Scraping URL tertentu
   python app/screverything.py --url https://antaranews.com/berita/1234567/judul-artikel
   
   # Mode testing (scraping 5 artikel pertama)
   python app/screverything.py --mode test --limit 5
   ```

3. **Parameter yang Tersedia**
   ```bash
   --mode     : Mode scraping (full/single/test)
   --url      : URL spesifik untuk di-scrape
   --limit    : Batasan jumlah artikel (untuk mode test)
   --verbose  : Level detail output (debug/info/warning)
   ```

### Alur Penggunaan

1. **Pengumpulan URL (via API)**
   - Gunakan endpoint `POST /scraper/` untuk menambah URL
   - URLs akan disimpan di database

2. **Proses Scraping (screverything.py)**
   - Jalankan screverything.py untuk memproses URLs
   - Tool akan mengekstrak konten secara otomatis

3. **Melihat Hasil**
   - Gunakan endpoint `GET /scraper/` untuk melihat hasil
   - Data tersimpan dalam format terstruktur di MongoDB

### Contoh Penggunaan Lengkap

1. **Tambah URL via API**
   ```bash
   curl -X POST "http://localhost:8000/scraper/" \
   -H "Content-Type: application/json" \
   -d '{"url": "https://antaranews.com/berita/1234567/judul-artikel"}'
   ```

2. **Jalankan Scraper**
   ```bash
   # Mode verbose untuk melihat proses detail
   python app/screverything.py --mode full --verbose debug
   ```

3. **Cek Hasil via API**
   ```bash
   curl "http://localhost:8000/scraper/"
   ```

### Output yang Dihasilkan

Tool akan mengekstrak dan menyimpan data dalam format berikut:

```javascript object notation
{
    "article_id": "1234567",
    "url": "https://antaranews.com/berita/1234567/judul-artikel",
    "title": {
        "main": "Judul Utama Artikel",
        "sub": "Sub Judul Jika Ada"
    },
    "content": {
        "text": "Isi artikel lengkap...",
        "paragraphs": ["Paragraf 1", "Paragraf 2", ...],
        "quotes": ["Kutipan 1", "Kutipan 2", ...]
    },
    "metadata": {
        "author": "Nama Penulis",
        "published_date": "2024-01-10T12:00:00Z",
        "category": "Kategori Artikel"
    }
}
```

### Tips Penggunaan

1. **Optimasi Performa**
   - Gunakan mode `test` untuk uji coba awal
   - Atur `--limit` sesuai kapasitas sistem
   - Monitor penggunaan resources

2. **Penanganan Error**
   - Cek log dengan mode `--verbose debug`
   - Perhatikan response code dari website target
   - Gunakan retry mechanism untuk URL yang gagal

3. **Best Practices**
   - Jalankan dalam virtual environment
   - Backup database secara berkala
   - Monitor rate limiting dari website target
   - Gunakan proxy jika diperlukan

### Troubleshooting Umum

1. **Koneksi Gagal**
   ```bash
   # Cek koneksi MongoDB
   python app/screverything.py --check-db
   
   # Coba dengan timeout lebih lama
   python app/screverything.py --mode single --url [URL] --timeout 30
   ```

2. **Rate Limiting**
   ```bash
   # Tambah delay antar request
   python app/screverything.py --mode full --delay 5
   ```

3. **Memory Issues**
   ```bash
   # Batasi jumlah concurrent requests
   python app/screverything.py --mode full --max-concurrent 3
   ```

## 🔄 Alur Kerja Scraping

1. **Penerimaan Request**
   - API menerima URL target
   - Validasi format dan aksesibilitas URL

2. **Ekstraksi Link**
   - Scraper mengunjungi halaman target
   - Mengekstrak semua link yang ada
   - Memfilter link yang relevan (antaranews.com/berita/)

3. **Pemrosesan Konten**
   - Tool scraping memproses setiap link valid
   - Mengekstrak komponen artikel:
     - Judul dan sub-judul
     - Informasi penulis
     - Tanggal publikasi
     - Konten utama
     - Link artikel terkait

4. **Penyimpanan Data**
   - Data yang sudah diproses disimpan ke MongoDB
   - Metadata ditambahkan (timestamp, status, dll)

## ⚠️ Penanganan Error

Sistem dilengkapi penanganan error komprehensif:

- **Validasi URL**
  - Pengecekan format URL
  - Verifikasi aksesibilitas domain

- **Error Scraping**
  - Timeout handling
  - Retry mechanism untuk request gagal
  - Logging error detail

- **Database Error**
  - Connection retry
  - Failover handling
  - Data integrity check

## 👩‍💻 Panduan Pengembangan

### Mode Development
```bash
# Jalankan dengan hot-reload
uvicorn app.server.app:app --reload --host 0.0.0.0 --port 8000
```

### Dokumentasi API
Akses dokumentasi interaktif di:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
