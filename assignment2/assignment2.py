import csv
import os
import traceback
from datetime import datetime

try:
    import custom_module
except ModuleNotFoundError:
    from . import custom_module


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "..", "csv")


def print_exception(exception):
    trace_back = traceback.extract_tb(exception.__traceback__)
    stack_trace = []

    for trace in trace_back:
        stack_trace.append(
            f"File : {trace[0]} , "
            f"Line : {trace[1]}, "
            f"Func.Name : {trace[2]}, "
            f"Message : {trace[3]}"
        )

    print(f"Exception type: {type(exception).__name__}")

    message = str(exception)

    if message:
        print(f"Exception message: {message}")

    print(f"Stack trace: {stack_trace}")


# Task 2: Read employees.csv

def read_employees():
    employee_data = {
        "fields": [],
        "rows": []
    }

    employees_path = os.path.join(CSV_DIR, "employees.csv")

    try:
        with open(employees_path, "r", newline="") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    employee_data["fields"] = row
                else:
                    employee_data["rows"].append(row)

    except Exception as exception:
        print_exception(exception)
        raise

    return employee_data


employees = read_employees()


# Task 3: Find a column index

def column_index(column_name):
    return employees["fields"].index(column_name)


employee_id_column = column_index("employee_id")


# Task 4: Find an employee's first name

def first_name(row_number):
    first_name_column = column_index("first_name")
    return employees["rows"][row_number][first_name_column]


# Task 5: Find an employee using an inner function

def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(
        filter(employee_match, employees["rows"])
    )

    return matches


# Task 6: Find an employee using a lambda

def employee_find_2(employee_id):
    matches = list(
        filter(
            lambda row: int(row[employee_id_column]) == employee_id,
            employees["rows"]
        )
    )

    return matches


# Task 7: Sort employees by last name

def sort_by_last_name():
    last_name_column = column_index("last_name")

    employees["rows"].sort(
        key=lambda row: row[last_name_column]
    )

    return employees["rows"]


# Task 8: Create a dictionary for one employee

def employee_dict(row):
    result = {}

    for index, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[index]

    return result


# Task 9: Create a dictionary containing all employees

def all_employees_dict():
    all_employees = {}

    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        all_employees[employee_id] = employee_dict(row)

    return all_employees


# Task 10: Read an environment variable

def get_this_value():
    return os.getenv("THISVALUE")


# Task 11: Use a custom module

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


# Task 12: Read minutes1.csv and minutes2.csv

def read_minutes_file(file_path):
    minutes_data = {
        "fields": [],
        "rows": []
    }

    try:
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    minutes_data["fields"] = row
                else:
                    minutes_data["rows"].append(tuple(row))

    except Exception as exception:
        print_exception(exception)
        raise

    return minutes_data


def read_minutes():
    minutes1_path = os.path.join(CSV_DIR, "minutes1.csv")
    minutes2_path = os.path.join(CSV_DIR, "minutes2.csv")

    minutes1_data = read_minutes_file(minutes1_path)
    minutes2_data = read_minutes_file(minutes2_path)

    return minutes1_data, minutes2_data


minutes1, minutes2 = read_minutes()


# Task 13: Create one set of unique minutes

def create_minutes_set():
    minutes1_set = set(minutes1["rows"])
    minutes2_set = set(minutes2["rows"])

    return minutes1_set.union(minutes2_set)


minutes_set = create_minutes_set()


# Task 14: Convert date strings to datetime objects

def create_minutes_list():
    minutes_rows = list(minutes_set)

    converted_minutes = list(
        map(
            lambda row: (
                row[0],
                datetime.strptime(row[1], "%B %d, %Y")
            ),
            minutes_rows
        )
    )

    return converted_minutes


minutes_list = create_minutes_list()


# Task 15: Sort and write minutes.csv

def write_sorted_list():
    minutes_list.sort(key=lambda row: row[1])

    converted_list = list(
        map(
            lambda row: (
                row[0],
                datetime.strftime(row[1], "%B %d, %Y")
            ),
            minutes_list
        )
    )

    minutes_output_path = os.path.join(BASE_DIR, "minutes.csv")

    try:
        with open(minutes_output_path, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(minutes1["fields"])
            writer.writerows(converted_list)

    except Exception as exception:
        print_exception(exception)
        raise

    return converted_list


if __name__ == "__main__":
    sort_by_last_name()
    set_that_secret("python is powerful")

    print(employees)
    print(employee_dict(employees["rows"][0]))
    print(all_employees_dict())
    print(custom_module.secret)
    print(minutes1)
    print(minutes2)
    print(minutes_set)
    print(minutes_list)
    print(write_sorted_list())
