import sqlite3
import pandas as pd
import os

csv_path = "data/crime_data_clean.csv"
df = pd.read_csv(csv_path)

os.makedirs("database", exist_ok=True)
sqlite_db_path = "database/crime_analytics.db"

conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS crime_records (
    Incident_ID TEXT PRIMARY KEY,
    Date TEXT NOT NULL,
    Year INTEGER NOT NULL,
    Month TEXT NOT NULL,
    Day_of_Week TEXT NOT NULL,
    Time_Category TEXT NOT NULL,
    State TEXT NOT NULL,
    City TEXT NOT NULL,
    Area TEXT NOT NULL,
    Location_Type TEXT NOT NULL,
    Crime_Type TEXT NOT NULL,
    Crime_Category TEXT NOT NULL,
    Severity_Level TEXT NOT NULL,
    Victim_Age INTEGER,
    Victim_Gender TEXT,
    Weather TEXT,
    Holiday TEXT,
    Previous_Incidents INTEGER DEFAULT 0,
    Crime_Risk_Level TEXT NOT NULL
)
''')

df.to_sql("crime_records", conn, if_exists="replace", index=False)
conn.commit()

cursor.execute("SELECT COUNT(*) FROM crime_records")
count = cursor.fetchone()[0]
print(f"Successfully loaded {count} multi-year records into SQLite database at '{sqlite_db_path}'.")

print("\nIncident count by Year:")
cursor.execute("SELECT Year, COUNT(*) as count FROM crime_records GROUP BY Year ORDER BY Year ASC")
for row in cursor.fetchall():
    print(f"  Year {row[0]}: {row[1]} incidents")

conn.close()
