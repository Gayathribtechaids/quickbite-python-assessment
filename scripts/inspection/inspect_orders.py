
import pandas as pd
from pathlib import Path

# Project folder path
base_path = Path(__file__).resolve().parents[2]

input_file = base_path / "data" / "QuickBite_Assessment.xlsx"

orders = pd.read_excel(input_file, sheet_name="orders")

print("========== ORDERS DATA INSPECTION ==========")

#  Dataset Overview
print("\nTotal Rows and Columns:")
print(orders.shape)

#  Missing Values Count
print("\nMissing Values Count:")
print(orders.isnull().sum())

print("\nTotal Missing Values:")
print(orders.isnull().sum().sum())

#  Duplicate Rows Count
print("\nExact Duplicate Rows:")
print(orders.duplicated().sum())

#  Duplicate Order IDs Count
print("\nDuplicate Order IDs:")
print(orders.duplicated(subset=["order_id"]).sum())

#  Data Types
print("\nColumn Data Types:")
print(orders.dtypes)

# Missing Values Percentage
print("\nMissing Values Percentage:")
print((orders.isnull().sum() / len(orders)) * 100)