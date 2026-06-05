"""Streamlit capstone dashboard for Assignment 11.

Run from the repository root with:
    streamlit run assignment11/dashboard.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).with_name("employee_results.csv")


@st.cache_data
def load_employee_data() -> pd.DataFrame:
    """Load employee payroll results created by employee_results.py."""
    employees = pd.read_csv(DATA_PATH)
    employees["overtime_hours"] = (employees["hours_worked"] - 40).clip(lower=0)
    employees["regular_hours"] = employees["hours_worked"] - employees["overtime_hours"]
    employees["pay_per_hour_worked"] = employees["gross_pay"] / employees["hours_worked"]
    return employees


def main() -> None:
    st.set_page_config(
        page_title="Capstone Workforce Dashboard",
        layout="wide",
    )

    employees = load_employee_data()
    departments = sorted(employees["department"].unique())
    selected_departments = st.sidebar.multiselect(
        "Departments",
        departments,
        default=departments,
    )
    hour_range = st.sidebar.slider(
        "Hours worked",
        min_value=float(employees["hours_worked"].min()),
        max_value=float(employees["hours_worked"].max()),
        value=(
            float(employees["hours_worked"].min()),
            float(employees["hours_worked"].max()),
        ),
        step=0.5,
    )

    filtered_employees = employees[
        employees["department"].isin(selected_departments)
        & employees["hours_worked"].between(hour_range[0], hour_range[1])
    ]

    st.title("Capstone Workforce Dashboard")
    st.caption("Payroll, hours, and overtime insights from the Assignment 11 employee analysis.")

    if filtered_employees.empty:
        st.warning("No employees match the selected filters.")
        return

    total_payroll = filtered_employees["gross_pay"].sum()
    average_hours = filtered_employees["hours_worked"].mean()
    overtime_count = int((filtered_employees["overtime_hours"] > 0).sum())
    average_rate = filtered_employees["hourly_rate"].mean()

    metric_columns = st.columns(4)
    metric_columns[0].metric("Total Payroll", f"${total_payroll:,.2f}")
    metric_columns[1].metric("Average Hours", f"{average_hours:.1f}")
    metric_columns[2].metric("Overtime Employees", overtime_count)
    metric_columns[3].metric("Average Hourly Rate", f"${average_rate:,.2f}")

    department_summary = (
        filtered_employees.groupby("department", as_index=False)
        .agg(
            employees=("name", "count"),
            total_payroll=("gross_pay", "sum"),
            average_hours=("hours_worked", "mean"),
            overtime_hours=("overtime_hours", "sum"),
        )
        .sort_values("total_payroll", ascending=False)
    )

    chart_columns = st.columns(2)
    chart_columns[0].subheader("Payroll by Employee")
    chart_columns[0].plotly_chart(
        px.bar(
            filtered_employees.sort_values("gross_pay", ascending=True),
            x="gross_pay",
            y="name",
            color="department",
            orientation="h",
            labels={"gross_pay": "Gross pay", "name": "Employee"},
        ),
        width="stretch",
    )

    chart_columns[1].subheader("Payroll by Department")
    chart_columns[1].plotly_chart(
        px.pie(
            department_summary,
            names="department",
            values="total_payroll",
            hole=0.45,
        ),
        width="stretch",
    )

    st.subheader("Hours and Overtime")
    st.plotly_chart(
        px.bar(
            filtered_employees,
            x="name",
            y=["regular_hours", "overtime_hours"],
            labels={"value": "Hours", "name": "Employee", "variable": "Hour type"},
            barmode="stack",
        ),
        width="stretch",
    )

    table_columns = [
        "name",
        "department",
        "role",
        "hourly_rate",
        "hours_worked",
        "overtime_hours",
        "gross_pay",
        "pay_per_hour_worked",
    ]

    st.subheader("Employee Details")
    st.dataframe(
        filtered_employees.sort_values("gross_pay", ascending=False)[table_columns],
        width="stretch",
        hide_index=True,
        column_config={
            "name": "Employee",
            "department": "Department",
            "role": "Role",
            "hourly_rate": st.column_config.NumberColumn("Hourly Rate", format="$%.2f"),
            "hours_worked": st.column_config.NumberColumn("Hours Worked", format="%.1f"),
            "overtime_hours": st.column_config.NumberColumn("Overtime Hours", format="%.1f"),
            "gross_pay": st.column_config.NumberColumn("Gross Pay", format="$%.2f"),
            "pay_per_hour_worked": st.column_config.NumberColumn(
                "Pay per Hour Worked",
                format="$%.2f",
            ),
        },
    )

    st.download_button(
        "Download filtered CSV",
        filtered_employees[table_columns].to_csv(index=False),
        file_name="filtered_employee_results.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
