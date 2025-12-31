import os
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_covid_data.csv")


# 🎨 PAGE CONFIGURATION
st.set_page_config(
    page_title="COVID-19 Data Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 💠 MODERN STYLING
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-header {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(90deg, #00c4ff, #00ffaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        text-align: center;
        font-size: 18px;
        color: #cfd8dc;
        margin-bottom: 30px;
    }
    section[data-testid="stSidebar"] {
        background-color: #11151c !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🧾 HEADER
st.markdown("<div class='main-header'>🦠 COVID-19 DATA ANALYSIS DASHBOARD</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Comprehensive Global COVID-19 Insights (2020–2022)</div>", unsafe_allow_html=True)

# 📂 LOAD DATA
try:
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2022-01-31")]
    df.rename(columns={"total_vaccinations": "total_vaccination_doses"}, inplace=True)
except FileNotFoundError:
    st.error("❌ 'cleaned_covid_data.csv' not found. Please run main.py first.")
    st.stop()

# 📊 SIDEBAR NAVIGATION
st.sidebar.title("📋 Menu")
page = st.sidebar.radio(
    "Go to:",
    ["Country Overview", "Visualizations", "Summary Reports"]
)

# 🔹 1. COUNTRY OVERVIEW
if page == "Country Overview":
    st.header("🌍 Country-Wise COVID-19 Analysis")

    countries = sorted(df["location"].unique())
    selected_country = st.sidebar.selectbox("Select Country", countries)
    country_data = df[df["location"] == selected_country].copy()

    time_filter = st.sidebar.radio("View Data By:", ["Day-wise", "Month-wise", "Year-wise"])

    if time_filter == "Day-wise":
        grouped = country_data.groupby("date")[["total_cases", "total_deaths", "total_vaccination_doses"]].max().reset_index()
    elif time_filter == "Month-wise":
        grouped = country_data.groupby(pd.Grouper(key="date", freq="M"))[["total_cases", "total_deaths", "total_vaccination_doses"]].last().reset_index()
        grouped["date"] = grouped["date"].dt.strftime("%b %Y")
    else:
        grouped = country_data.groupby(pd.Grouper(key="date", freq="Y"))[["total_cases", "total_deaths", "total_vaccination_doses"]].last().reset_index()
        grouped["date"] = grouped["date"].dt.strftime("%Y")

    grouped = grouped.fillna(0)

    latest = grouped.iloc[-1]
    col1, col2, col3 = st.columns(3)
    col1.metric("📈 Total Cases", f"{int(latest['total_cases']):,}")
    col2.metric("💀 Total Deaths", f"{int(latest['total_deaths']):,}")
    col3.metric("💉 Total Vaccination Doses", f"{int(latest['total_vaccination_doses']):,}")

    st.subheader(f"📊 COVID-19 Data for {selected_country}")
    st.dataframe(grouped)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=grouped["date"], y=grouped["total_cases"], mode="lines", name="Total Cases", line=dict(color="cyan", width=2)))
    fig.add_trace(go.Scatter(x=grouped["date"], y=grouped["total_deaths"], mode="lines", name="Total Deaths", line=dict(color="red", width=2)))
    fig.add_trace(go.Scatter(x=grouped["date"], y=grouped["total_vaccination_doses"], mode="lines", name="Total Vaccination Doses", line=dict(color="lime", width=2)))

    fig.update_layout(
        template="plotly_dark",
        title=f"COVID-19 Trend for {selected_country} ({time_filter})",
        xaxis_title="Date",
        yaxis_title="Number of Cases / Deaths / Doses",
        hovermode="x unified",
        height=550
    )
    st.plotly_chart(fig, use_container_width=True)

# 🔹 2. VISUALIZATION DASHBOARD
elif page == "Visualizations":
    st.header("📊 Visualization Dashboard")
    st.markdown("<p style='font-size:20px; color:#cccccc;'>Explore key insights and patterns observed from global COVID-19 data. Each visualization includes labeled axes for clarity and ease of understanding.</p>", unsafe_allow_html=True)

    charts = {
        "🌍 Top 10 Total Cases": {
            "path": "data/top10_confirmed.png",
            "desc": "Shows the 10 countries with the highest total COVID-19 cases. **X-axis**: Total cases (log scale). **Y-axis**: Countries."
        },
        "💀 Top 10 Mortality Rate": {
            "path": "data/top10_mortality_rate.png",
            "desc": "Displays the 10 countries with the highest mortality rate (%). **X-axis**: Death rate percentage. **Y-axis**: Countries."
        },
        "💉 Top 10 Vaccination Rate": {
            "path": "data/top10_vaccination_rate.png",
            "desc": "Represents top 10 countries by vaccination rate (%). **X-axis**: Vaccination rate (% of population). **Y-axis**: Countries."
        },
        "📈 Global Trend (Cases, Deaths, Vaccinations)": {
            "path": "data/global_trend.png",
            "desc": "Line chart showing worldwide trends. **X-axis**: Date (2020–2022). **Y-axis**: Cumulative counts of cases, deaths, and vaccine doses."
        },
        "🔥 Correlation Heatmap": {
            "path": "data/correlation_heatmap.png",
            "desc": "Heatmap of correlations among metrics. Darker colors = stronger correlation. High correlation between cases and deaths is evident (~0.95)."
        },
        "🌎 Continent-Wise Vaccination Rate": {
            "path": "data/continent_vaccination_rate.png",
            "desc": "Compares average vaccination rates by continent. **X-axis**: Continents. **Y-axis**: Average vaccination rate (%)."
        }
    }

    for title, info in charts.items():
        st.subheader(title)
        try:
            img = Image.open(info["path"])
            st.image(img, use_container_width=True)
            st.markdown(f"<p style='color:#a0a0a0; font-size:16px;'>{info['desc']}</p>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning(f"⚠️ {info['path']} not found. Run visualization.py first.")

# 🔹 3. SUMMARY REPORTS
elif page == "Summary Reports":
    st.header("📄 Summary Reports")
    st.markdown("<p style='font-size:20px; color:#cccccc;'>Global and country-level summaries derived from processed data.</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📑 Show Summary Report Table"):
            try:
                summary = pd.read_csv("data/summary_report.csv")
                st.dataframe(summary)
            except:
                st.warning("⚠️ summary_report.csv not found.")
    with col2:
        if st.button("🌍 Show Country-Level Summary"):
            try:
                country_summary = pd.read_csv("data/country_summary.csv")
                st.dataframe(country_summary)
                st.success(f"✅ Showing all {len(country_summary)} countries")
            except:
                st.warning("⚠️ country_summary.csv not found.")

# 🌟 FOOTER
st.markdown("""
<hr>
<p style='text-align:center; color:#00b4db;'>
Developed with ❤️ by Team COVID-19 Analysis | Powered by Streamlit
</p>
""", unsafe_allow_html=True)
