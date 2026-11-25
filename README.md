# QuickBite Data Analysis
### From Raw Data to Reliable Business Insights

## 1. Project Overview

This project focuses on preparing and analysing QuickBite's food delivery data using Python.

The objective was to transform multiple related Excel datasets into a structured dataset and use it to understand three aspects of the business:

- Area-wise order and revenue performance
- Daily customer cuisine preferences
- Delivery vehicle performance

I approached this task in three stages: data cleaning, data integration, and business analysis. Each stage was handled separately so that the data could be inspected and validated before moving to the next stage.

## 2. Understanding the Source Data

The original Excel workbook contained six sheets. I inspected each sheet individually to understand its structure, data types, identifiers and relationships.

| Dataset     |                Purpose                      |

| Areas       |    Area details and identifiers             |
| Restaurants | Restaurant information and cuisine          |
| Delivery Partners | Delivery partner information          |
| Customers    | Customer details and area references       |
| Orders       | Order transactions, amounts, status, and  delivery time  |
| Feedback     | Customer ratings and comments              |

I selected the Orders dataset as the primary table because the required analysis was centred on individual orders.

The remaining datasets provided additional information that could be connected through their respective identifiers.

## 3. Data Inspection and Quality Issues

Before cleaning, I inspected the dimensions, column names, data types, duplicate records and missing values in all six datasets.

The inspection identified the following issues:

- Duplicate records in multiple sheets.
- Missing values in several columns.
- Inconsistent date representations.
- Order amounts containing currency text and formatting differences.
- Order records containing references that did not match some related customer, restaurant or delivery partner records.
- Inconsistent vehicle names caused by differences in formatting and naming.

I treated these as separate data quality issues because each one could affect the reliability of the combined dataset or the final calculations.

## 4. Data Cleaning

I used Python and Pandas to clean the datasets. The original workbook was kept separate and the cleaned sheets were exported into a new Excel file.

### 4.1 Duplicate Removal

I removed duplicate records and checked the resulting record counts.

| Dataset    | Original Rows | Cleaned Rows | Rows Removed |

| Areas      | 21            | 20           | 1            |
| Restaurants| 44            | 42           | 2            |
| Delivery Partners | 51     | 50           | 1            |
| Customers  | 414           | 400          | 14           |
| Orders     | 1,567         | 1,500        | 67           |
| Feedback   | 711           | 693          | 18           |

For Orders, duplicate checking included an additional standardisation step. After removing 52 exact duplicate records, 15 additional duplicate records were identified after standardisation. The final Orders dataset contained 1,500 unique order IDs.

### 4.2 Missing Value Handling

I examined missing values column by column instead of treating every missing value as an error.

The following missing values remained in the cleaned datasets:

| Dataset| Column       | Missing Values |

| Orders | customer_id  | 17             |
| Orders | restaurant_id| 13             |
| Orders | partner_id   | 109            |
| Orders | order_amount | 16             |
| Orders | delivery_minutes | 214        |
| Orders | coupon_code  | 986            |
| Feedback | rating     | 5              |
| Feedback | comment    | 373            |
| Customers | email     | 31             |
| Customers | area_id   | 15             |
| Restaurants | rating  | 6              |

I retained unavailable information rather than replacing it with arbitrary values. For example, an order with a missing delivery time can still contribute to the total order count, but it cannot be used in delivery-time calculations.

### 4.3 Date and Amount Standardisation

Date columns were converted into a consistent datetime format using Pandas.

Order amount values were cleaned by removing currency prefixes and unwanted formatting characters, including commas before converting them into numeric values.

This made the columns suitable for date-based grouping and numerical calculations.

### 4.4 Cleaning Output

The six cleaned datasets were saved in:

`cleaned_data/Quick_Bite_Data_Cleaning.xlsx`

## 5. Combining the Datasets

After cleaning, I used Orders as the primary dataset and connected the related tables using LEFT JOIN operations.

| Primary Table | Related Table | Join Key |

| Orders        | Customers     | customer_id |
| Orders        | Restaurants   | restaurant_id |
| Restaurants   | Areas         | area_id |
| Orders        | Delivery Partners | partner_id |
| Orders        | Feedback      | order_id |

I chose LEFT JOIN because I wanted to preserve the order records even when some related information was unavailable.

I also applied merge validation to check the expected relationships and prevent unexpected row multiplication.

### 5.1 Relationship Validation

The following unmatched references were identified:

| Relationship         | Unmatched Records |

| Orders → Customers   | 17                |
| Orders → Restaurants | 31                |
| Orders → Delivery Partners | 24          |
| Restaurants → Areas | 0                  |
| Customers → Areas   | 0                  |
| Feedback → Orders   | 0                  |

These unmatched references were not silently removed. Since Orders was the primary table, the LEFT JOIN approach retained the order records while unavailable related fields remained missing.

I also verified that the primary identifiers were unique and non-missing, and that Feedback contained at most one record per order.

The final combined dataset retained **1,500 rows**, maintaining one row per order.

The output was saved as:

`cleaned_data/Quick_Bite_Combined_Data.xlsx`

## 6. Business Analysis

All three analysis outputs were calculated from the combined dataset.

### 6.1 Area Performance

**Business question:** Which areas generate higher revenue, and which areas experience more delivery delays?

I grouped the data by area and calculated:

- Total orders
- Orders with available revenue information
- Total revenue
- Orders with available delivery time
- Average delivery time
- Number of late deliveries
- Late delivery percentage

The late delivery percentage was calculated as:

`(Late Deliveries / Eligible Delivery Orders) * 100`

For this analysis, a delivery was considered late when its delivery time was greater than 45 minutes.

**Key findings:**

| Observation          | Result |

| Highest revenue area | Anna Nagar – ₹80,172.12 |
| Highest order volume | Madhapur – 189 orders |
| Highest late delivery percentage | Andheri West – 44.44% |
| Lowest late delivery percentage | Kukatpally – 2.38% |

The area analysis shows that order volume, revenue and delivery efficiency do not necessarily move together. Madhapur recorded the highest number of orders while Anna Nagar generated the highest revenue.

Andheri West had a comparatively high late delivery percentage, indicating an area that may need further delivery-performance investigation.

Orders without an available area name were excluded from area-wise grouping.

### 6.2 Top Cuisine by Day

**Business question:** Which cuisine receives the highest number of orders on each day of the week?

I grouped orders by weekday and cuisine, calculated the number of orders for each combination and selected the cuisine with the highest count for each weekday.

The order share percentage was calculated using the total number of orders recorded for that weekday.

`(Cuisine Orders / Total Orders for the Day) * 100`

**Results:**

| Day     | Top Cuisine | Cuisine Orders | Order Share |

| Monday  | South Indian | 39 | 19.40% |
| Tuesday | South Indian | 31 | 15.82% |
| Wednesday | Chinese    | 58 | 25.78% |
| Thursday | South Indian| 32 | 15.76% |
| Friday  | Biryani      | 54 | 23.58% |
| Saturday | Pizza       | 47 | 20.17% |
| Sunday   | Biryani     | 38 | 17.84% |

**Key findings:**

South Indian cuisine was the leading category on Monday, Tuesday and Thursday. Biryani led on Friday and Sunday, while Chinese and Pizza led on Wednesday and Saturday respectively.

This suggests that customer cuisine preferences vary across the week. These patterns could help the business consider day-specific promotions and restaurant campaigns.

### 6.3 Vehicle Performance

**Business question:** How do different vehicle categories compare in delivery efficiency?

For this analysis, I considered delivered orders with both vehicle type and delivery time available.

I calculated:

- Number of delivered orders
- Average delivery time
- Number of late deliveries
- Late delivery percentage

Vehicle names were standardised to reduce category fragmentation caused by inconsistent formatting and naming variations.

Vehicles were ranked primarily by the lowest late delivery percentage, with average delivery time used as the secondary sorting factor.

**Results:**

| Vehicle Type | Delivered Orders | Average Delivery (Minutes) | Late Deliveries | Late Delivery % | Rank |

| Motor Bike | 116 | 34.10 | 12 | 10.34% | 1 |
| Bike       | 182 | 34.51 | 19 | 10.44% | 2 |
| EV         | 66 | 33.71 | 7 | 10.61% | 3 |
| EV Scooter | 207 | 33.77 | 25 | 12.08% | 4 |
| Scooty     | 82 | 35.93 | 10 | 12.20%  | 5 |
| Scooter    | 218 | 37.00 | 33 | 15.14% | 6 |
| activa     | 102 | 37.14 | 20 | 19.61% | 7 |
| Bicycle    | 190 | 45.07 | 92 | 48.42% | 8 |
| Cycle      | 16  | 45.88 | 8 | 50.00%  | 9 |

**Key findings:**

- Motor Bike recorded the lowest late delivery percentage at 10.34%.
- Bike and EV also showed comparatively low late delivery percentages.
- Bicycle and Cycle recorded considerably higher late delivery percentages.
- Bicycle had 92 late deliveries among 190 eligible delivered orders.

The analysis indicates differences in delivery outcomes across vehicle categories. However, vehicle type alone does not establish the cause of a delay. Factors such as distance, traffic and delivery location were not separately evaluated.

The vehicle analysis included 1,179 eligible delivered orders. The remaining delivered orders were not included because vehicle type or delivery time was unavailable.

## 7. Validation and Limitations

I performed validation checks throughout the workflow instead of relying only on the final Excel outputs.

The main checks included:

- Verifying unique and non-missing primary identifiers.
- Checking duplicate records after cleaning.
- Validating relationships between the datasets.
- Confirming that the combined dataset retained 1,500 order records.
- Checking that feedback did not multiply order records during joining.
- Using only available values for calculations that required specific columns.

A few limitations should be considered while interpreting the results:

1. The area analysis includes only orders with an available area name.
2. Revenue is calculated from available order amounts without filtering by order status in the current implementation.
3. Cuisine order share uses all orders recorded for the weekday as its denominator including orders with missing cuisine.
4. Vehicle performance is calculated only from delivered orders with available vehicle type and delivery time.
5. The late delivery threshold is greater than 45 minutes. This is the rule used in this analysis not a separately verified operational SLA.

These considerations help distinguish what the data demonstrates from what cannot be concluded from the available information.

## 8. Tools and Technologies

| Tool | Usage |

| Python     | Main programming language                     |
| Pandas     | Data cleaning, merging, grouping and analysis |
| OpenPyXL   | Excel workbook handling                       |
| Microsoft Excel| Reviewing output workbooks                |
| Git and GitHub | Version control and source code management|

## 9. Project Structure

quickbite-python-assessment/
│
├── data/
│   └── QuickBite_Assessment.xlsx
│
├── scripts/
│   ├── inspection/
│   │   ├── inspect_areas.py
│   │   ├── inspect_restaurants.py
│   │   ├── inspect_delivery_partners.py
│   │   ├── inspect_customers.py
│   │   ├── inspect_orders.py
│   │   └── inspect_feedback.py
│   │
│   ├── analysis/
│   │   ├── inspect_analysis.py
│   │   └── analysis.py
│   │
│   ├── cleaning.py
│   └── combine.py
│
├── cleaned_data/
├── requirements.txt
├── .gitignore
└── README.md

## 10. How to Run the Project

### Prerequisites

- Python installed on the system.
- Git installed.
- Original QuickBite Excel workbook.

### Step 1: Clone the repository

```bash
git clone https://github.com/Gayathribtechaids/quickbite-python-assessment.git
cd quickbite-python-assessment
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

For Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Add the source dataset

Place `QuickBite_Assessment.xlsx` inside the `data` directory.

### Step 6: Run the scripts in order

```bash
python scripts/cleaning.py
python scripts/combine.py
python scripts/analysis/analysis.py
```

The generated Excel workbooks will be saved in the `cleaned_data` directory.

## 11. Final Deliverables

| Output File                   | Description |

| Quick_Bite_Data_Cleaning.xlsx | Six cleaned datasets |
| Quick_Bite_Combined_Data.xlsx | Combined order-level dataset |
| Quick_Bite_Analysis.xlsx      | Area Performance, Top Cuisine by Day and Vehicle Performance |

## 12. Conclusion

This project involved more than preparing three Excel output sheets. It required understanding how multiple datasets were related, identifying data quality issues deciding how missing information should be handled and validating the results after integration.

The final analysis provides a view of QuickBite's area-level business performance, weekday cuisine preferences and vehicle-wise delivery outcomes.

One key learning from this exercise was that reliable analysis depends not only on calculations but also on the quality of the underlying data and the decisions made during preparation.

The approach followed in this project was to preserve available information, make analytical rules explicit, validate each stage and interpret the results within the limitations of the dataset.