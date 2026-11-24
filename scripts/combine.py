
import pandas as pd
from pathlib import Path

# Project folder path
base_path = Path(__file__).resolve().parent.parent

# Input and output files
input_file = base_path / "cleaned_data" / "Quick_Bite_Data_Cleaning.xlsx"
output_file = base_path / "cleaned_data" / "Quick_Bite_Combined_Data.xlsx"


# Read all cleaned sheets
areas = pd.read_excel(input_file, sheet_name="areas")
restaurants = pd.read_excel(input_file, sheet_name="restaurants")
partners = pd.read_excel(input_file, sheet_name="delivery_partners")
customers = pd.read_excel(input_file, sheet_name="customers")
orders = pd.read_excel(input_file, sheet_name="orders")
feedback = pd.read_excel(input_file, sheet_name="feedback")


# Orders is the main table
combined = orders.copy()

print("Initial Orders:", len(combined))


# 1. Join Customers using customer_id
combined = combined.merge(
    customers[["customer_id", "customer_name"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print("After Customers:", len(combined))


# 2. Join Restaurants using restaurant_id
combined = combined.merge(
    restaurants[["restaurant_id", "restaurant_name", "cuisine", "area_id"]],
    on="restaurant_id",
    how="left",
    validate="many_to_one"
)

print("After Restaurants:", len(combined))


# 3. Join Areas using area_id
combined = combined.merge(
    areas[["area_id", "area_name", "city"]],
    on="area_id",
    how="left",
    validate="many_to_one"
)

print("After Areas:", len(combined))


# 4. Join Delivery Partners using partner_id
combined = combined.merge(
    partners[["partner_id", "partner_name", "vehicle_type"]],
    on="partner_id",
    how="left",
    validate="many_to_one"
)

print("After Delivery Partners:", len(combined))


# 5. Join Feedback using order_id
combined = combined.merge(
    feedback[["order_id", "rating", "comment"]],
    on="order_id",
    how="left",
    validate="one_to_one"
)

print("After Feedback:", len(combined))


# Extract order date, time and weekday
combined["order_date"] = combined["order_datetime"].dt.date
combined["order_time"] = combined["order_datetime"].dt.time
combined["order_day"] = combined["order_datetime"].dt.day_name()


# Identify late deliveries
combined["is_late"] = pd.NA

valid_delivery = combined["delivery_minutes"].notna()

combined.loc[valid_delivery, "is_late"] = (
    combined.loc[valid_delivery, "delivery_minutes"]
    .gt(45)
    .map({True: "Yes", False: "No"})
)


# Select the required columns in order
final_columns = [
    "order_id",
    "order_date",
    "order_time",
    "order_day",
    "customer_name",
    "restaurant_name",
    "cuisine",
    "area_name",
    "city",
    "partner_name",
    "vehicle_type",
    "order_amount",
    "payment_mode",
    "coupon_code",
    "order_status",
    "delivery_minutes",
    "is_late",
    "rating",
    "comment"
]

combined = combined[final_columns]


# Validate final data
print("\nFinal Combined Data")
print("Rows:", len(combined))
print("Columns:", len(combined.columns))
print("Duplicate Order IDs:", combined["order_id"].duplicated().sum())

print("\nMissing Values:")
print(combined.isnull().sum())


# Save combined data
combined.to_excel(output_file, index=False)

print("\nCombined data saved successfully!")
print("File:", output_file)
