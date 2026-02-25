# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ----------------------
# Header Dashboard
# ----------------------
st.markdown(
    "<h1 style='text-align: center; color: #2E8B57;'>Dashboard Penyewaan Sepeda 2011-2012 🚴</h1>",
    unsafe_allow_html=True
)

# ----------------------
# Load Data
# ----------------------
day_df = pd.read_csv("main_data_day.csv")
hour_df = pd.read_csv("main_data_hour.csv")

# Pastikan kolom datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# ----------------------
# Sidebar Filters
# ----------------------
st.sidebar.header("Filter Data")

# YEARS
years_options = sorted(day_df['yr'].dropna().unique())
years = st.sidebar.multiselect("Pilih Tahun:", options=years_options, default=years_options)

# MONTHS
months_options = sorted(day_df['mnth'].dropna().unique())
months = st.sidebar.multiselect("Pilih Bulan:", options=months_options, default=months_options)

# WEEKDAYS
weekdays_options = sorted(day_df['weekday'].dropna().unique())
weekdays = st.sidebar.multiselect("Pilih Hari:", options=weekdays_options, default=weekdays_options)

# HOURS (hanya hour_df)
hours_options = sorted(hour_df['hr'].dropna().unique())
hours = st.sidebar.multiselect("Pilih Jam:", options=hours_options, default=hours_options)

# APPLY FILTER
day_df = day_df[day_df['yr'].isin(years) & day_df['mnth'].isin(months) & day_df['weekday'].isin(weekdays)]
hour_df = hour_df[hour_df['yr'].isin(years) & hour_df['mnth'].isin(months) & hour_df['weekday'].isin(weekdays) & hour_df['hr'].isin(hours)]

# ----------------------
# Tabs
# ----------------------
tab1, tab2 = st.tabs(["Harian", "Per Jam"])

# ----------------------
# TAB 1: Harian (day_df)
# ----------------------
with tab1:
    st.header("Dashboard Harian")

    # Total & Rata-rata Penyewaan
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Penyewaan", int(day_df['cnt'].sum()))
    with col2:
        st.metric("Rata-rata Penyewaan", round(day_df['cnt'].mean(),2))

    # Rata-rata per Season
    st.subheader("Rata-rata Penyewaan per Season")
    season_avg = day_df.groupby('season')['cnt'].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=season_avg.index, y=season_avg.values, palette="viridis", ax=ax)
    ax.set_xlabel("Season (1=Winter,2=Spring,3=Summer,4=Fall)")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Rata-rata per Cuaca
    st.subheader("Rata-rata Penyewaan per Kondisi Cuaca")
    weather_avg = day_df[day_df['weathersit'].isin([1,2,3])].groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=weather_avg.index, y=weather_avg.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Weathersit (1=Clear,2=Mist,3=Light Snow/Rain)")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Rata-rata per Bulan
    st.subheader("Tren Penyewaan Sepeda Bulanan")
    month_avg = day_df.groupby('mnth')['cnt'].mean()
    fig, ax = plt.subplots()
    sns.lineplot(x=month_avg.index, y=month_avg.values, marker='o', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Rata-rata per Hari
    st.subheader("Rata-rata Penyewaan per Hari dalam Seminggu")
    weekday_avg = day_df.groupby('weekday')['cnt'].mean()
    weekday_labels = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    fig, ax = plt.subplots()
    sns.barplot(x=weekday_avg.index, y=weekday_avg.values, palette="magma", ax=ax)
    ax.set_xticks(range(7))
    ax.set_xticklabels(weekday_labels)
    ax.set_xlabel("Hari")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

# ----------------------
# TAB 2: Per Jam (hour_df)
# ----------------------
with tab2:
    st.header("Dashboard Per Jam")

    # Rata-rata per Jam
    st.subheader("Rata-rata Penyewaan per Jam")
    hr_avg = hour_df.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots()
    sns.lineplot(x=hr_avg.index, y=hr_avg.values, marker='o', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Hari Kerja vs Hari Libur
    st.subheader("Rata-rata Penyewaan per Jam: Hari Kerja vs Hari Libur")
    hour_workingday = hour_df.groupby(['hr','workingday'])['cnt'].mean().unstack()
    fig, ax = plt.subplots()
    hour_workingday.plot(kind='line', marker='o', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

st.caption("Dashboard Bike Sharing 2011-2012")