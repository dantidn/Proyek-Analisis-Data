import sys
print("Using Python executable:", sys.executable)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hr").agg({"cnt": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)   

hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date_days = day_df["dteday"].min()
max_date_days = day_df["dteday"].max()

min_date_hour = hour_df["dteday"].min()
max_date_hour = hour_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://wwo.moqo.de/web/image/4688-9c26d8bd/mq%20-%20product%20-%20bikesharing%20%3E%20s2%20-%20g1.png")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = day_df[(day_df["dteday"] >= str(start_date)) & 
                       (day_df["dteday"] <= str(end_date))]

main_df_hour = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                        (hour_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)


st.subheader("Rentang waktu mana yang menunjukkan permintaan tertinggi dan terendah untuk penyewaan sepeda?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
st.caption("Grafik menunjukkan bahwa jam 17.00 merupakan waktu paling sibuk untuk menyewa sepeda dengan jumlah mencapai hampir 350.000 unit. Di sisi lain, jam 04.00 menjadi waktu dengan permintaan paling rendah, hanya sekitar kurang dari  5.000 unit sepeda yang disewa")

sns.barplot(x="hr", y="cnt", data=sum_order_items_df.head(5), palette=["#98FB98", "#98FB98", "#98FB98", "#98FB98", "#32CD32"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="hr", y="cnt", data=sum_order_items_df.sort_values(by="hr", ascending=True).head(5), palette=["#98FB98", "#98FB98", "#98FB98", "#98FB98", "#32CD32"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)


st.subheader("Seberapa besar kontribusi pengguna terdaftar dan pengguna kasual terhadap total penyewaan?")
st.caption("Persentase pengguna yang telah melakukan registrasi adalah 81,2%, sedangkan sisanya sebesar 18,8% merupakan pengguna kasual yang belum melakukan registrasi")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#98FB98", "#32CD32"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)