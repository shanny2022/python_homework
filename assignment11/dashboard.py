"""Streamlit capstone dashboard for Assignment 11.

Run with:
    streamlit run dashboard.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


def load_employee_data() -> pd.DataFrame:
    data = [
        {"employee": "Aaliyah Johnson", "department": "Engineering", "hours": 41.5, "gross_pay": 1969.13},
        {"employee": "Marcus Lee", "department": "Design", "hours": 38.0, "gross_pay": 1491.50},
        {"employee": "Priya Shah", "department": "Data", "hours": 45.0, "gross_pay": 1995.00},
        {"employee": "Elena Garcia", "department": "Support", "hours": 36.5, "gross_pay": 1049.38},
        {"employee": "Jordan Smith", "department": "Engineering", "hours": 40.0, "gross_pay": 1420.00},
    ]
    return pd.DataFrame(data)


def main() -> None:
    st.set_page_config(page_title="Capstone Workforce Dashboard", layout="wide")

    employees = load_employee_data()
    departments = ["All"] + sorted(employees["department"].unique())

    st.title("Capstone Workforce Dashboard")
    selected_department = st.sidebar.selectbox("Department", departments)

    if selected_department != "All":
        employees = employees[employees["department"] == selected_department]

    total_payroll = employees["gross_pay"].sum()
    average_hours = employees["hours"].mean()
    overtime_count = int((employees["hours"] > 40).sum())

    metric_columns = st.columns(3)
    metric_columns[0].metric("Total Payroll", f"${total_payroll:,.2f}")
    metric_columns[1].metric("Average Hours", f"{average_hours:.1f}")
    metric_columns[2].metric("Overtime Employees", overtime_count)

    chart_columns = st.columns(2)
    chart_columns[0].subheader("Payroll by Employee")
    chart_columns[0].bar_chart(
        employees.set_index("employee")["gross_pay"],
        color="#1f77b4",
    )

    chart_columns[1].subheader("Hours by Employee")
    chart_columns[1].bar_chart(
        employees.set_index("employee")["hours"],
        color="#ff7f0e",
    )

    st.subheader("Employee Details")
    st.dataframe(
        employees.sort_values("gross_pay", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
