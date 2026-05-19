import csv
import os
import traceback
from datetime import datetime

import custom_module


def _print_exception_and_exit(e):
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = []
    for trace in trace_back:
        stack_trace.append(
            f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}"
        )
    print("An exception occurred.")
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")
    raise SystemExit(1)


# Task 2

def read_employees():
    employees_data = {}
    rows = []
    try:
        with open("../csv/employees.csv", "r", newline="", encoding="utf-8") as employee_file:
            reader = csv.reader(employee_file)
            for row_index, row in enumerate(reader):
                if row_index == 0:
                    employees_data["fields"] = row
                else:
                    rows.append(row)
            employees_data["rows"] = rows
            return employees_data
    except Exception as e:
        _print_exception_and_exit(e)


employees = read_employees()


# Task 3

def column_index(column_name):
    return employees["fields"].index(column_name)


employee_id_column = column_index("employee_id")


# Task 4

def first_name(row_number):
    first_name_column = column_index("first_name")
    return employees["rows"][row_number][first_name_column]


# Task 5

def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6

def employee_find_2(employee_id):
    matches = list(
        filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"])
    )
    return matches


# Task 7

def sort_by_last_name():
    last_name_column = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_column])
    return employees["rows"]


# Task 8

def employee_dict(row):
    result = {}
    for index, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[index]
    return result


# Task 9

def all_employees_dict():
    result = {}
    for row in employees["rows"]:
        result[row[employee_id_column]] = employee_dict(row)
    return result


# Task 10

def get_this_value():
    return os.getenv("THISVALUE")


# Task 11

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


# Task 12

def _read_csv_as_dict(path, row_converter=None):
    data = {}
    rows = []
    with open(path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row_index, row in enumerate(reader):
            if row_index == 0:
                data["fields"] = row
            else:
                rows.append(row_converter(row) if row_converter else row)
    data["rows"] = rows
    return data


def read_minutes():
    try:
        minutes_1 = _read_csv_as_dict("../csv/minutes1.csv", row_converter=tuple)
        minutes_2 = _read_csv_as_dict("../csv/minutes2.csv", row_converter=tuple)
        return minutes_1, minutes_2
    except Exception as e:
        _print_exception_and_exit(e)


minutes1, minutes2 = read_minutes()


# Task 13

def create_minutes_set():
    return set(minutes1["rows"]).union(set(minutes2["rows"]))


minutes_set = create_minutes_set()


# Task 14

def create_minutes_list():
    minutes_rows_list = list(minutes_set)
    converted = list(
        map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_rows_list)
    )
    return converted


minutes_list = create_minutes_list()


# Task 15

def write_sorted_list():
    minutes_list.sort(key=lambda x: x[1])
    converted = list(
        map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list)
    )

    with open("./minutes.csv", "w", newline="", encoding="utf-8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(minutes1["fields"])
        writer.writerows(converted)

    return converted


# Program calls for verification (as requested by assignment steps)
sorted_rows = sort_by_last_name()
example_employee = employee_dict(employees["rows"][0])
all_employees = all_employees_dict()
set_that_secret("open-sesame")
sorted_minutes = write_sorted_list()
