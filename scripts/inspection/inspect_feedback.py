
import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parents[2]
input_file = base_path / "data" / "QuickBite_Assessment.xlsx"

feedback = pd.read_excel(input_file, sheet_name="feedback")

print("========== FEEDBACK DATA INSPECTION ==========")

print("\nTotal Rows and Columns:")
print(feedback.shape)

print("\nMissing Values Count:")
print(feedback.isnull().sum())

print("\nTotal Missing Values:")
print(feedback.isnull().sum().sum())

print("\nExact Duplicate Rows:")
print(feedback.duplicated().sum())

print("\nDuplicate Feedback IDs:")
print(feedback.duplicated(subset=["feedback_id"]).sum())

print("\nColumn Data Types:")
print(feedback.dtypes)
