import pandas as pd
import json
import os

# Task 1: Introduction to Pandas - Creating and Manipulating DataFrames

# Create a DataFrame from a dictionary
task1_data_frame = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
})

print("Task 1 - Created DataFrame:")
print(task1_data_frame)

# Add a new column called Salary
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]

print("\nTask 1 - DataFrame with Salary column:")
print(task1_with_salary)

# Modify the Age column by incrementing by 1
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1

print("\nTask 1 - DataFrame with incremented Age:")
print(task1_older)

# Save to CSV file without index
task1_older.to_csv('employees.csv', index=False)
print("\nTask 1 - Saved to employees.csv")
print(pd.read_csv('employees.csv'))


# Task 2: Loading Data from CSV and JSON

# Read data from the CSV file we just created
task2_employees = pd.read_csv('employees.csv')

print("\nTask 2 - Read from employees.csv:")
print(task2_employees)

# Create a JSON file with additional employees
additional_employees = [
    {
        'Name': 'Eve',
        'Age': 28,
        'City': 'Miami',
        'Salary': 60000
    },
    {
        'Name': 'Frank',
        'Age': 40,
        'City': 'Seattle',
        'Salary': 95000
    }
]

with open('additional_employees.json', 'w') as f:
    json.dump(additional_employees, f)

print("\nTask 2 - Created additional_employees.json")

# Load from JSON file
json_employees = pd.read_json('additional_employees.json')

print("\nTask 2 - Read from additional_employees.json:")
print(json_employees)

# Combine the DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

print("\nTask 2 - Combined DataFrames:")
print(more_employees)


# Task 3: Data Inspection - Using Head, Tail, and Info Methods

# Get first three rows
first_three = more_employees.head(3)

print("\nTask 3 - First three rows:")
print(first_three)

# Get last two rows
last_two = more_employees.tail(2)

print("\nTask 3 - Last two rows:")
print(last_two)

# Get the shape
employee_shape = more_employees.shape

print(f"\nTask 3 - Shape of more_employees: {employee_shape}")

# Print info about the DataFrame
print("\nTask 3 - DataFrame Info:")
more_employees.info()


# Task 4: Data Cleaning

# Read the dirty data CSV
dirty_data = pd.read_csv('dirty_data.csv')

print("\nTask 4 - Dirty data:")
print(dirty_data)

# Create a copy for cleaning
clean_data = dirty_data.copy()

# Remove duplicate rows
clean_data.drop_duplicates(inplace=True)
print("\nTask 4 - After removing duplicates:")
print(clean_data)

# Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("\nTask 4 - After converting Age to numeric:")
print(clean_data)

# Convert Salary to numeric and replace known placeholders
clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a'], pd.NA)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
print("\nTask 4 - After converting Salary to numeric:")
print(clean_data)

# Fill missing values: Age with mean, Salary with median
clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print("\nTask 4 - After filling missing values:")
print(clean_data)

# Convert Hire Date to datetime
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce', format='mixed')
print("\nTask 4 - After converting Hire Date to datetime:")
print(clean_data)

# Strip whitespace and standardize Name and Department
clean_data['Name'] = clean_data['Name'].str.strip()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("\nTask 4 - After stripping whitespace and standardizing:")
print(clean_data)

print("\nAssignment 4 completed!")
