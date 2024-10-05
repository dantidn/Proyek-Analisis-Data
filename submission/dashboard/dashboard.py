import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menampilkan path executable Python yang digunakan
print("Python executable yang digunakan:", sys.executable)

# Set gaya Seaborn
sns.set(style='darkgrid')

def get_hourly_counts(hour_data):
    """Mengelompokkan data berdasarkan jam dan menghitung jumlah total."""
    return hour_data.groupby(by="hr").agg({"cnt": "sum"})

def filter_days_in_year(day_data):
    """Memfilter data untuk tahun 2011."""
    return day_data.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')

def calculate_total_registered(day_data):
    """Menghitung jumlah total pengguna terdaftar per hari."""
    registered_count = day_data.groupby(by="dteday").agg({"registered": "sum"})
    registered_count = registered_count.reset_index()
    registered_count.rename(columns={"registered": "total_registered"}, inplace=True)
    return registered_count

def calculate_total_casual(day_data):
    """Menghitung jumlah total pengguna kasual per hari."""
    casual_count = day_data.groupby(by="dteday").agg({"casual": "sum"})
    casual_count = casual_count.reset_index()
    casual_count.rename(columns={"casual": "total_casual"}, inplace=True)
    return casual_count

def summarize_orders(hour_data):
    """Menyimpulkan total pesanan berdasarkan jam."""
    return hour_data.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()

def analyze_seasonal_data(day_data):
    """Menganalisis data penyewaan sepeda berdasarkan musim."""
    return day_data.groupby(by="season").cnt.sum().reset_index()

# Memuat dataset
day_data = pd.read_csv("../data/day.csv")
hour_data = pd.read_csv("../data/hour.csv")

# Mengurutkan dan mereset index untuk kolom tanggal
datetime_columns = ["dteday"]
day_data.sort_values(by="dteday", inplace=True)
hour_data.sort_values(by="dteday", inplace=True)

# Mengubah kolom tanggal menjadi format datetime
for column in datetime_columns:
    day_data[column] = pd.to_datetime(day_data[column])
    hour_data[column] = pd.to_datetime(hour_data[column])

# Mendapatkan tanggal minimum dan maksimum untuk penyaringan
min_day_date = day_data["dteday"].min()
max_day_date = day_data["dteday"].max()
min_hour_date = hour_data["dteday"].min()
max_hour_date = hour_data["dteday"].max()

# Sidebar untuk pemilihan tanggal
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://wwo.moqo.de/web/image/4688-9c26d8bd/mq%20-%20product%20-%20bikesharing%20%3E%20s2%20-%20g1.png")
    
    # Input rentang tanggal
    selected_dates = st.date_input(
        label='Pilih Rentang Tanggal',
        min_value=min_day_date,
        max_value=max_day_date,
        value=[min_day_date, max_day_date]
    )

# Memfilter dataset berdasarkan rentang tanggal yang dipilih
filtered_day_data = day_data[(day_data["dteday"] >= str(selected_dates[0])) & 
                              (day_data["dteday"] <= str(selected_dates[1]))]

filtered_hour_data = hour_data[(hour_data["dteday"] >= str(selected_dates[0])) & 
                                (hour_data["dteday"] <= str(selected_dates[1]))]

# Melakukan agregasi data
hourly_count_data = get_hourly_counts(filtered_hour_data)
day_count_2011 = filter_days_in_year(filtered_day_data)
total_registered_data = calculate_total_registered(filtered_day_data)
total_casual_data = calculate_total_casual(filtered_day_data)
summarized_orders = summarize_orders(filtered_hour_data)
seasonal_analysis = analyze_seasonal_data(filtered_hour_data)

# Membuat dashboard dengan visualisasi data
st.header('Analisis Penyewaan Sepeda :sparkles:')

st.subheader('Penyewaan Sepeda Harian')
col1, col2, col3 = st.columns(3)

with col1:
    total_bike_rentals = day_count_2011.cnt.sum()
    st.metric("Total Penyewaan Sepeda", value=total_bike_rentals)

with col2:
    total_registered = total_registered_data.total_registered.sum()
    st.metric("Total Pengguna Terdaftar", value=total_registered)

with col3:
    total_casual = total_casual_data.total_casual.sum()
    st.metric("Total Pengguna Kasual", value=total_casual)

st.subheader("Jam berapa yang menunjukkan permintaan tertinggi dan terendah untuk penyewaan sepeda?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
st.caption("Grafik menunjukkan bahwa jam 17.00 adalah waktu paling sibuk untuk menyewa sepeda, dengan hampir 350.000 unit. Sebaliknya, jam 04.00 menunjukkan permintaan terendah dengan kurang dari 5.000 penyewaan.")

# Grafik untuk jam dengan penyewaan tertinggi
sns.barplot(x="hr", y="cnt", data=summarized_orders.head(5), palette=["#98FB98", "#98FB98", "#98FB98", "#98FB98", "#32CD32"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam (PM)", fontsize=30)
ax[0].set_title("Jam dengan Penyewaan Sepeda Tertinggi", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Grafik untuk jam dengan penyewaan terendah
sns.barplot(x="hr", y="cnt", data=summarized_orders.sort_values(by="hr").head(5), palette=["#98FB98", "#98FB98", "#98FB98", "#98FB98", "#32CD32"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam (AM)", fontsize=30)
ax[1].set_title("Jam dengan Penyewaan Sepeda Terendah", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Berapa kontribusi pengguna terdaftar dan pengguna kasual terhadap total penyewaan?")
st.caption("Pengguna terdaftar berkontribusi sebesar 81,2%, sedangkan pengguna kasual berkontribusi sebesar 18,8%.")

labels = ['Kasual', 'Terdaftar']
sizes = [18.8, 81.2]
explode = (0, 0.1)  # hanya meledakkan irisan kedua

# Grafik pie untuk kontribusi pengguna
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=["#98FB98", "#32CD32"], shadow=True, startangle=90)
ax1.axis('equal')  # Rasio aspek yang sama memastikan pie digambar sebagai lingkaran.

st.pyplot(fig1)
