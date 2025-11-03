import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Load cleaned data
df = pd.read_csv("data/processed/cleaned_covid_data.csv")

print("✅ Data loaded for analysis!")

# --- 1️⃣ Global Summary ---
global_summary = df.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]].max().reset_index()
print("\n🌍 Global Summary:")
print(global_summary.head())

# --- 2️⃣ Correlation Analysis ---
if "Confirmed" in df.columns and "Deaths" in df.columns:
    corr, _ = pearsonr(df["Confirmed"], df["Deaths"])
    print(f"\n📊 Correlation between Confirmed and Deaths: {corr:.2f}")

if "Confirmed" in df.columns and "Recovered" in df.columns:
    corr, _ = pearsonr(df["Confirmed"], df["Recovered"])
    print(f"📊 Correlation between Confirmed and Recovered: {corr:.2f}")

# --- 3️⃣ Growth Rate Calculation ---
df["Confirmed_Shifted"] = df.groupby("Country/Region")["Confirmed"].shift(1)
df["GrowthRate"] = ((df["Confirmed"] - df["Confirmed_Shifted"]) / df["Confirmed_Shifted"]) * 100
df["GrowthRate"].fillna(0, inplace=True)

avg_growth = df.groupby("Country/Region")["GrowthRate"].mean().reset_index()
avg_growth.rename(columns={"GrowthRate": "AvgGrowthRate (%)"}, inplace=True)
print("\n📈 Average Growth Rate per Country:")
print(avg_growth.head())

# --- 4️⃣ Save insights for Streamlit ---
avg_growth.to_csv("data/processed/country_growth_insights.csv", index=False)
print("\n💾 Insights saved to 'country_growth_insights.csv'")
