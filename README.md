# E-Commerce Data Analytics Project

## Project Overview
Proyek ini merupakan implementasi dari siklus analisis data lengkap menggunakan **E-Commerce Public Dataset**. Tujuan utama dari proyek ini adalah untuk menganalisis performa penjualan, tren pendapatan bulanan, kategori produk terbaik, serta melakukan segmentasi pelanggan menggunakan metode **RFM (Recency, Frequency, Monetary)**. Hasil analisis disajikan dalam bentuk dashboard interaktif guna mendukung pengambilan keputusan strategis dalam bisnis.

## Project Structure
- **`/dashboard`**: Berisi file utama aplikasi dashboard (`dashboard.py`) dan dataset yang telah dibersihkan (`main_data.csv`).
- **`notebook.ipynb`**: Dokumentasi teknis proses analisis data (Data Wrangling, Exploratory Data Analysis, Visualization).
- **`requirements.txt`**: Daftar pustaka (*libraries*) Python yang diperlukan.
- **`README.md`**: Dokumentasi utama proyek.

## Setup Environment

### 1. Menggunakan venv (Virtual Environment)
```bash
# Membuat environment
python -m venv env

# Aktivasi environment
source env/bin/activate  # Untuk Linux/Mac
.\env\Scripts\activate   # Untuk Windows

# Instalasi Dependencies
pip install -r dashboard/requirements.txt

```

### 2. Menggunakan Conda
```bash
# Membuat dan mengaktifkan environment
conda create --name ecommerce-project python=3.9
conda activate ecommerce-project

# Instalasi Dependencies
pip install -r dashboard/requirements.txt
```

## Running Dashboard

streamlit run dashboard.py

## Live Dashboard URL
Anda dapat mengakses dashboard yang telah dideploy secara publik melalui tautan berikut: https://ecommerce-public-dash.streamlit.app/

## Business Insights

Berdasarkan hasil analisis data yang telah dilakukan, diperoleh beberapa poin penting sebagai berikut:

### Tren Pendapatan Bulanan
* **Fluktuasi Kinerja:** Analisis menunjukkan adanya fluktuasi performa penjualan bulanan yang dinamis sepanjang periode pengamatan[cite: 5, 7].
* **Periode Puncak (*Peak Performance*):** Terdapat bulan-bulan tertentu yang mencatatkan lonjakan volume transaksi dan pendapatan tertinggi secara signifikan[cite: 5, 7].

### Kategori Produk
* **Produk Unggulan:** Terdapat kategori produk tertentu yang secara konsisten mendominasi jumlah total pesanan (*total orders*)[cite: 5, 7].
* **Kontribusi Pendapatan:** Kategori produk teratas memberikan kontribusi terbesar terhadap total pendapatan keseluruhan perusahaan[cite: 5, 7].

### Segmentasi Pelanggan (*RFM Analysis*)
* **Klaster Pelanggan:** Pelanggan berhasil dikelompokkan ke dalam beberapa segmen menggunakan metode *Recency, Frequency, and Monetary*[cite: 5, 7].
* **Identifikasi Loyalitas:** Analisis ini memudahkan identifikasi kelompok *best customers*, pola pembelian ulang, serta tingkat loyalitas pelanggan secara keseluruhan[cite: 5, 7].

---

## Action Items & Recommendations

### Strategi Pemasaran Berbasis RFM
* **Retensi Pelanggan Utama:** Memfokuskan program promosi khusus (seperti penawaran eksklusif atau *loyalty rewards*) kepada kelompok pelanggan dengan skor **Monetary** dan **Frequency** tertinggi[cite: 5, 7].
* **Re-engagement:** Merancang strategi kampanye terarah untuk merangkul kembali pelanggan yang sudah lama tidak melakukan transaksi (*churned customers*)[cite: 5, 7].

### Optimalisasi Stok Kategori Unggulan
* **Manajemen Inventaris:** Meningkatkan ketersediaan stok dan variasi produk pada kategori yang paling diminati pasar[cite: 5, 7].
* **Maksimalisasi Potensi:** Mengoptimalkan penawaran dan penempatan produk unggulan guna mendongkrak total pendapatan perusahaan[cite: 5, 7].

### Manajemen Musim Penjualan
* **Kampanye *Low Season*:** Memanfaatkan pola tren bulanan untuk merancang strategi kampanye pemasaran atau diskon khusus pada periode dengan volume transaksi rendah[cite: 5, 7].
* **Efisiensi Operasional:** Mengantisipasi siklus musiman penjualan untuk menjaga kestabilan arus kas dan operasional bisnis sepanjang tahun[cite: 5, 7].
