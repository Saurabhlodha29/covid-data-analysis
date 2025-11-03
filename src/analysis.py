import pandas as pd

# Load your local dataset (make sure it's in the same folder)
df = pd.read_csv("covid_data.csv")

# Confirm dataset loaded
print("✅ Dataset loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Keep only useful columns if they exist
columns_to_keep = ['Date', 'Country/Region', 'Confirmed', 'Deaths', 'Recovered']
available_cols = [col for col in columns_to_keep if col in df.columns]
df = df[available_cols]

# Convert Date to datetime if present
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Group by Country and Date if applicable
if all(col in df.columns for col in ['Country/Region', 'Date']):
    df = df.groupby(['Country/Region', 'Date']).sum().reset_index()

# Display first few rows
print("\n🧾 Cleaned data preview:")
print(df.head())

# Save cleaned version
df.to_csv("cleaned_covid_data.csv", index=False)
print("\n💾 Cleaned data saved as 'cleaned_covid_data.csv'")
