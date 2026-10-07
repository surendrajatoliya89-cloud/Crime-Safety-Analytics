import pandas as pd

# Load dataset
df = pd.read_csv("data/crime_data.csv")

print("=" * 60)
print("1. DATASET SHAPE (Rows, Columns):")
print(df.shape)

print("\n" + "=" * 60)
print("2. FIRST 5 ROWS:")
print(df.head())

print("\n" + "=" * 60)
print("3. DATA TYPES & NON-NULL COUNTS (df.info()):")
df.info()

print("\n" + "=" * 60)
print("4. MISSING VALUES CHECK (df.isnull().sum()):")
missing = df.isnull().sum()
print(missing[missing > 0])

print("\n" + "=" * 60)
print("5. DUPLICATE RECORDS CHECK (df.duplicated().sum()):")
print(f"Total duplicate rows: {df.duplicated().sum()}")

print("\n" + "=" * 60)
print("6. NUMERICAL FEATURES SUMMARY (df.describe()):")
print(df.describe())
print("=" * 60)
