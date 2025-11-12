import pandas as pd

# Load the OWID dataset
df = pd.read_csv("data/owid_covid_data.csv")

print("✅ OWID dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist()[:10], "...")

# Keep only relevant columns
df = df[[
    "location", "date", "total_cases", "new_cases",
    "total_deaths", "new_deaths", "total_vaccinations",
    "population"
]]

# Remove global or non-country rows
exclude = ["World", "European Union", "International"]
df = df[~df["location"].isin(exclude)]

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Handle missing values
df.fillna(0, inplace=True)

# Save cleaned dataset for dashboard
df.to_csv("cleaned_covid_data.csv", index=False)
print("\n💾 Cleaned OWID dataset saved as 'cleaned_covid_data.csv'")
