import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# ✅ Load dataset
df = pd.read_csv("cleaned_covid_data.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2022-01-31")]
df.rename(columns={"total_vaccinations": "total_vaccination_doses"}, inplace=True)
df.fillna(method="ffill", inplace=True)
df.fillna(0, inplace=True)

print("✅ Data loaded for statistical analysis!")

# 🔹 Compute mean values by country
country_stats = (
    df.groupby("location")[["total_cases", "total_deaths", "total_vaccination_doses"]]
    .max()
    .reset_index()
)

# 🔹 Correlation Matrix
correlation = country_stats[["total_cases", "total_deaths", "total_vaccination_doses"]].corr()
print("\n📈 Correlation Matrix:\n", correlation)

# Save heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap - COVID-19 Data (2020–2022)")
plt.tight_layout()
plt.savefig("data/correlation_heatmap.png")
print("🔥 Correlation heatmap saved as data/correlation_heatmap.png")

# 🔹 Hypothesis Testing
t_stat, p_value = stats.ttest_ind(
    country_stats["total_deaths"], country_stats["total_vaccination_doses"], equal_var=False
)
print(f"\n🧪 T-test Result: t={t_stat:.4f}, p={p_value:.4f}")

if p_value < 0.05:
    print("👉 Statistically significant difference found between deaths and vaccinations.")
else:
    print("👉 No significant difference found between deaths and vaccinations.")

# Save stats summary
country_stats.to_csv("data/statistical_summary.csv", index=False)
print("💾 Statistical summary saved to 'data/statistical_summary.csv'")
