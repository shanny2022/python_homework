"""Task 1: Decorator logging function calls to decorator.log."""

# Task 1
import logging
from functools import wraps


logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log", "a"))


def logger_decorator(func):
    """Log function name, positional/keyword parameters, and return value."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        positional = list(args) if args else "none"
        keyword = kwargs if kwargs else "none"

        logger.log(logging.INFO, f"function: {func.__name__}")
        logger.log(logging.INFO, f"positional parameters: {positional}")
        logger.log(logging.INFO, f"keyword parameters: {keyword}")
        logger.log(logging.INFO, f"return: {value}")

        return value

    return wrapper


@logger_decorator
def say_hello():
    """Function with no parameters and no return value."""
    print("Hello, World!")


@logger_decorator
def always_true(*args):
    """Function with variable positional arguments."""
    _ = args
    return True


@logger_decorator
def return_decorator(**kwargs):
    """Function with variable keyword arguments."""
    _ = kwargs
    return logger_decorator


if __name__ == "__main__":
    say_hello()
    always_true(1, "abc", 3.14)
    return_decorator(first="alpha", second=2, third=True)
    print("Check decorator.log for call details.")
