import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.set_page_config(page_title="COVID-19 Data Analysis", layout="wide")
st.title("🦠 COVID-19 Data Analysis Dashboard")

# Load cleaned data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_covid_data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
countries = df["Country/Region"].unique().tolist()
selected_country = st.sidebar.selectbox("Select Country", countries)

# Filter data
country_data = df[df["Country/Region"] == selected_country]

# Show data summary
st.subheader(f"📊 COVID-19 Trend for {selected_country}")
st.write(country_data.tail())

# Plot trends
fig, ax = plt.subplots(figsize=(10, 5))
if "Date" in country_data.columns and "Confirmed" in country_data.columns:
    ax.plot(country_data["Date"], country_data["Confirmed"], label="Confirmed", color="blue")
if "Deaths" in country_data.columns:
    ax.plot(country_data["Date"], country_data["Deaths"], label="Deaths", color="red")
if "Recovered" in country_data.columns:
    ax.plot(country_data["Date"], country_data["Recovered"], label="Recovered", color="green")

ax.set_xlabel("Date")
ax.set_ylabel("Cases")
ax.set_title(f"COVID-19 Trends in {selected_country}")
ax.legend()
st.pyplot(fig)

# Statistics section
st.subheader("📈 Key Statistics")
st.write(f"Total Confirmed Cases: {country_data['Confirmed'].sum():,}")
st.write(f"Total Deaths: {country_data['Deaths'].sum():,}")
st.write(f"Total Recovered: {country_data['Recovered'].sum():,}")
