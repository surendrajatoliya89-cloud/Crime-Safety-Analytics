import pandas as pd
import os

raw_path = "data/crime_data.csv"
df = pd.read_csv(raw_path)
print(f"Initial raw record count: {len(df)}")

initial_duplicates = df.duplicated().sum()
df.drop_duplicates(subset=["Incident_ID"], keep="first", inplace=True)
print(f"Dropped {initial_duplicates} duplicate records. Current rows: {len(df)}")

weather_mode = df["Weather"].mode()[0]
df["Weather"] = df["Weather"].fillna(weather_mode)

loc_mode = df["Location_Type"].mode()[0]
df["Location_Type"] = df["Location_Type"].fillna(loc_mode)

age_median = df["Victim_Age"].median()
df["Victim_Age"] = df["Victim_Age"].fillna(age_median).astype(int)

df["Date"] = pd.to_datetime(df["Date"])

text_cols = ["State", "City", "Area", "Location_Type", "Crime_Type", "Crime_Category", 
             "Severity_Level", "Victim_Gender", "Weather", "Holiday", "Time_Category", "Crime_Risk_Level"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

remaining_nulls = df.isnull().sum().sum()
print(f"Remaining null values across entire dataset: {remaining_nulls}")

clean_path = "data/crime_data_clean.csv"
df.to_csv(clean_path, index=False)
print(f"Cleaned dataset saved successfully to '{clean_path}' ({len(df)} rows, {len(df.columns)} columns).")
