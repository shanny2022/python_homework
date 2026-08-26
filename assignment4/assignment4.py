import os

import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Task 1: Create and manipulate DataFrames

task1_data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}

task1_data_frame = pd.DataFrame(task1_data)

task1_with_salary = task1_data_frame.copy()
task1_with_salary["Salary"] = [
    70000,
    80000,
    90000
]

task1_older = task1_with_salary.copy()
task1_older["Age"] = task1_older["Age"] + 1

employees_csv_path = os.path.join(
    BASE_DIR,
    "employees.csv"
)

task1_older.to_csv(
    employees_csv_path,
    index=False
)


# Task 2: Load data from CSV and JSON

task2_employees = pd.read_csv(
    employees_csv_path
)

additional_employees_path = os.path.join(
    BASE_DIR,
    "additional_employees.json"
)

json_employees = pd.read_json(
    additional_employees_path
)

more_employees = pd.concat(
    [task2_employees, json_employees],
    ignore_index=True
)


# Task 3: Inspect the DataFrame

first_three = more_employees.head(3)

last_two = more_employees.tail(2)

employee_shape = more_employees.shape


# Task 4: Clean dirty data

dirty_data_path = os.path.join(
    BASE_DIR,
    "dirty_data.csv"
)

dirty_data = pd.read_csv(
    dirty_data_path
)

clean_data = dirty_data.copy()

clean_data = clean_data.drop_duplicates()
clean_data = clean_data.reset_index(drop=True)

clean_data["Age"] = pd.to_numeric(
    clean_data["Age"],
    errors="coerce"
)

clean_data["Salary"] = clean_data["Salary"].replace(
    ["unknown", "n/a"],
    pd.NA
)

clean_data["Salary"] = pd.to_numeric(
    clean_data["Salary"],
    errors="coerce"
)

age_mean = clean_data["Age"].mean()

clean_data["Age"] = clean_data["Age"].fillna(
    age_mean
)

salary_median = clean_data["Salary"].median()

clean_data["Salary"] = clean_data["Salary"].fillna(
    salary_median
)

clean_data["Hire Date"] = pd.to_datetime(
    clean_data["Hire Date"],
    format="mixed",
    errors="coerce"
)

clean_data["Name"] = (
    clean_data["Name"]
    .str.strip()
    .str.upper()
)

clean_data["Department"] = (
    clean_data["Department"]
    .str.strip()
    .str.upper()
)


if __name__ == "__main__":
    print("Task 1 DataFrame:")
    print(task1_data_frame)

    print("\nTask 1 with salary:")
    print(task1_with_salary)

    print("\nTask 1 with older ages:")
    print(task1_older)

    print("\nEmployees loaded from CSV:")
    print(task2_employees)

    print("\nEmployees loaded from JSON:")
    print(json_employees)

    print("\nCombined employees:")
    print(more_employees)

    print("\nFirst three employees:")
    print(first_three)

    print("\nLast two employees:")
    print(last_two)

    print("\nEmployee shape:")
    print(employee_shape)

    print("\nEmployee information:")
    more_employees.info()

    print("\nOriginal dirty data:")
    print(dirty_data)

    print("\nCleaned data:")
    print(clean_data)

    print("\nCleaned data information:")
    clean_data.info()
