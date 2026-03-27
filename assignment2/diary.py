import traceback


try:
    first_prompt = True
    with open("diary.txt", "a", encoding="utf-8") as diary_file:
        while True:
            prompt = "What happened today? " if first_prompt else "What else? "
            line = input(prompt)
            diary_file.write(f"{line}\n")

            if line == "done for now":
                break

            first_prompt = False
except Exception as e:
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
