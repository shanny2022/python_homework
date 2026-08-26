# Task 1: Writing and testing a decorator

import logging
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "decorator.log")

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers if the file is executed more than once
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_PATH, "a")
    logger.addHandler(file_handler)


def logger_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        positional_parameters = list(args) if args else "none"
        keyword_parameters = kwargs if kwargs else "none"

        logger.log(logging.INFO, f"function: {func.__name__}")
        logger.log(
            logging.INFO,
            f"positional parameters: {positional_parameters}"
        )
        logger.log(
            logging.INFO,
            f"keyword parameters: {keyword_parameters}"
        )
        logger.log(logging.INFO, f"return: {result}")

        return result

    return wrapper


@logger_decorator
def say_hello():
    print("Hello, World!")


@logger_decorator
def positional_function(*args):
    print(f"Positional arguments: {args}")
    return True


@logger_decorator
def keyword_function(**kwargs):
    print(f"Keyword arguments: {kwargs}")
    return logger_decorator


if __name__ == "__main__":
    say_hello()
    positional_function(1, 2, 3, "Python")
    keyword_function(name="Shuntoria", course="Python")
