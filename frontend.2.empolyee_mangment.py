import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st

from frontend.api_client import (
    get_employees,
    create_employee,
    update_employee,
    delete_employee,
)

st.set_page_config(page_title="Employee Management", page_icon="🛠️", layout="wide")
st.title("🛠️ Employee Management")

tab_add, tab_update, tab_delete = st.tabs(["➕ Add Employee", "✏️ Update Employee", "🗑️ Delete Employee"])

with tab_add:
    st.subheader("Add New Employee")
    with st.form("add_employee_form", clear_on_submit=True):
        name = st.text_input("Name")
        department = st.text_input("Department")
        salary = st.number_input("Salary", min_value=0.0, step=100.0)
        hire_date = st.date_input("Hire Date", value=date.today())
        submitted = st.form_submit_button("Add")

        if submitted:
            if not name.strip() or not department.strip():
                st.warning("Please fill in name and department.")
            else:
                result, error = create_employee(
                    name.strip(), department.strip(), salary, str(hire_date)
                )
                if error:
                    st.error(f"Failed to add employee: {error}")
                else:
                    st.success(f"Employee added successfully (ID: {result['employee_id']})")

with tab_update:
    st.subheader("Update Employee")
    employees, error = get_employees()

    if error:
        st.error(f"Could not connect to backend: {error}")
    elif not employees:
        st.info("No employees yet.")
    else:
        options = {f"{e['employee_id']} - {e['name']}": e for e in employees}
        selected_label = st.selectbox("Select Employee", list(options.keys()))
        selected_employee = options[selected_label]

        with st.form("update_employee_form"):
            new_name = st.text_input("Name", value=selected_employee["name"])
            new_department = st.text_input("Department", value=selected_employee["department"])
            new_salary = st.number_input(
                "Salary", min_value=0.0, step=100.0, value=float(selected_employee["salary"])
            )
            new_hire_date = st.text_input(
                "Hire Date (YYYY-MM-DD)", value=selected_employee["hire_date"]
            )
            update_submitted = st.form_submit_button("Update")

            if update_submitted:
                result, error = update_employee(
                    selected_employee["employee_id"],
                    new_name.strip(),
                    new_department.strip(),
                    new_salary,
                    new_hire_date.strip(),
                )
                if error:
                    st.error(f"Failed to update employee: {error}")
                else:
                    st.success("Employee updated successfully.")

with tab_delete:
    st.subheader("Delete Employee")
    employees, error = get_employees()

    if error:
        st.error(f"Could not connect to backend: {error}")
    elif not employees:
        st.info("No employees yet.")
    else:
        options = {f"{e['employee_id']} - {e['name']}": e for e in employees}
        selected_label = st.selectbox("Select Employee to Delete", list(options.keys()), key="delete_select")
        selected_employee = options[selected_label]

        st.warning(f"This will delete: {selected_employee['name']} (ID: {selected_employee['employee_id']})")
        if st.button("Confirm Delete", type="primary"):
            result, error = delete_employee(selected_employee["employee_id"])
            if error:
                st.error(f"Failed to delete employee: {error}")
            else:
                st.success("Employee deleted successfully.")
                st.rerun()
