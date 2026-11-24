
import pandas as pd
from pathlib import Path

# Get project root folder
base_path = Path(__file__).resolve().parents[2]

# Combined Excel file path
input_file = base_path / "cleaned_data" / "Quick_Bite_Combined_Data.xlsx"


# Read combined dataset
df = pd.read_excel(input_file)


# 1. Basic dataset information
print("\n========== DATASET OVERVIEW ==========")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)


# 2. Missing values inspection
print("\n========== MISSING VALUES ==========")

missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().sum() / len(df) * 100
).round(2)

missing_report = pd.DataFrame({
    "Missing Count": missing_count,
    "Missing Percentage": missing_percentage
})

print(missing_report)


# 3. Duplicate order inspection
print("\n========== DUPLICATE CHECK ==========")

print(
    "Duplicate Order IDs:",
    df["order_id"].duplicated().sum()
)

print(
    "Missing Order IDs:",
    df["order_id"].isnull().sum()
)


# 4. Area Performance data inspection
print("\n========== AREA PERFORMANCE ==========")

area_orders = df[df["area_name"].notna()]

area_revenue = area_orders[
    area_orders["order_amount"].notna()
]

area_delivery = area_orders[
    area_orders["delivery_minutes"].notna()
]

print("Orders with Area:", len(area_orders))
print("Orders with Revenue Data:", len(area_revenue))
print("Orders with Delivery Data:", len(area_delivery))


# 5. Top Cuisine by Day inspection
print("\n========== TOP CUISINE BY DAY ==========")

cuisine_data = df[
    df["order_day"].notna() &
    df["cuisine"].notna()
]

print("Valid Cuisine Records:", len(cuisine_data))

print("\nWeekday Distribution:")
print(cuisine_data["order_day"].value_counts())


# 6. Vehicle Performance inspection
print("\n========== VEHICLE PERFORMANCE ==========")

delivered_data = df[
    df["order_status"].eq("DELIVERED")
]

vehicle_data = delivered_data[
    delivered_data["vehicle_type"].notna() &
    delivered_data["delivery_minutes"].notna()
]

print("Total Delivered Orders:", len(delivered_data))
print("Valid Vehicle Records:", len(vehicle_data))

print("\nVehicle Type Distribution:")
print(vehicle_data["vehicle_type"].value_counts())


# 7. Delivery classification inspection
print("\n========== DELIVERY CLASSIFICATION ==========")

print("\nLate Delivery Values:")
print(df["is_late"].value_counts(dropna=False))

print("\nDelivery Time Statistics:")
print(df["delivery_minutes"].describe())


# 8. Rating inspection
print("\n========== CUSTOMER FEEDBACK ==========")

print("Available Ratings:", df["rating"].notna().sum())
print("Missing Ratings:", df["rating"].isnull().sum())


print("\n========== INSPECTION COMPLETED ==========")
