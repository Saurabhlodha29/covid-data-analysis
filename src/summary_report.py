import pandas as pd

#  Load cleaned dataset
df = pd.read_csv("data/cleaned_covid_data.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df[df["date"] <= "2022-01-31"]
df = df.fillna(0)

print("✅ Data loaded for summary report!")

#  Aggregate per country (max cumulative values)
latest_global = (
    df.groupby("location")[["total_cases", "total_deaths", "total_vaccinations", "population"]]
    .max()
    .reset_index()
)

#  Compute global totals
summary = {
    "Total Cases": int(latest_global["total_cases"].sum()),
    "Total Deaths": int(latest_global["total_deaths"].sum()),
    "Total Vaccination Doses": int(latest_global["total_vaccinations"].sum()),
    "Mortality Rate (%)": round((latest_global["total_deaths"].sum() / latest_global["total_cases"].sum()) * 100, 2),
    "Vaccination Rate (%)": round((latest_global["total_vaccinations"].sum() / latest_global["population"].sum()) * 100, 2)
}

#  Save global summary
pd.DataFrame([summary]).to_csv("data/summary_report.csv", index=False)
print("📊 Summary report saved as data/summary_report.csv")

#  Save country-level summary
country_summary = latest_global.copy()
country_summary["Mortality Rate (%)"] = round((country_summary["total_deaths"] / country_summary["total_cases"]) * 100, 2)
country_summary["Vaccination Rate (%)"] = round((country_summary["total_vaccinations"] / country_summary["population"]) * 100, 2)
country_summary.to_csv("data/country_summary.csv", index=False)
print("🌍 Country-level summary saved as data/country_summary.csv")

print("✅ Summary report generation complete!")
