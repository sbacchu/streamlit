import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

# st.write("## Your additions")
# st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
# st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
# st.write("### (3) show a line chart of sales for the selected items in (2)")
# st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
# st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")

st.write("-----------------------------------------------")

# Get the unique categories
categories = df["Category"].unique()
selected_category = st.selectbox("Select a Category", categories)

# Get the unique sub-categories for the selected category
sub_categories = df[df["Category"] == selected_category]["Sub_Category"].unique()
selected_sub_categories = st.multiselect("Select Sub-Categories", sub_categories)

# Line chart of sales for the selected items
selected_df = df[(df["Category"] == selected_category) & (df["Sub_Category"].isin(selected_sub_categories))]
selected_sales_by_month = selected_df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.line_chart(selected_sales_by_month, y="Sales")

# Metrics for the selected items
total_sales = round(selected_df["Sales"].sum(), 2)
total_profit = round(selected_df["Profit"].sum(), 2)
if total_profit > 0:
    profit_margin = round(total_profit / total_sales * 100, 2) 
else:
    profit_margin = 0



col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", f"${total_sales}")
    
with col2:
    st.metric("Total Profit", f"${total_profit}")
    
with col3:
    st.metric("Profit Margin (%)", f"{profit_margin}%")
    
# Overall average profit margin
overall_avg_profit_margin = round(df["Profit"].sum() / df["Sales"].sum() * 100, 2)
st.metric("Overall Average Profit Margin", f"{overall_avg_profit_margin}%", delta=profit_margin - overall_avg_profit_margin)
    
