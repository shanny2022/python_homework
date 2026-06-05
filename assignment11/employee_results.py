"""Employee analysis for Assignment 11.

Run with:
    python employee_results.py
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Employee:
    name: str
    department: str
    role: str
    hourly_rate: float
    hours_worked: float

    @property
    def gross_pay(self) -> float:
        overtime_hours = max(self.hours_worked - 40, 0)
        regular_hours = min(self.hours_worked, 40)
        return (regular_hours * self.hourly_rate) + (overtime_hours * self.hourly_rate * 1.5)


EMPLOYEES = [
    Employee("Aaliyah Johnson", "Engineering", "Backend Developer", 44.50, 41.5),
    Employee("Marcus Lee", "Design", "UX Designer", 39.25, 38),
    Employee("Priya Shah", "Data", "Data Analyst", 42.00, 45),
    Employee("Elena Garcia", "Support", "Customer Advocate", 28.75, 36.5),
    Employee("Jordan Smith", "Engineering", "QA Engineer", 35.50, 40),
]


def summarize_employees(employees: list[Employee]) -> dict[str, float | str]:
    """Return high-level payroll metrics for a list of employees."""
    total_payroll = sum(employee.gross_pay for employee in employees)
    highest_paid = max(employees, key=lambda employee: employee.gross_pay)
    average_hours = sum(employee.hours_worked for employee in employees) / len(employees)
    overtime_count = sum(employee.hours_worked > 40 for employee in employees)

    return {
        "employee_count": len(employees),
        "total_payroll": round(total_payroll, 2),
        "average_hours": round(average_hours, 2),
        "overtime_count": overtime_count,
        "highest_paid_employee": highest_paid.name,
        "highest_paid_amount": round(highest_paid.gross_pay, 2),
    }


def write_results_csv(employees: list[Employee], output_path: Path) -> None:
    """Write employee pay details to a CSV file."""
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "name",
                "department",
                "role",
                "hourly_rate",
                "hours_worked",
                "gross_pay",
            ],
        )
        writer.writeheader()
        for employee in employees:
            writer.writerow(
                {
                    "name": employee.name,
                    "department": employee.department,
                    "role": employee.role,
                    "hourly_rate": employee.hourly_rate,
                    "hours_worked": employee.hours_worked,
                    "gross_pay": round(employee.gross_pay, 2),
                }
            )


def main() -> None:
    output_path = Path(__file__).with_name("employee_results.csv")
    write_results_csv(EMPLOYEES, output_path)

    summary = summarize_employees(EMPLOYEES)
    print("Employee Payroll Summary")
    print("------------------------")
    for key, value in summary.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print(f"\nDetailed CSV written to: {output_path}")


if __name__ == "__main__":
    main()
