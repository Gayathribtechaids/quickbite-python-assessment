
import pandas as pd
from pathlib import Path

# ---------------------------------
# FILE PATHS
# ---------------------------------

base_path = Path(__file__).resolve().parent.parent

input_file = base_path / "data" / "QuickBite_Assessment.xlsx"
output_file = base_path / "cleaned_data" / "Quick_Bite_Data_Cleaning.xlsx"

output_file.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------
# COMMON TEXT CLEANING FUNCTION
# ---------------------------------

def clean_text_columns(df):

    for column in df.select_dtypes(include="object").columns:

        df[column] = df[column].apply(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    return df


# ---------------------------------
# COMMON CLEANING FUNCTION
# ---------------------------------

def remove_exact_duplicates(df, table_name):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"{table_name} - Exact duplicates removed:", before - after)

    return df


# =================================
# 1. AREAS CLEANING
# =================================

areas = pd.read_excel(input_file, sheet_name="areas")

print("\n========== AREAS ==========")
print("Before Cleaning:", len(areas))

areas = remove_exact_duplicates(areas, "Areas")
areas = areas.dropna(subset=["area_id"])
areas = clean_text_columns(areas)

print("After Cleaning:", len(areas))
print("Duplicate Area IDs:", areas.duplicated(subset=["area_id"]).sum())


# =================================
# 2. RESTAURANTS CLEANING
# =================================

restaurants = pd.read_excel(input_file, sheet_name="restaurants")

print("\n========== RESTAURANTS ==========")
print("Before Cleaning:", len(restaurants))

restaurants = remove_exact_duplicates(restaurants, "Restaurants")
restaurants = restaurants.dropna(subset=["restaurant_id"])
restaurants = clean_text_columns(restaurants)

print("After Cleaning:", len(restaurants))
print("Duplicate Restaurant IDs:",
      restaurants.duplicated(subset=["restaurant_id"]).sum())


# =================================
# 3. DELIVERY PARTNERS CLEANING
# =================================

delivery_partners = pd.read_excel(
    input_file,
    sheet_name="delivery_partners"
)

print("\n========== DELIVERY PARTNERS ==========")
print("Before Cleaning:", len(delivery_partners))

delivery_partners = remove_exact_duplicates(
    delivery_partners, "Delivery Partners"
)

delivery_partners = delivery_partners.dropna(
    subset=["partner_id"]
)

delivery_partners = clean_text_columns(delivery_partners)

print("After Cleaning:", len(delivery_partners))
print("Duplicate Partner IDs:",
      delivery_partners.duplicated(subset=["partner_id"]).sum())


# =================================
# 4. CUSTOMERS CLEANING
# =================================

customers = pd.read_excel(input_file, sheet_name="customers")

print("\n========== CUSTOMERS ==========")
print("Before Cleaning:", len(customers))

customers = remove_exact_duplicates(customers, "Customers")
customers = customers.dropna(subset=["customer_id"])
customers = clean_text_columns(customers)

print("After Cleaning:", len(customers))
print("Duplicate Customer IDs:",
      customers.duplicated(subset=["customer_id"]).sum())



# =================================
# 5. ORDERS CLEANING
# =================================

orders = pd.read_excel(
    input_file,
    sheet_name="orders"
)

print("\n========== ORDERS ==========")

print("Before Cleaning:", len(orders))

# ---------------------------------
# 1. REMOVE EXACT DUPLICATE ROWS
# ---------------------------------

before_duplicates = len(orders)

orders = orders.drop_duplicates()

print(
    "Exact Duplicate Rows Removed:",
    before_duplicates - len(orders)
)


# ---------------------------------
# 2. REMOVE MISSING ORDER IDs
# ---------------------------------

before_missing_id = len(orders)

orders = orders.dropna(subset=["order_id"])

print(
    "Rows Removed Without Order ID:",
    before_missing_id - len(orders)
)


# ---------------------------------
# 3. REMOVE EXTRA SPACES
# ---------------------------------

orders = clean_text_columns(orders)


# ---------------------------------
# 4. STANDARDIZE ORDER STATUS
# ---------------------------------

orders["order_status"] = orders["order_status"].str.upper()

orders["order_status"] = orders["order_status"].replace({
    "CANCELED": "CANCELLED"
})


# ---------------------------------
# 5. STANDARDIZE PAYMENT MODE
# ---------------------------------

orders["payment_mode"] = orders["payment_mode"].str.upper()


# ---------------------------------
# 6. STANDARDIZE COUPON CODE
# ---------------------------------

orders["coupon_code"] = orders["coupon_code"].str.upper()


# ---------------------------------
# 7. CONVERT ORDER AMOUNT TO NUMERIC
# ---------------------------------

orders["order_amount"] = (
    orders["order_amount"]
    .astype("string")
    .str.strip()
    .str.replace(
        r"(?i)^(?:rs\.?|inr)\s*",
        "",
        regex=True
    )
    .str.replace(",", "", regex=False)
)

orders["order_amount"] = pd.to_numeric(
    orders["order_amount"],
    errors="coerce"
)


# ---------------------------------
# 8. CONVERT DELIVERY MINUTES TO NUMERIC
# ---------------------------------

orders["delivery_minutes"] = (
    orders["delivery_minutes"]
    .astype("string")
    .str.strip()
    .str.replace(r"(?i)\s*min$", "", regex=True)
)

orders["delivery_minutes"] = pd.to_numeric(
    orders["delivery_minutes"],
    errors="coerce"
)


# ---------------------------------
# 9. STANDARDIZE ORDER DATETIME
# ---------------------------------

parsed_dates = pd.to_datetime(
    orders["order_datetime"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

print("\nOrder Date Validation:")
print("Total Orders:", len(orders))
print("Successfully Parsed:", parsed_dates.notna().sum())
print("Invalid Dates:", parsed_dates.isna().sum())

print("\nInvalid Date Records:")

print(
    orders.loc[
        parsed_dates.isna(),
        ["order_id", "order_datetime"]
    ].to_string(index=False)
)

# Assign standardized datetime values
orders["order_datetime"] = parsed_dates


# ---------------------------------
# 10. REMOVE DUPLICATES AFTER STANDARDIZATION
# ---------------------------------

before_standardization_duplicates = len(orders)

orders = orders.drop_duplicates()

print(
    "\nDuplicate Rows Removed After Standardization:",
    before_standardization_duplicates - len(orders)
)


# ---------------------------------
# 11. VALIDATE UNIQUE ORDER IDs
# ---------------------------------

print("\nAfter Cleaning:", len(orders))

print(
    "Duplicate Order IDs:",
    orders.duplicated(subset=["order_id"]).sum()
)

print("Unique Order IDs:", orders["order_id"].nunique())


# ---------------------------------
# 12. DISPLAY CLEANED VALUES
# ---------------------------------

print("\nOrder Status Values:")
print(orders["order_status"].value_counts())

print("\nPayment Mode Values:")
print(orders["payment_mode"].value_counts())


# ---------------------------------
# 13. DISPLAY MISSING VALUES
# ---------------------------------

print("\nMissing Values After Cleaning:")
print(orders.isnull().sum())


# =================================
# 6. FEEDBACK CLEANING
# =================================

feedback = pd.read_excel(input_file, sheet_name="feedback")

print("\n========== FEEDBACK ==========")
print("Before Cleaning:", len(feedback))

feedback = remove_exact_duplicates(feedback, "Feedback")

# Feedback ID and Order ID are mandatory
feedback = feedback.dropna(
    subset=["feedback_id", "order_id"]
)

feedback = clean_text_columns(feedback)

print("After Cleaning:", len(feedback))
print("Duplicate Feedback IDs:",
      feedback.duplicated(subset=["feedback_id"]).sum())

print("\nMissing Values:")
print(feedback.isnull().sum())

# Validate feedback order IDs

invalid_feedback_orders = feedback[
    ~feedback["order_id"].isin(orders["order_id"])
]

print("\nFeedback Order ID Validation:")
print("Total Feedback Records:", len(feedback))
print("Invalid Order IDs:", len(invalid_feedback_orders))

# =================================
# 7. SAVE ALL CLEANED TABLES
# =================================

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    areas.to_excel(writer, sheet_name="areas", index=False)

    restaurants.to_excel(
        writer,
        sheet_name="restaurants",
        index=False
    )

    delivery_partners.to_excel(
        writer,
        sheet_name="delivery_partners",
        index=False
    )

    customers.to_excel(
        writer,
        sheet_name="customers",
        index=False
    )

    orders.to_excel(
        writer,
        sheet_name="orders",
        index=False
    )

    feedback.to_excel(
        writer,
        sheet_name="feedback",
        index=False
    )
# =================================
# 8. VERIFY SAVED EXCEL FILE
# =================================

print("\n========== SAVING RESULTS ==========")

saved_data = pd.ExcelFile(output_file)

print("Excel file saved successfully!")
print("Output File:", output_file)
print("\nSaved Sheets:")
print(saved_data.sheet_names)