# 🚲🚲 Dashboard Bike Sharing 🚲🚲

Ini adalah dashboard untuk memvisualisasikan data bike sharing menggunakan Python, Streamlit, dan Matplotlib. Dashboard ini memberikan wawasan tentang pembagian sepeda harian, total pengguna terdaftar dan kasual, penyewaan sepeda berdasarkan jam dan musim, dan banyak lagi.

## Fitur
- **Ringkasan Pembagian Sepeda Harian**: Menampilkan total penyewaan sepeda, pengguna terdaftar, dan pengguna kasual.
- **Wawasan Berbasis Waktu**: Menganalisis penyewaan sepeda berdasarkan jam dan melihat waktu paling populer/sedikit.
- **Perbandingan Pengguna Terdaftar vs Kasual**: Memvisualisasikan proporsi pengguna terdaftar dibandingkan dengan pengguna kasual.

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir submission
cd submission
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```