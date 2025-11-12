import pandas as pd
import numpy as np

print("🚀 Starting COVID-19 Data Cleaning and Processing...")

# ✅ Load raw OWID dataset
df = pd.read_csv("data/owid_covid_data.csv")

# ✅ Keep only important columns
cols_to_keep = [
    "location", "date", "total_cases", "total_deaths",
    "total_vaccinations", "population", "continent"
]
df = df[cols_to_keep]

# ✅ Parse dates
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ✅ Remove rows without valid date or location
df = df.dropna(subset=["date", "location"])

# ✅ Sort by country and date
df = df.sort_values(["location", "date"]).reset_index(drop=True)

# ✅ Handle missing cumulative values properly (ffill by country)
for col in ["total_cases", "total_deaths", "total_vaccinations"]:
    df[col] = df.groupby("location")[col].ffill().fillna(0)
    df[col] = df[col].clip(lower=0)  # Avoid negatives

# ✅ Handle population (constant per country)
df["population"] = (
    df.groupby("location")["population"]
    .ffill()
    .bfill()
    .fillna(df["population"].median())
)

# ✅ Fill missing continent values
df["continent"] = df["continent"].fillna("Unknown")

# ✅ Filter timeframe (2020–2022)
df = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2022-01-31")]

# ✅ Save cleaned dataset
df.to_csv("cleaned_covid_data.csv", index=False)
print("✅ Cleaned dataset saved as 'cleaned_covid_data.csv'")

# ✅ Preview sample
print(df.head(5))
print("\n✅ Data cleaning complete. Ready for analysis & dashboard!")
