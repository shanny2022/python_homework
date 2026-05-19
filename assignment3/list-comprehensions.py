"""Task 3: List comprehensions with CSV data."""

# Task 3
import csv


if __name__ == "__main__":
    with open("../csv/employees.csv", "r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.reader(csv_file))

    names = [f"{row[1]} {row[2]}" for row in rows[1:]]
    print(names)

    names_with_e = [name for name in names if "e" in name.lower()]
    print(names_with_e)
