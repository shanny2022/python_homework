# Task 1: Diary

import traceback

try:
    with open("diary.txt", "a") as diary_file:
        first_entry = True

        while True:
            if first_entry:
                entry = input("What happened today? ")
                first_entry = False
            else:
                entry = input("What else? ")

            diary_file.write(entry + "\n")

            if entry == "done for now":
                break

except Exception as e:
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
