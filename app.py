import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="ShopEasy Dashboard", layout="wide")
st.title("🛒 ShopEasy Sales Analytics Dashboard")

# ============================================
# LOAD DATA
# ============================================
sales_df = pd.read_csv("sales.csv")
inventory_df = pd.read_csv("inventory.csv")
sales_df['date_of_sale'] = pd.to_datetime(sales_df['date_of_sale'])
sales_df['revenue'] = sales_df['quantity_sold'] * sales_df['unit_price']

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.header("🔍 Filters")
categories = ["All"] + list(sales_df['category'].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

st.sidebar.header("📦 Inventory Settings")
threshold = st.sidebar.number_input("Low Stock Threshold", min_value=5, max_value=100, value=20)

min_date = sales_df['date_of_sale'].min()
max_date = sales_df['date_of_sale'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Apply filters
filtered_df = sales_df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['date_of_sale'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['date_of_sale'] <= pd.to_datetime(date_range[1]))
    ]

# ============================================
# SECTION B(a) - KEY METRICS
# ============================================
st.header("📊 Key Business Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"RM {filtered_df['revenue'].sum():,.2f}")
col2.metric("Total Units Sold", f"{filtered_df['quantity_sold'].sum():,}")
col3.metric("Average Selling Price", f"RM {filtered_df['unit_price'].mean():,.2f}")

# Data Table
st.subheader("📋 Sales Data")
st.dataframe(filtered_df)

# ============================================
# SECTION B(b) - VISUALIZATIONS
# ============================================
st.header("📈 Sales Visualizations")

col1, col2 = st.columns(2)

# 1. Bar Chart - Revenue by Category
with col1:
    st.subheader("Revenue by Category")
    fig1, ax1 = plt.subplots()
    filtered_df.groupby('category')['revenue'].sum().plot(kind='bar', ax=ax1, color='steelblue')
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Revenue (RM)")
    plt.tight_layout()
    st.pyplot(fig1)

# 2. Line Chart - Sales Trend
with col2:
    st.subheader("Sales Trend Over Time")
    fig2, ax2 = plt.subplots()
    filtered_df.groupby('date_of_sale')['quantity_sold'].sum().plot(kind='line', ax=ax2, marker='o', color='green')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Quantity Sold")
    plt.tight_layout()
    st.pyplot(fig2)

# 3. Scatter Plot
st.subheader("Category vs Revenue")
fig3, ax3 = plt.subplots()
ax3.scatter(filtered_df['category'], filtered_df['revenue'], color='orange')
ax3.set_xlabel("Category")
ax3.set_ylabel("Revenue (RM)")
plt.tight_layout()
st.pyplot(fig3)

# ============================================
# SECTION B(c) - INVENTORY MANAGEMENT
# ============================================
st.header("📦 Inventory Management")

inventory_list = inventory_df.to_dict('records')
low_stock = list(filter(lambda p: p['stock_quantity'] < threshold, inventory_list))
total_at_risk = reduce(lambda a, b: a + b['stock_quantity'], low_stock, 0)

if low_stock:
    st.warning(f"⚠️ {len(low_stock)} products are below threshold! Total units at risk: {total_at_risk}")
    low_stock_df = pd.DataFrame(low_stock)
    st.dataframe(low_stock_df)

# Full inventory table
st.subheader("Full Inventory")
inventory_df['status'] = inventory_df['stock_quantity'].apply(
    lambda x: "🔴 Low Stock" if x < threshold else "🟢 OK"
)
st.dataframe(inventory_df)