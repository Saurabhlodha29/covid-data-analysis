import os
import subprocess

print("🚀 Starting COVID-19 Data Analysis Pipeline...\n")

# Step 1: Data Cleaning & Basic Analysis
print("🔹 Running analysis.py...")
subprocess.run(["python", "src/analysis.py"])

# Step 2: Statistical Analysis
print("\n🔹 Running statistical_analysis.py...")
subprocess.run(["python", "src/statistical_analysis.py"])

# Step 3: Summary Reports
print("\n🔹 Running summary_report.py...")
subprocess.run(["python", "src/summary_report.py"])

# Step 4: Visualizations
print("\n🔹 Running visualization.py...")
subprocess.run(["python", "src/visualization.py"])

print("\n✅ All scripts executed successfully!")
