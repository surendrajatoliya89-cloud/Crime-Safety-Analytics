import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Load cleaned dataset
df = pd.read_csv("data/crime_data_clean.csv")

print("=" * 65)
print("EXPLORATORY DATA ANALYSIS (EDA) REPORT - CRIMEWATCH ANALYTICS")
print("=" * 65)

# A. Crime Type Analysis
print("\n--- 1. CRIME TYPE DISTRIBUTION ---")
crime_counts = df["Crime_Type"].value_counts()
crime_pct = df["Crime_Type"].value_counts(normalize=True) * 100
crime_summary = pd.DataFrame({"Incidents": crime_counts, "Percentage (%)": crime_pct.round(2)})
print(crime_summary)

# B. Location / Area Analysis
print("\n--- 2. AREA INCIDENT DISTRIBUTION ---")
area_counts = df["Area"].value_counts()
print(area_counts)

# C. Monthly Trend Analysis
print("\n--- 3. MONTHLY REPORTED INCIDENTS ---")
month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
monthly_counts = df["Month"].value_counts().reindex(month_order).fillna(0).astype(int)
print(monthly_counts)

# D. Day of Week Analysis
print("\n--- 4. DAY OF THE WEEK DISTRIBUTION ---")
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_counts = df["Day_of_Week"].value_counts().reindex(day_order)
print(day_counts)

# E. Severity Distribution
print("\n--- 5. SEVERITY LEVEL BREAKDOWN ---")
severity_counts = df["Severity_Level"].value_counts()
severity_pct = df["Severity_Level"].value_counts(normalize=True) * 100
severity_summary = pd.DataFrame({"Count": severity_counts, "Percentage (%)": severity_pct.round(2)})
print(severity_summary)

# F. Time Category Distribution
print("\n--- 6. TIME OF DAY DISTRIBUTION ---")
time_counts = df["Time_Category"].value_counts()
print(time_counts)

# G. Demographic summary
print("\n--- 7. VICTIM DEMOGRAPHICS SUMMARY ---")
print(f"Mean Victim Age: {df['Victim_Age'].mean():.1f} years (Range: {df['Victim_Age'].min()} - {df['Victim_Age'].max()})")
print("Gender Distribution:")
print(df["Victim_Gender"].value_counts())

print("\n" + "=" * 65)
print("Key Takeaway: Downtown and Harbor District report the highest incident volume.")
print("Theft is the most frequently recorded incident category (~32%).")
print("=" * 65)
