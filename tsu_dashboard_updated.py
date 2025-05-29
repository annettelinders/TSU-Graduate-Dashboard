
import pandas as pd
import streamlit as st
import plotly.express as px

# Load processed data
df = pd.read_csv("TSU_Graduate_Summary_Updated.csv")

st.set_page_config(page_title="TSU Graduate Program Dashboard", layout="wide")
st.title("📊 TSU Graduate Outcomes Dashboard")

# Sidebar filter
program = st.sidebar.selectbox("Select a Degree Program:", options=["All"] + sorted(df['Program'].unique().tolist()))

# Filter data
filtered_df = df.copy()
if program != "All":
    filtered_df = filtered_df[filtered_df['Program'] == program]

# Display key metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average GPA", f"{filtered_df['GPA'].mean():.2f}")
col2.metric("Avg Loan per Student", f"${filtered_df['Loans'].mean():,.0f}")
col3.metric("Unmet Need", f"${filtered_df['UnmetNeed'].mean():,.0f}")

# Bar chart - Average cost components
st.subheader("Cost Breakdown")
cost_df = filtered_df[['Tuition', 'TotalCost', 'Grants']].mean().reset_index()
cost_df.columns = ['Type', 'Amount']
fig = px.bar(cost_df, x='Type', y='Amount', title='Average Tuition, Total Cost, and Grants')
st.plotly_chart(fig, use_container_width=True)

# Table of data
st.subheader("Summary Table")
st.dataframe(filtered_df)
