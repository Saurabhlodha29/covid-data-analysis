import pandas as pd
import matplotlib.pyplot as plt

# ✅ Load cleaned dataset
df = pd.read_csv("cleaned_covid_data.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ✅ Filter up to Jan 2022
df = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2022-01-31")]

# ✅ Fill missing continent names logically
df["continent"] = df["continent"].fillna("Other")
df["continent"] = df["continent"].replace({
    "Oceania": "Australia & Pacific",
    "": "Other",
    "Unknown": "Other"
})
df = df[df["continent"] != "Other"]

# =============================
# 🌍 1. TOP 10 COUNTRIES BY TOTAL CASES
# =============================
top_cases = (
    df.groupby("location")["total_cases"]
    .max()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

plt.figure(figsize=(10, 6))
bars = plt.barh(
    top_cases["location"],
    top_cases["total_cases"] / 1_000_000,  # Convert to millions
    color="dodgerblue",
    edgecolor="black"
)
plt.title("Top 10 Countries by Total COVID-19 Cases (in Millions)", fontsize=14, fontweight="bold")
plt.xlabel("Total Confirmed Cases (Millions)", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.gca().invert_yaxis()  # Highest at top
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("data/top10_confirmed.png")
print("🌍 Top 10 Total Cases chart saved as data/top10_confirmed.png")

# =============================
# 💀 2. TOP 10 COUNTRIES BY MORTALITY RATE
# =============================
mortality = (
    df.groupby("location")[["total_deaths", "total_cases"]]
    .max()
    .reset_index()
)
mortality["Mortality Rate (%)"] = (mortality["total_deaths"] / mortality["total_cases"]) * 100
mortality = mortality.replace([float("inf"), -float("inf")], 0).fillna(0)
top_mortality = mortality.sort_values("Mortality Rate (%)", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(
    top_mortality["location"],
    top_mortality["Mortality Rate (%)"],
    color="firebrick",
    edgecolor="black"
)
plt.title("Top 10 Countries by Mortality Rate (%)", fontsize=14, fontweight="bold")
plt.xlabel("Mortality Rate (%)", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("data/top10_mortality_rate.png")
print("💀 Mortality Rate chart saved as data/top10_mortality_rate.png")

# =============================
# 💉 3. TOP 10 COUNTRIES BY VACCINATION RATE
# =============================
vaccination = (
    df.groupby("location")[["total_vaccinations", "population"]]
    .max()
    .reset_index()
)
vaccination["Vaccination Rate (%)"] = (vaccination["total_vaccinations"] / vaccination["population"]) * 100
vaccination = vaccination.replace([float("inf"), -float("inf")], 0).fillna(0)
top_vaccination = vaccination.sort_values("Vaccination Rate (%)", ascending=False).head(10)

plt.figure(figsize=(10, 6))
plt.barh(
    top_vaccination["location"],
    top_vaccination["Vaccination Rate (%)"],
    color="mediumseagreen",
    edgecolor="black"
)
plt.title("Top 10 Countries by Vaccination Rate (%)", fontsize=14, fontweight="bold")
plt.xlabel("Vaccination Rate (% of Population)", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.gca().invert_yaxis()
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("data/top10_vaccination_rate.png")
print("💉 Vaccination Rate chart saved as data/top10_vaccination_rate.png")

# =============================
# 🌎 4. CONTINENT-WISE VACCINATION RATE
# =============================
continent_vaccination = (
    df.groupby("continent")[["total_vaccinations", "population"]]
    .max()
    .reset_index()
)
continent_vaccination["Vaccination Rate (%)"] = (
    continent_vaccination["total_vaccinations"] / continent_vaccination["population"]
) * 100
continent_vaccination = continent_vaccination.replace([float("inf"), -float("inf")], 0).fillna(0)

plt.figure(figsize=(10, 6))
plt.bar(
    continent_vaccination["continent"],
    continent_vaccination["Vaccination Rate (%)"],
    color="skyblue",
    edgecolor="black"
)
plt.title("Continent-wise COVID-19 Vaccination Rates (2020–2022)", fontsize=14, fontweight="bold")
plt.xlabel("Continent", fontsize=12)
plt.ylabel("Vaccination Rate (%)", fontsize=12)
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("data/continent_vaccination_rate.png")
print("🌎 Continent-wise vaccination chart saved as data/continent_vaccination_rate.png")
