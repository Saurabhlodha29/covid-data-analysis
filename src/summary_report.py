import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("data/covid_data.csv")
print("✅ Data loaded for summary report!")

# Clean data
df = df.dropna(subset=["Confirmed", "Deaths", "Recovered"])

# Global statistics
summary = {
    "Total Confirmed": df["Confirmed"].sum(),
    "Total Deaths": df["Deaths"].sum(),
    "Total Recovered": df["Recovered"].sum(),
    "Mortality Rate (%)": (df["Deaths"].sum() / df["Confirmed"].sum()) * 100,
    "Recovery Rate (%)": (df["Recovered"].sum() / df["Confirmed"].sum()) * 100,
}

summary_df = pd.DataFrame([summary])
summary_df.to_csv("data/summary_report.csv", index=False)
print("\n📊 Summary report saved as data/summary_report.csv")

# Country-level summary
country_summary = df.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]].sum().reset_index()
country_summary.to_csv("data/country_summary.csv", index=False)
print("🌍 Country-level summary saved as data/country_summary.csv")


# Ranking by recovery and mortality rate
country_summary["Recovery Rate (%)"] = (country_summary["Recovered"] / country_summary["Confirmed"]) * 100
country_summary["Mortality Rate (%)"] = (country_summary["Deaths"] / country_summary["Confirmed"]) * 100

# Top 10 countries by recovery rate
top_recovery = country_summary.sort_values(by="Recovery Rate (%)", ascending=False).head(10)
top_recovery.to_csv("data/top10_recovery.csv", index=False)

# Top 10 countries by mortality rate
top_mortality = country_summary.sort_values(by="Mortality Rate (%)", ascending=False).head(10)
top_mortality.to_csv("data/top10_mortality.csv", index=False)

print("🏆 Top 10 recovery and mortality rate tables saved in data/")
