import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parents[2]
input_file = base_path / "data" / "QuickBite_Assessment.xlsx"

areas = pd.read_excel(input_file, sheet_name="areas")

print("========= AREAS DATA INSPECTION =========")

print("\nTotal Rows and Columns:")
print(areas.shape)

print("\nMissing Values Count:")
print(areas.isnull().sum())

print("\nTotal Missing Values:")
print(areas.isnull().sum().sum())

print("\nExact Duplicate Rows:")
print(areas.duplicated().sum())

print("\nDuplicate Area IDs:")
print(areas.duplicated(subset=["area_id"]).sum())

print("\nColumn Data Types:")
print(areas.dtypes)
