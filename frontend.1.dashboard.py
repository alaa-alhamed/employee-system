import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import pandas as pd

from frontend.api_client import get_employees

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard - Employee Data")

employees, error = get_employees()

if error:
    st.error(f"Could not connect to backend: {error}")
    st.info("Make sure the FastAPI server is running.")
    st.stop()

if not employees:
    st.warning("No employees in the database yet. Add one from the Employee Management page.")
    st.stop()

df = pd.DataFrame(employees)

st.subheader("Employee Table")
st.dataframe(df, use_container_width=True)

st.subheader("Average Salary")
avg_salary = df["salary"].mean()
st.metric(label="Average Salary", value=f"{avg_salary:,.2f}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Employees per Department")
    dept_counts = df.groupby("department")["employee_id"].count()
    st.bar_chart(dept_counts)

with col2:
    st.subheader("Salary Distribution")
    hist_values = pd.cut(df["salary"], bins=10).value_counts().sort_index()
    hist_df = pd.DataFrame({
        "range": [str(interval) for interval in hist_values.index],
        "count": hist_values.values,
    }).set_index("range")
    st.bar_chart(hist_df)
