import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/covid_data.csv")

print("✅ Data loaded for statistical analysis!")

# Group by country and calculate means
country_stats = df.groupby("Country/Region")[["Confirmed", "Deaths", "Recovered"]].mean().reset_index()

# Correlation matrix
correlation = country_stats.select_dtypes(include=[np.number]).corr()
print("\n📈 Correlation Matrix:\n", correlation)

# T-test example: Check if mean deaths differ significantly from mean recoveries
t_stat, p_value = stats.ttest_ind(country_stats["Deaths"], country_stats["Recovered"], equal_var=False)
print(f"\n🧪 T-test Result: t={t_stat:.4f}, p={p_value:.4f}")

if p_value < 0.05:
    print("👉 Statistically significant difference found.")
else:
    print("👉 No significant difference found.")

# Save statistical summary
country_stats.to_csv("data/statistical_summary.csv", index=False)
print("\n💾 Statistical summary saved to 'data/statistical_summary.csv'")


# Correlation heatmap
corr = df[["Confirmed", "Deaths", "Recovered"]].corr()

plt.figure(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap - COVID-19 Data")
plt.tight_layout()
plt.savefig("data/correlation_heatmap.png")
print("🔥 Correlation heatmap saved as data/correlation_heatmap.png")