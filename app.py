
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="StockSense",
    page_icon="📦",
    layout="wide"
)

st.title("📦 StockSense")
st.subheader(
    "Inventory Shortage Prediction and Product Demand Mining"
)
st.write(
    "Upload your inventory dataset to analyze product demand "
    "and identify products that may need restocking."
)

uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload your inventory CSV file to begin.")
    st.stop()

try:
    df = pd.read_csv(uploaded_file)
except Exception:
    st.error("Unable to read this file. Please upload a valid CSV.")
    st.stop()

# Match column names without worrying about capitalization
columns = {str(c).strip().lower(): c for c in df.columns}

def get_col(*names):
    for name in names:
        if name.lower() in columns:
            return columns[name.lower()]
    return None

product = get_col("Product ID", "ProductID", "StockCode", "Product")
stock = get_col(
    "Inventory Level", "Current Stock",
    "Available Stock", "Stock Level"
)
sold = get_col("Units Sold", "Quantity Sold", "Quantity")
forecast = get_col(
    "Demand Forecast", "Predicted Demand",
    "Predicted Daily Demand", "Forecast"
)

if product is None:
    st.error("Product ID column was not found in your CSV.")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

if stock is None:
    st.error("Inventory Level column was not found in your CSV.")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

df[stock] = pd.to_numeric(df[stock], errors="coerce")

if sold:
    df[sold] = pd.to_numeric(df[sold], errors="coerce")

if forecast:
    df[forecast] = pd.to_numeric(df[forecast], errors="coerce")

df = df.dropna(subset=[product, stock])
df = df[df[stock] >= 0].copy()

if df.empty:
    st.warning("No valid inventory records were found.")
    st.stop()

# Use an existing forecast, or sales as a simple demand estimate
if forecast:
    df["Display Demand"] = df[forecast]
    if sold:
        df["Display Demand"] = df["Display Demand"].fillna(df[sold])
    demand_label = "Forecast / estimated demand"
elif sold:
    df["Display Demand"] = df[sold]
    demand_label = "Units sold (demand estimate)"
else:
    df["Display Demand"] = 0
    demand_label = "Demand data unavailable"

df["Display Demand"] = (
    pd.to_numeric(df["Display Demand"], errors="coerce")
    .fillna(0)
    .clip(lower=0)
)

# Simple demonstration reorder rule: demand + 20% buffer
df["Reorder Point"] = np.ceil(df["Display Demand"] * 1.2)

df["Status"] = np.where(
    df[stock] <= df["Reorder Point"],
    "Low Stock",
    "Stock Available"
)

total_products = df[product].nunique()
low_stock = int((df["Status"] == "Low Stock").sum())

a, b = st.columns(2)
a.metric("Total Products", total_products)
b.metric("Low Stock Alerts", low_stock)

st.divider()

st.header("📊 Product Demand Analysis")
st.caption(demand_label)

chart_df = (
    df.groupby(product)["Display Demand"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(chart_df)

st.header("⚠️ Inventory Shortage Alerts")
alerts = df[df["Status"] == "Low Stock"]

if alerts.empty:
    st.success("No products currently meet the low-stock rule.")
else:
    st.dataframe(
        alerts[[product, stock, "Display Demand",
                "Reorder Point", "Status"]],
        use_container_width=True
    )

st.header("📋 Inventory Report")
st.dataframe(df, use_container_width=True)

st.download_button(
    "⬇️ Download Inventory Report",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="StockSense_Report.csv",
    mime="text/csv"
)
