import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parents[2]
input_file = base_path / "data" / "QuickBite_Assessment.xlsx"

delivery_partners = pd.read_excel(
    input_file,
    sheet_name="delivery_partners"
)

print("========== DELIVERY PARTNERS DATA INSPECTION ==========")

print("\nTotal Rows and Columns:")
print(delivery_partners.shape)

print("\nMissing Values Count:")
print(delivery_partners.isnull().sum())

print("\nTotal Missing Values:")
print(delivery_partners.isnull().sum().sum())

print("\nExact Duplicate Rows:")
print(delivery_partners.duplicated().sum())

print("\nDuplicate Partner IDs:")
print(delivery_partners.duplicated(subset=["partner_id"]).sum())

print("\nColumn Data Types:")
print(delivery_partners.dtypes)
