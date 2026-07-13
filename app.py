import streamlit as st

st.set_page_config(page_title="Employee System", page_icon="🧑‍💼", layout="wide")

st.title(" Employee Management System")
st.markdown(
    """
    Welcome to the Employee Management System.

    Use the sidebar to navigate between pages:
    - **Dashboard**: view data and analytics.
    - **Employee Management**: add, update, or delete employees.

    This app only communicates with the FastAPI backend and never
    accesses the database directly.
    """
)
