
import pandas as pd
import streamlit as st
import plotly.express as px

# Load processed data (replace this with the real path if deploying)
df = pd.read_csv("TSU_Graduate_Summary.csv")

st.set_page_config(page_title="TSU Graduate Program Dashboard", layout="wide")
st.title("📊 TSU Graduate Program Outcomes Dashboard")

# Sidebar filters
college = st.sidebar.selectbox("Select College:", options=["All"] + sorted(df['MajorCollege'].dropna().unique().tolist()))
major = st.sidebar.selectbox("Select Major:", options=["All"] + sorted(df['Major'].dropna().unique().tolist()))

# Filter logic
filtered_df = df.copy()
if college != "All":
    filtered_df = filtered_df[filtered_df['MajorCollege'] == college]
if major != "All":
    filtered_df = filtered_df[filtered_df['Major'] == major]

# Metrics display
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg GPA", f"{filtered_df['CumulativeGPA'].mean():.2f}")
col2.metric("Avg Loans", f"${filtered_df['TotalLoansAccepted'].mean():,.0f}")
col3.metric("Avg Grants", f"${filtered_df['TotalGrantsAccepted'].mean():,.0f}")
col4.metric("Employability Score", f"{filtered_df['EmployabilityScore'].mean():.2f}")

# Charts
st.subheader("Graduate Count by Major")
grad_chart = px.bar(
    filtered_df.sort_values(by='GraduateCount', ascending=False).head(15),
    x='GraduateCount',
    y='Major',
    orientation='h',
    title='Top Majors by Number of Graduates'
)
st.plotly_chart(grad_chart, use_container_width=True)

st.subheader("TSU vs National Debt Comparison")
debt_df = filtered_df[filtered_df['NationalAvgDebt'] != 'N/A'].copy()
debt_df['NationalAvgDebt'] = pd.to_numeric(debt_df['NationalAvgDebt'], errors='coerce')

comparison_chart = px.bar(
    debt_df.sort_values(by='TotalLoansAccepted', ascending=False).head(10),
    x='Major',
    y=['TotalLoansAccepted', 'NationalAvgDebt'],
    barmode='group',
    title='Average Student Loan Debt: TSU vs National'
)
st.plotly_chart(comparison_chart, use_container_width=True)

st.caption("Developed for Texas Southern University by Higher Education Compliance Partners")
