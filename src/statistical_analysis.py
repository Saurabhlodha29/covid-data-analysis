import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

#  Load dataset
df = pd.read_csv("cleaned_covid_data.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Use only 2020–2022 data
df = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2022-01-31")]

# Rename vaccination column
df.rename(columns={"total_vaccinations": "total_vaccination_doses"}, inplace=True)

# Handle missing values using forward-fill, then fill remaining gaps
df.fillna(method="ffill", inplace=True)
df.fillna(0, inplace=True)

print("✅ Data loaded for statistical analysis!")

# ===============================
# 🔹 Compute country-level stats
# ===============================
country_stats = (
    df.groupby("location")[["total_cases", "total_deaths", "total_vaccination_doses", "population"]]
    .max()
    .reset_index()
)

# Add derived metrics
country_stats["Mortality Rate (%)"] = (
    country_stats["total_deaths"] / country_stats["total_cases"]
) * 100

country_stats["Vaccination Rate (%)"] = (
    country_stats["total_vaccination_doses"] / country_stats["population"]
) * 100

# Replace inf or NaN
country_stats = country_stats.replace([float("inf"), -float("inf")], 0).fillna(0)

# ===============================
# 🔹 Correlation Matrix (Enhanced)
# ===============================
corr_data = country_stats[
    ["total_cases", "total_deaths", "total_vaccination_doses", "Mortality Rate (%)", "Vaccination Rate (%)"]
]

correlation = corr_data.corr()
print("\n📈 Correlation Matrix:\n", correlation)

# Save enhanced heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Enhanced Correlation Heatmap (Cases, Deaths, Vaccinations, Rates)")
plt.tight_layout()
plt.savefig("data/correlation_heatmap.png")
print("🔥 Enhanced correlation heatmap saved as data/correlation_heatmap.png")

# ===============================
# 🔹 Hypothesis Testing (T-test)
# ===============================
t_stat, p_value = stats.ttest_ind(
    country_stats["total_deaths"],
    country_stats["total_vaccination_doses"],
    equal_var=False
)

print(f"\n🧪 T-test Result: t={t_stat:.4f}, p={p_value:.4f}")

if p_value < 0.05:
    print("👉 Significant difference found between deaths and vaccinations.")
else:
    print("👉 No significant difference found between deaths and vaccinations.")

# ===============================
# 🔹 Save statistical summary
# ===============================
country_stats.to_csv("data/statistical_summary.csv", index=False)
print("💾 Statistical summary saved to 'data/statistical_summary.csv'")
