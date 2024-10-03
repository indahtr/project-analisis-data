import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='datetime').agg({
        "cnt": "sum"
    }).reset_index()
    daily_rentals_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)
    
    return daily_rentals_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit").agg({
        "cnt": "sum"
    }).reset_index()
    byweather_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)
    
    return byweather_df

def create_bymonth_df(df):
    df['month'] = df['datetime'].dt.month
    bymonth_df = df.groupby(by="month").agg({
        "cnt": "sum"
    }).reset_index()
    bymonth_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)
    
    return bymonth_df

def create_by_season_df(df):
    df['month'] = df['datetime'].dt.month
    conditions = [
        df['month'].isin([12, 1, 2]),  # Winter
        df['month'].isin([3, 4, 5]),   # Spring
        df['month'].isin([6, 7, 8]),   # Summer
        df['month'].isin([9, 10, 11])  # Fall
    ]
    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    df['season'] = pd.Series(pd.cut(df['month'], bins=[0, 3, 6, 9, 12], labels=seasons, ordered=False))

    byseason_df = df.groupby('season').agg({
        'cnt': 'sum'
    }).reset_index()

    return byseason_df

# Load data
bike_df = pd.read_csv("day.csv")
bike_df["datetime"] = pd.to_datetime(bike_df["dteday"])

# Filter data
min_date = bike_df["datetime"].min()
max_date = bike_df["datetime"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df["datetime"] >= str(start_date)) & 
                  (bike_df["datetime"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rentals_df = create_daily_rentals_df(main_df)
byweather_df = create_byweather_df(main_df)
bymonth_df = create_bymonth_df(main_df)
byseason_df = create_by_season_df(main_df)

# Dashboard header
st.header('Bike Sharing Dashboard 🚴')

# Pengaruh Cuaca
st.subheader('Pengaruh Cuaca Terhadap Penyewaan Sepeda')

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=main_df, x='temp', y='cnt', ax=ax, color='orange')
    ax.set_title("Pengaruh Suhu Terhadap Penyewaan")
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=main_df, x='hum', y='cnt', ax=ax, color='blue')
    ax.set_title("Pengaruh Kelembaban Terhadap Penyewaan")
    ax.set_xlabel("Kelembaban")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

# Kecepatan Angin
st.subheader('Pengaruh Kecepatan Angin Terhadap Penyewaan Sepeda')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_df, x='windspeed', y='cnt', ax=ax, color='green')
ax.set_title("Pengaruh Kecepatan Angin Terhadap Penyewaan")
ax.set_xlabel("Kecepatan Angin")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

# Perbedaan Hari Kerja dan Hari Libur
st.subheader('Perbandingan Penyewaan Sepeda di Hari Kerja dan Hari Libur')

main_df['weekday'] = main_df['datetime'].dt.dayofweek
main_df['is_weekend'] = main_df['weekday'] >= 5
weekend_df = main_df.groupby('is_weekend').agg({
    'cnt': 'sum'
}).reset_index()
weekend_df['label'] = weekend_df['is_weekend'].replace({True: 'Akhir Pekan', False: 'Hari Kerja'})

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='label', y='cnt', data=weekend_df, palette="Set2", ax=ax)
ax.set_title('Penyewaan Sepeda pada Hari Kerja vs Hari Libur')
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

# Pola Musiman
st.subheader('Pola Penyewaan Sepeda Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=byseason_df, palette="coolwarm", ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)
