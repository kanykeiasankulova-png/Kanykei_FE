import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ============================================
# CREATE SALES CSV - 50+ rows
# ============================================
products_list = [
    {"name": "Phone",         "category": "Electronics", "unit_price": 1200},
    {"name": "Laptop",        "category": "Electronics", "unit_price": 2500},
    {"name": "Headphone",     "category": "Electronics", "unit_price": 150},
    {"name": "Shirt",         "category": "Clothing",    "unit_price": 45},
    {"name": "Jacket",        "category": "Clothing",    "unit_price": 120},
    {"name": "Shoes",         "category": "Clothing",    "unit_price": 90},
    {"name": "Table",         "category": "Furniture",   "unit_price": 350},
    {"name": "Chair",         "category": "Furniture",   "unit_price": 180},
    {"name": "Sofa",          "category": "Furniture",   "unit_price": 800},
    {"name": "Cream",         "category": "Beauty",      "unit_price": 35},
    {"name": "Shampoo",       "category": "Beauty",      "unit_price": 25},
    {"name": "Lipstick",      "category": "Beauty",      "unit_price": 40},
    {"name": "Mat",           "category": "Sports",      "unit_price": 60},
    {"name": "Ball",          "category": "Sports",      "unit_price": 30},
    {"name": "Elastic Band",  "category": "Sports",      "unit_price": 15},
]

# Generate 60 rows of sales data
random.seed(42)
sales_data = []
start_date = datetime(2026, 1, 1)

for i in range(60):
    product = random.choice(products_list)
    quantity = random.randint(1, 30)
    date = start_date + timedelta(days=random.randint(0, 90))
    sales_data.append({
        "product_name": product["name"],
        "category":     product["category"],
        "quantity_sold": quantity,
        "unit_price":   product["unit_price"],
        "date_of_sale": date.strftime("%Y-%m-%d")
    })

sales_df = pd.DataFrame(sales_data)
sales_df = sales_df.sort_values("date_of_sale").reset_index(drop=True)
sales_df.to_csv("sales.csv", index=False)
print("sales.csv created!")
print(sales_df.head(10))
print(f"Total rows: {len(sales_df)}")

# ============================================
# CREATE INVENTORY CSV
# ============================================
inventory_data = []
for product in products_list:
    inventory_data.append({
        "product_name": product["name"],
        "category":     product["category"],
        "stock_quantity": random.randint(3, 100)
    })

inventory_df = pd.DataFrame(inventory_data)
inventory_df.to_csv("inventory.csv", index=False)
print("\ninventory.csv created!")
print(inventory_df)