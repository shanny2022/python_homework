"""Task 2: Decorator that converts function output type."""

# Task 2
from functools import wraps


def type_converter(type_of_output):
    """Decorator factory that converts wrapped function return value."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = func(*args, **kwargs)
            return type_of_output(x)

        return wrapper

    return decorator


@type_converter(str)
def return_int():
    return 5


@type_converter(int)
def return_string():
    return "not a number"


if __name__ == "__main__":
    y = return_int()
    print(type(y).__name__)  # This should print "str"
    try:
        y = return_string()
        print("shouldn't get here!")
    except ValueError:
        print("can't convert that string to an integer!")
