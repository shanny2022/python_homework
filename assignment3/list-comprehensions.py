# Task 3: List comprehensions practice

import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "csv", "employees.csv")


def read_employee_rows():
    rows = []

    with open(CSV_PATH, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    return rows


if __name__ == "__main__":
    employee_rows = read_employee_rows()

    headings = employee_rows[0]
    first_name_column = headings.index("first_name")
    last_name_column = headings.index("last_name")

    employee_names = [
        f"{row[first_name_column]} {row[last_name_column]}"
        for row in employee_rows[1:]
    ]

    print(employee_names)

    names_with_e = [
        name
        for name in employee_names
        if "e" in name.lower()
    ]

    print(names_with_e)
