import csv
import os
import traceback
import custom_module
from datetime import datetime

def print_exception(e):
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = []

    for trace in trace_back:
        stack_trace.append(
            f"File : {trace[0]} , "
            f"Line : {trace[1]}, "
            f"Func.Name : {trace[2]}, "
            f"Message : {trace[3]}"
        )

    print(f"Exception type: {type(e).__name__}")

    message = str(e)

    if message:
        print(f"Exception message: {message}")

    print(f"Stack trace: {stack_trace}")

    # Task 2: Read employees.csv

def read_employees():
    employee_data = {
        "fields": [],
        "rows": []
    }

    try:
        with open("../csv/employees.csv", "r") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    employee_data["fields"] = row
                else:
                    employee_data["rows"].append(row)

    except Exception as e:
        print_exception(e)

    return employee_data


employees = read_employees()
print(employees)


# Task 3: Find a column index

def column_index(column_name):
    return employees["fields"].index(column_name)


employee_id_column = column_index("employee_id")

# Task 4: Find an employee first name

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


sort_by_last_name()
print(employees)

# Task 8: Create an employee dictionary

def employee_dict(row):
    result = {}

    for index, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[index]

    return result


print(employee_dict(employees["rows"][0]))

# Task 9: Create a dictionary of all employees

def all_employees_dict():
    all_employees = {}

    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        all_employees[employee_id] = employee_dict(row)

    return all_employees


print(all_employees_dict())

# Task 10: Read an environment variable

def get_this_value():
    return os.getenv("THISVALUE")

# Task 11: Use a custom module

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


set_that_secret("python is powerful")
print(custom_module.secret)

# Task 12: Read minutes CSV files

def read_minutes_file(file_path):
    minutes_data = {
        "fields": [],
        "rows": []
    }

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    minutes_data["fields"] = row
                else:
                    minutes_data["rows"].append(tuple(row))

    except Exception as e:
        print_exception(e)

    return minutes_data


def read_minutes():
    minutes1_data = read_minutes_file("../csv/minutes1.csv")
    minutes2_data = read_minutes_file("../csv/minutes2.csv")

    return minutes1_data, minutes2_data


minutes1, minutes2 = read_minutes()

print(minutes1)
print(minutes2)

# Task 13: Create a set of unique minutes

def create_minutes_set():
    minutes1_set = set(minutes1["rows"])
    minutes2_set = set(minutes2["rows"])

    return minutes1_set.union(minutes2_set)


minutes_set = create_minutes_set()
print(minutes_set)

# Task 14: Convert dates to datetime objects

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
print(minutes_list)

# Task 15: Write the sorted minutes list

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

    with open("minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(minutes1["fields"])
        writer.writerows(converted_list)

    return converted_list


print(write_sorted_list())
