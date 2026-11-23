
import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parents[2]
input_file = base_path / "data" / "QuickBite_Assessment.xlsx"

customers = pd.read_excel(input_file, sheet_name="customers")

print("========== CUSTOMERS DATA INSPECTION ==========")

print("\nTotal Rows and Columns:")
print(customers.shape)

print("\nMissing Values Count:")
print(customers.isnull().sum())

print("\nTotal Missing Values:")
print(customers.isnull().sum().sum())

print("\nExact Duplicate Rows:")
print(customers.duplicated().sum())

print("\nDuplicate Customer IDs:")
print(customers.duplicated(subset=["customer_id"]).sum())

print("\nColumn Data Types:")
print(customers.dtypes)
