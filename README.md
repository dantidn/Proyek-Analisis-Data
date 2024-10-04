# Dashboard Bike Sharing

Ini adalah dashboard untuk memvisualisasikan data bike sharing menggunakan Python, Streamlit, dan Matplotlib. Dashboard ini memberikan wawasan tentang pembagian sepeda harian, total pengguna terdaftar dan kasual, penyewaan sepeda berdasarkan jam dan musim, dan banyak lagi.

## Fitur
- **Ringkasan Pembagian Sepeda Harian**: Menampilkan total penyewaan sepeda, pengguna terdaftar, dan pengguna kasual.
- **Wawasan Berbasis Waktu**: Menganalisis penyewaan sepeda berdasarkan jam dan melihat waktu paling populer/sedikit.
- **Tren Musiman**: Menampilkan aktivitas penyewaan sepeda di berbagai musim.
- **Perbandingan Pengguna Terdaftar vs Kasual**: Memvisualisasikan proporsi pengguna terdaftar dibandingkan dengan pengguna kasual.

## Prasyarat

Sebelum menjalankan dashboard, pastikan sudah menginstal:

- **Anaconda** atau **Miniconda**
- **Python** (versi 3.8 atau lebih tinggi)
- **Streamlit** (library Python untuk membuat aplikasi web)
- **Matplotlib** (library plotting Python)
- **Pandas** (library untuk manipulasi dan analisis data)
- **Seaborn** (library visualisasi data)

## Petunjuk Setup

### 1. Clone Repositori

Pertama, clone repositori proyek ke mesin lokal.

```bash
git clone https://github.com/dantidn/Proyek-Analisis-Data.git
cd Proyek-Analisis-Data

### 2. Setup Lingkungan Conda

1. Buka Anaconda Prompt
2. Setup Lingkungan Conda:
```bash
conda create --name dashboard-env python=3.9
```bash
conda activate dashboard-env
```bash
pip install -r requirements.txt

### 3. Menjalankan Dashboard
```bash
cd local-directory

```bash
streamlit run dashboard.py

