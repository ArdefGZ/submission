import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import locale

sns.set(style='dark')
locale.setlocale(locale.LC_ALL, '')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_partikel_rata2_df(df):
    partikel_df = df[['PM2.5', 'PM10']].groupby(df['month']).agg({'PM2.5': ['mean', 'min', 'max'], 'PM10': ['mean', 'min', 'max']})
    partikel_df.columns = [f"{col[0]}_{col[1]}" for col in partikel_df.columns]
    return partikel_df

def create_gas_df(df):
    gas_df = df[['SO2', 'NO2', 'CO', 'O3']].groupby(df['month']).agg({'SO2': ['mean', 'min', 'max'], 'NO2': ['mean', 'min', 'max'], 'CO': ['mean', 'min', 'max'], 'O3': ['mean', 'min', 'max']})
    gas_df.columns = [f"{col[0]}_{col[1]}" for col in gas_df.columns]
    return gas_df

def create_gas_seasonal_df(df):
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    seasonal_df = create_gas_df(df).reset_index()
    seasonal_df['season'] = seasonal_df['month'].apply(get_season)
    seasonal_df = seasonal_df.groupby('season').agg({
        'SO2_mean': 'mean',
        'NO2_mean': 'mean',
        'CO_mean': 'mean',
        'O3_mean': 'mean'
    })
    return seasonal_df

def create_weather_df(df):
    def get_week(day):
        if day in range(1, 8):
            return 1
        elif day in range(8, 15):
            return 2
        elif day in range(15, 22):
            return 3
        elif day in range(22, 32):
            return 4

    weather_df = df[['TEMP', 'PRES', 'DEWP', 'WSPM', 'day']].copy()
    weather_df['week'] = weather_df['day'].apply(get_week)
    weather_df = weather_df.groupby('week').agg({
        'TEMP': ['mean', 'min', 'max'],
        'PRES': ['mean', 'min', 'max'],
        'DEWP': ['mean', 'min', 'max'],
        'WSPM': ['mean', 'min', 'max']
    })
    weather_df.columns = [f"{col[0]}_{col[1]}" for col in weather_df.columns]
    return weather_df




# Load Cleaned Data
df = pd.read_csv('PRSA_Data_20130301-20170228.csv')

with st.sidebar:
    # Menambahkan logo
    st.image('logo.png', width=50)
    
    years = [int(year) for year in df['year'].unique()]

    # Tampilkan selectbox dengan tahun-tahun yang sudah diformat tanpa koma
    year = st.selectbox('Pilih Tahun', years)
    
    station = st.selectbox('Pilih Station', df['station'].unique())
    
main_df = df[(df['year'] == year) & (df['station'] == station)]

# Create dataframe
daily_partikel_df = create_partikel_rata2_df(main_df)
daily_gas_df = create_gas_df(main_df)
seasonal_gas_df = create_gas_seasonal_df(main_df)
    
# Add header
st.title('Air Quality Data')
st.subheader('Partikel Polutan per Bulan')

st.subheader('Rata-rata Partikel per Bulan')
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    
    sns.lineplot(data=daily_partikel_df, x=daily_partikel_df.index, y='PM2.5_mean', marker='o', label='PM2.5')
    plt.title('Rata-rata PM2.5 per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata PM2.5')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    
    sns.lineplot(data=daily_partikel_df, x=daily_partikel_df.index, y='PM10_mean', marker='o', label='PM10')
    plt.title('Rata-rata PM10 per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata PM10')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()
    st.pyplot(fig)

st.subheader('Minimum Partikel per Bulan') 
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    
    sns.lineplot(data=daily_partikel_df, x=daily_partikel_df.index, y='PM2.5_min', marker='o', label='PM2.5')
    plt.title('Minimum PM2.5 per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Minimum PM2.5')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots()
    
    sns.lineplot(data=daily_partikel_df, x=daily_partikel_df.index, y='PM10_min', marker='o', label='PM10')
    plt.title('Minimum PM10 per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Minimum PM10')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()
    st.pyplot(fig)

st.subheader('Maximum Partikel per Bulan')
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    
    sns.lineplot(data=daily_partikel_df, x=daily_partikel_df.index, y='PM2.5_max', marker='o', label='PM2.5')
    plt.title('Maximum PM2.5 per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Maximum PM2.5')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots()
    
    sns.lineplot(data=daily_partikel_df, x=daily_partikel_df.index, y='PM10_max', marker='o', label='PM10')
    plt.title('Maximum PM10 per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Maximum PM10')
    plt.xticks(range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.show()
    st.pyplot(fig)
    
st.subheader('Gas Polutan yang Terukur')
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_so2 = daily_gas_df['SO2_mean'].mean()
    avg_so2_rounded = round(avg_so2, 2)
    st.metric('Rata-rata SO2', avg_so2_rounded)
    
with col2:
    avg_no2 = daily_gas_df['NO2_mean'].mean()
    avg_no2_rounded = round(avg_no2, 2)
    st.metric('Rata-rata NO2', avg_no2_rounded)
    
with col3:
    avg_co = daily_gas_df['CO_mean'].mean()
    avg_co_rounded = round(avg_co, 2)
    st.metric('Rata-rata CO', avg_co_rounded)
    
with col4:
    avg_o3 = daily_gas_df['O3_mean'].mean()
    avg_o3_rounded = round(avg_o3, 2)
    st.metric('Rata-rata O3', avg_o3_rounded)
    
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    
    sns.barplot(data=seasonal_gas_df, x=seasonal_gas_df.index, y='SO2_mean', palette='viridis')
    plt.title('Rata-rata SO2 per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata SO2')
    plt.show()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    
    sns.barplot(data=seasonal_gas_df, x=seasonal_gas_df.index, y='NO2_mean', palette='viridis')
    plt.title('Rata-rata NO2 per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata NO2')
    plt.show()
    st.pyplot(fig)
    
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    
    sns.barplot(data=seasonal_gas_df, x=seasonal_gas_df.index, y='CO_mean', palette='viridis')
    plt.title('Rata-rata CO per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata CO')
    plt.show()
    st.pyplot(fig)
    
with col2:
    fig, ax = plt.subplots()
    
    sns.barplot(data=seasonal_gas_df, x=seasonal_gas_df.index, y='O3_mean', palette='viridis')
    plt.title('Rata-rata O3 per Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-rata O3')
    plt.show()
    st.pyplot(fig)

months = [int(month) for month in main_df['month'].unique()]

# Tampilkan selectbox dengan bulan-bulan
month = st.selectbox('Pilih Bulan', months)

detail_df = main_df[main_df['month'] == month]

# Create a dataframe
daily_weather_df = create_weather_df(detail_df)

st.subheader(f'Data Detail Cuaca Bulan ke-{month}')


col1, col2 = st.columns(2)

with col1:
    # cek jika data tidak bernilai negatif
    if daily_weather_df['TEMP_min'].min() >= 0:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Piechart membandingkan rata-rata temperature dalam tiap minggu
        labels = [f'Week {i}\n({daily_weather_df["TEMP_mean"][i]:.2f}°C)' for i in range(1, 5)]
        sizes = daily_weather_df['TEMP_mean']
        explode = (0.1, 0, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Rata-Rata Temperature per Minggu')
        plt.show()
        st.pyplot(fig)
    else:
        st.error('Ada data temperature yang bernilai negatif')
    
with col2:
    if daily_weather_df['WSPM_min'].min() >= 0:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Piechart membandingkan rata-rata windspeed dalam tiap minggu
        labels = [f'Week {i}\n({daily_weather_df["WSPM_mean"][i]:.2f} m/s)' for i in range(1, 5)]
        sizes = daily_weather_df['WSPM_mean']
        explode = (0.1, 0, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Rata-Rata Windspeed per Minggu')
        plt.show()
        st.pyplot(fig)
    else:
        st.error('Ada data windspeed yang bernilai negatif')
    
col1, col2 = st.columns(2)

with col1:
    if daily_weather_df['PRES_min'].min() >= 0:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Piechart membandingkan rata-rata pressure dalam tiap minggu
        labels = [f'Week {i}\n({daily_weather_df["PRES_mean"][i]:.2f} hPa)' for i in range(1, 5)]
        sizes = daily_weather_df['PRES_mean']
        explode = (0.1, 0, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Rata-Rata Pressure per Minggu')
        plt.show()
        st.pyplot(fig)
    else:
        st.error('Ada data pressure yang bernilai negatif')

with col2:
    if daily_weather_df['DEWP_min'].min() >= 0:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Piechart membandingkan rata-rata dewpoint dalam tiap minggu
        labels = [f'Week {i}\n({daily_weather_df["DEWP_mean"][i]:.2f}°C)' for i in range(1, 5)]
        sizes = daily_weather_df['DEWP_mean']
        explode = (0.1, 0, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.title('Rata-Rata Dewpoint per Minggu')
        plt.show()
        st.pyplot(fig)
    else:
        st.error('Ada data dewpoint yang bernilai negatif')
        

    

# Add footer
st.markdown('---')
st.write('© 2024 - Made by Arya Dheffan S. - All rights reserved.')
