import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/country_summary.csv")
print("✅ Data loaded for visualization!")

# Sort countries by confirmed cases
top_countries = df.sort_values(by="Confirmed", ascending=False).head(10)

# --- Bar Chart: Top 10 Countries by Confirmed Cases ---
plt.figure(figsize=(10,6))
plt.bar(top_countries["Country/Region"], top_countries["Confirmed"], color='skyblue')
plt.title("Top 10 Countries by Confirmed COVID-19 Cases")
plt.xlabel("Country")
plt.ylabel("Confirmed Cases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/top10_confirmed.png")
plt.close()

# --- Line Chart: Deaths vs Recovered for Top 10 Countries ---
plt.figure(figsize=(10,6))
plt.plot(top_countries["Country/Region"], top_countries["Deaths"], label="Deaths", marker='o')
plt.plot(top_countries["Country/Region"], top_countries["Recovered"], label="Recovered", marker='o')
plt.title("Deaths vs Recovered (Top 10 Countries)")
plt.xlabel("Country")
plt.ylabel("Count")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/deaths_vs_recovered.png")
plt.close()

print("📊 Charts saved: data/top10_confirmed.png & data/deaths_vs_recovered.png")
