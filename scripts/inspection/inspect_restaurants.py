import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parents[2]
input_file = base_path / "data" / "QuickBite_Assessment.xlsx"

restaurants = pd.read_excel(input_file, sheet_name="restaurants")

print("========== RESTAURANTS DATA INSPECTION ==========")

print("\nTotal Rows and Columns:")
print(restaurants.shape)

print("\nMissing Values Count:")
print(restaurants.isnull().sum())

print("\nTotal Missing Values:")
print(restaurants.isnull().sum().sum())

print("\nExact Duplicate Rows:")
print(restaurants.duplicated().sum())

print("\nDuplicate Restaurant IDs:")
print(restaurants.duplicated(subset=["restaurant_id"]).sum())

print("\nColumn Data Types:")
print(restaurants.dtypes)
