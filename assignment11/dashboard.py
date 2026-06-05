"""Streamlit dashboard for Assignment 11 revenue analysis.

Run from the repository root with:
    streamlit run assignment11/dashboard.py
"""

from pathlib import Path
import sqlite3

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


<<<<<<< HEAD
DB_PATH = Path(__file__).resolve().parent.parent / "db" / "lesson.db"


@st.cache_data
def load_order_lines(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Load employee, order, line item, and product data from SQLite."""
    query = """
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            e.first_name || ' ' || e.last_name AS employee_name,
            o.order_id,
            li.line_item_id,
            li.quantity,
            p.product_id,
            p.product_name,
            p.price,
            li.quantity * p.price AS line_revenue
        FROM employees AS e
        JOIN orders AS o
            ON e.employee_id = o.employee_id
        JOIN line_items AS li
            ON o.order_id = li.order_id
        JOIN products AS p
            ON li.product_id = p.product_id
        ORDER BY o.order_id, li.line_item_id
    """

    if not db_path.exists():
        st.error(f"Database not found at {db_path}")
        st.stop()

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


def summarize_by_employee(order_lines: pd.DataFrame) -> pd.DataFrame:
    """Return total revenue and order activity by employee."""
    return (
        order_lines.groupby(["employee_id", "employee_name", "last_name"], as_index=False)
        .agg(
            total_revenue=("line_revenue", "sum"),
            order_count=("order_id", "nunique"),
            line_items=("line_item_id", "count"),
        )
        .sort_values("total_revenue", ascending=False)
    )


def summarize_by_order(order_lines: pd.DataFrame) -> pd.DataFrame:
    """Return order totals with a cumulative revenue column."""
    order_totals = (
        order_lines.groupby("order_id", as_index=False)["line_revenue"]
        .sum()
        .rename(columns={"line_revenue": "total_price"})
        .sort_values("order_id")
    )
    order_totals["cumulative_revenue"] = order_totals["total_price"].cumsum()
    return order_totals


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def main() -> None:
    st.set_page_config(page_title="Assignment 11 Revenue Dashboard", layout="wide")

    order_lines = load_order_lines()
    employee_summary = summarize_by_employee(order_lines)
    order_summary = summarize_by_order(order_lines)

    st.title("Assignment 11 Revenue Dashboard")
    st.caption("SQLite, Pandas, Plotly, and Streamlit dashboard for employee and order revenue.")

    employees = ["All employees"] + employee_summary["employee_name"].sort_values().tolist()
    selected_employee = st.sidebar.selectbox("Employee", employees)

    min_order, max_order = int(order_summary["order_id"].min()), int(order_summary["order_id"].max())
    order_range = st.sidebar.slider("Order ID range", min_order, max_order, (min_order, max_order))

    filtered_lines = order_lines[
        order_lines["order_id"].between(order_range[0], order_range[1])
    ].copy()
    if selected_employee != "All employees":
        filtered_lines = filtered_lines[filtered_lines["employee_name"] == selected_employee]

    filtered_employee_summary = summarize_by_employee(filtered_lines)
    filtered_order_summary = summarize_by_order(filtered_lines)

    total_revenue = filtered_lines["line_revenue"].sum()
    total_orders = filtered_lines["order_id"].nunique()
    average_order = filtered_order_summary["total_price"].mean() if not filtered_order_summary.empty else 0
    top_employee = (
        filtered_employee_summary.iloc[0]["employee_name"]
        if not filtered_employee_summary.empty
        else "No data"
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Total revenue", format_currency(total_revenue))
    metric_columns[1].metric("Orders", f"{total_orders:,}")
    metric_columns[2].metric("Average order", format_currency(average_order))
    metric_columns[3].metric("Top employee", top_employee)

    chart_columns = st.columns((1.1, 1))
    with chart_columns[0]:
        st.subheader("Revenue by employee")
        employee_chart = px.bar(
            filtered_employee_summary,
            x="last_name",
            y="total_revenue",
            color="employee_name",
            hover_data=["order_count", "line_items"],
            labels={
                "last_name": "Employee last name",
                "total_revenue": "Total revenue",
                "employee_name": "Employee",
            },
        )
        employee_chart.update_layout(showlegend=False)
        st.plotly_chart(employee_chart, use_container_width=True)

    with chart_columns[1]:
        st.subheader("Cumulative revenue")
        cumulative_chart = px.line(
            filtered_order_summary,
            x="order_id",
            y="cumulative_revenue",
            markers=True,
            labels={
                "order_id": "Order ID",
                "cumulative_revenue": "Cumulative revenue",
            },
        )
        st.plotly_chart(cumulative_chart, use_container_width=True)

    st.subheader("Employee revenue table")
    display_summary = filtered_employee_summary.copy()
    display_summary["total_revenue"] = display_summary["total_revenue"].map(format_currency)
    st.dataframe(
        display_summary[["employee_name", "last_name", "order_count", "line_items", "total_revenue"]],
        use_container_width=True,
=======
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
>>>>>>> c6d439aa2654e712c952e19501ef5dccf874b7e3
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

    st.subheader("Order detail")
    display_orders = filtered_order_summary.copy()
    display_orders["total_price"] = display_orders["total_price"].map(format_currency)
    display_orders["cumulative_revenue"] = display_orders["cumulative_revenue"].map(format_currency)
    st.dataframe(display_orders, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
