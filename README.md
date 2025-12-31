# COVID-19 Data Analysis & Processing Pipeline

This project implements an end-to-end data analysis pipeline in Python to process, analyze, and visualize global COVID-19 data spanning 2020–2022.  
The goal is to extract meaningful trends and relationships between confirmed cases, deaths, and vaccination progress across countries and continents.

---

## Dataset
- Source: Our World in Data (OWID) COVID-19 Dataset
- Time range analyzed: January 2020 – January 2022
- Data is cleaned and standardized before analysis to handle missing values and inconsistencies.

---

## Project Structure
DS_PROJECT/
├── data/
│ └── cleaned_covid_data.csv
├── src/
│ ├── analysis.py # Data cleaning and preprocessing
│ ├── statistical_analysis.py # Correlation analysis and statistical tests
│ ├── visualization.py # Static and interactive visualizations
│ ├── summary_report.py # Aggregated country-level summaries
│ └── dashboard.py # Streamlit-based interactive dashboard
├── README.md
└── requirements.txt

---

## Pipeline Overview
1. **Data Cleaning & Preprocessing**
   - Filter relevant columns and time range
   - Handle missing and invalid values
   - Standardize cumulative metrics by country

2. **Exploratory & Statistical Analysis**
   - Compute mortality and vaccination-related metrics
   - Perform correlation analysis and hypothesis testing

3. **Visualization**
   - Generate country- and continent-level comparisons
   - Create charts to highlight trends and patterns

4. **Interactive Dashboard**
   - Explore data using filters and visual components via Streamlit

---

## Tech Stack
- Python
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- SciPy
- Streamlit

---

## How to Run
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
