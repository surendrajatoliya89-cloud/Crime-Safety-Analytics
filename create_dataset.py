import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for exact academic reproducibility
np.random.seed(42)
random.seed(42)

TOTAL_RECORDS = 2400

# Geographic Hierarchy: State -> City -> Areas
geo_hierarchy = {
    "Maharashtra": {
        "Mumbai": ["Colaba", "Bandra", "Andheri", "Fort Downtown", "Harbor Docklands", "Dadar"],
        "Pune": ["Shivaji Nagar", "Kothrud", "Hinjewadi IT Park", "Viman Nagar", "Camp Cantonment", "Baner"]
    },
    "Delhi (NCT)": {
        "Delhi": ["Connaught Place", "South Delhi", "Old Delhi", "Dwarka", "Rohini", "Karol Bagh"]
    },
    "Karnataka": {
        "Bengaluru": ["Koramangala", "Indiranagar", "Whitefield", "MG Road Central", "Electronic City", "Jayanagar"]
    },
    "Telangana": {
        "Hyderabad": ["Banjara Hills", "Hitec City", "Charminar Heritage", "Gachibowli", "Secunderabad", "Madhapur"]
    },
    "West Bengal": {
        "Kolkata": ["Park Street", "Salt Lake", "Howrah", "New Town", "Ballygunge", "Esplanade"]
    },
    "Tamil Nadu": {
        "Chennai": ["T. Nagar", "Adyar", "Anna Nagar", "Marina Beachfront", "Velachery", "Guindy"]
    },
    "Gujarat": {
        "Ahmedabad": ["Navrangpura", "Satellite", "Maninagar", "SG Highway", "Sabarmati", "Paldi"]
    }
}

states = list(geo_hierarchy.keys())

location_types = [
    "Street", "Residential", "Commercial Market", "Public Park", "Transit Station", "Parking Complex"
]

# Realistic crime types with categories and severity levels
crime_catalog = {
    "Theft": {"category": "Property Crime", "severity": "Low", "weight": 0.28},
    "Vehicle Theft": {"category": "Property Crime", "severity": "Medium", "weight": 0.18},
    "Cyber Fraud": {"category": "Financial Crime", "severity": "Low", "weight": 0.16},
    "Burglary": {"category": "Property Crime", "severity": "Medium", "weight": 0.14},
    "Vandalism": {"category": "Public Order", "severity": "Low", "weight": 0.10},
    "Robbery": {"category": "Violent Crime", "severity": "Medium", "weight": 0.08},
    "Assault": {"category": "Violent Crime", "severity": "High", "weight": 0.06}
}

crime_types = list(crime_catalog.keys())
crime_weights = [crime_catalog[c]["weight"] for c in crime_types]

time_categories = ["Morning", "Afternoon", "Evening", "Night"]
time_weights = [0.18, 0.27, 0.33, 0.22]

weather_conditions = ["Clear", "Rainy", "Cloudy", "Foggy"]
weather_weights = [0.55, 0.25, 0.15, 0.05]

genders = ["Male", "Female", "Other"]
gender_weights = [0.49, 0.48, 0.03]

years = [2021, 2022, 2023, 2024]
year_weights = [0.20, 0.24, 0.28, 0.28] # Showing realistic historical volume progression

data = []

higher_risk_areas = {
    "Fort Downtown", "Harbor Docklands", "Old Delhi", "Connaught Place", 
    "Howrah", "Esplanade", "Charminar Heritage", "Camp Cantonment", "T. Nagar", "Navrangpura"
}

for i in range(1, TOTAL_RECORDS + 1):
    chosen_year = random.choices(years, weights=year_weights)[0]
    inc_id = f"INC-{chosen_year}-{i:04d}"
    
    start_of_year = datetime(chosen_year, 1, 1)
    is_leap = (chosen_year % 4 == 0 and (chosen_year % 100 != 0 or chosen_year % 400 == 0))
    day_count = 366 if is_leap else 365
    dt = start_of_year + timedelta(days=random.randint(0, day_count - 1))
    
    month_name = dt.strftime("%B")
    day_name = dt.strftime("%A")
    
    state = random.choice(states)
    city = random.choice(list(geo_hierarchy[state].keys()))
    area = random.choice(geo_hierarchy[state][city])
    
    loc_type = random.choice(location_types)
    
    # Realistic trend: Cyber Fraud increased in tech hubs (Bengaluru, Hyderabad) in recent years
    if city in ["Bengaluru", "Hyderabad"] and chosen_year in [2023, 2024] and random.random() < 0.25:
        c_type = "Cyber Fraud"
    else:
        c_type = random.choices(crime_types, weights=crime_weights)[0]
        
    category = crime_catalog[c_type]["category"]
    severity = crime_catalog[c_type]["severity"]
    
    time_cat = random.choices(time_categories, weights=time_weights)[0]
    weather = random.choices(weather_conditions, weights=weather_weights)[0]
    
    is_holiday = "Yes" if (dt.month == 1 and dt.day == 26) or (dt.month == 8 and dt.day == 15) or (dt.month == 10 and dt.day == 2) or random.random() < 0.04 else "No"
    
    if area in higher_risk_areas:
        prev_incidents = int(np.clip(np.random.poisson(lam=7), 1, 15))
    else:
        prev_incidents = int(np.clip(np.random.poisson(lam=3), 0, 10))
        
    v_age = int(np.clip(np.random.normal(loc=34, scale=11), 18, 75))
    v_gender = random.choices(genders, weights=gender_weights)[0]
    
    # Calculate contextual risk level without target leakage
    risk_score = 0
    if state in ["Delhi (NCT)", "Maharashtra"]:
        risk_score += 0.5
    if area in higher_risk_areas:
        risk_score += 2.0
    if time_cat in ["Evening", "Night"]:
        risk_score += 1.5
    if loc_type in ["Transit Station", "Parking Complex", "Commercial Market"]:
        risk_score += 1.0
    if prev_incidents >= 6:
        risk_score += 2.0
    elif prev_incidents >= 3:
        risk_score += 1.0
    if is_holiday == "Yes":
        risk_score += 0.5
        
    risk_score += random.uniform(-0.5, 0.5)
    
    if risk_score >= 4.5:
        risk_level = "High"
    elif risk_score >= 2.5:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    data.append({
        "Incident_ID": inc_id,
        "Date": dt.strftime("%Y-%m-%d"),
        "Year": chosen_year,
        "Month": month_name,
        "Day_of_Week": day_name,
        "Time_Category": time_cat,
        "State": state,
        "City": city,
        "Area": area,
        "Location_Type": loc_type,
        "Crime_Type": c_type,
        "Crime_Category": category,
        "Severity_Level": severity,
        "Victim_Age": v_age,
        "Victim_Gender": v_gender,
        "Weather": weather,
        "Holiday": is_holiday,
        "Previous_Incidents": prev_incidents,
        "Crime_Risk_Level": risk_level
    })

df = pd.DataFrame(data)

# Sort chronologically by date
df = df.sort_values(by="Date", ascending=False).reset_index(drop=True)

# Realistic missing values for data cleaning demonstration
missing_indices = random.sample(range(TOTAL_RECORDS), 6)
df.loc[missing_indices[:2], "Weather"] = np.nan
df.loc[missing_indices[2:4], "Location_Type"] = np.nan
df.loc[missing_indices[4:], "Victim_Age"] = np.nan

# Duplicate rows for deduplication
duplicates = df.iloc[:3].copy()
df = pd.concat([df, duplicates], ignore_index=True)

os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "crime_data.csv")
df.to_csv(output_path, index=False)

print(f"Multi-Year Dataset generated at {output_path} with {len(df)} rows across {len(years)} years (2021-2024):")
print("\nIncidents by Year:")
print(df["Year"].value_counts().sort_index())
print("\nIncidents by State:")
print(df["State"].value_counts())
print("\nIncidents by Crime Type:")
print(df["Crime_Type"].value_counts())
