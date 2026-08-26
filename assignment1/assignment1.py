# Task 1
def hello():
    return "Hello!"


# Task 2
def greet(name):
    return f"Hello, {name}!"


# Task 3
def calc(value1, value2, operation="multiply"):
    try:
        if operation == "add":
            return value1 + value2
        elif operation == "subtract":
            return value1 - value2
        elif operation == "multiply":
            return value1 * value2
        elif operation == "divide":
            return value1 / value2
        elif operation == "modulo":
            return value1 % value2
        elif operation == "int_divide":
            return value1 // value2
        elif operation == "power":
            return value1 ** value2
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return f"You can't {operation} those values!"


# Task 4
def data_type_conversion(value, data_type):
    try:
        if data_type == "float":
            return float(value)
        elif data_type == "str":
            return str(value)
        elif data_type == "int":
            return int(value)
    except ValueError:
        return f"You can't convert {value} into a {data_type}."


# Task 5
def grade(*args):
    try:
        average = sum(args) / len(args)

        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except (TypeError, ZeroDivisionError):
        return "Invalid data was provided."


# Task 6
def repeat(string, count):
    result = ""

    for _ in range(count):
        result += string

    return result


# Task 7
def student_scores(option, **kwargs):
    if option == "best":
        return max(kwargs, key=kwargs.get)
    elif option == "mean":
        return sum(kwargs.values()) / len(kwargs)


# Task 8
def titleize(title):
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    words = title.split()
    new_words = []

    for index, word in enumerate(words):
        if index == 0 or index == len(words) - 1:
            new_words.append(word.capitalize())
        elif word.lower() in little_words:
            new_words.append(word.lower())
        else:
            new_words.append(word.capitalize())

    return " ".join(new_words)


# Task 9
def hangman(secret, guess):
    result = ""

    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"

    return result


# Task 10
def pig_latin(sentence):
    vowels = "aeiou"
    translated_words = []

    for word in sentence.split():
        if word[0] in vowels:
            translated_words.append(word + "ay")
            continue

        consonants = ""
        index = 0

        while index < len(word) and word[index] not in vowels:
            if word[index:index + 2] == "qu":
                consonants += "qu"
                index += 2
                break

            consonants += word[index]
            index += 1

        translated_words.append(word[index:] + consonants + "ay")

    return " ".join(translated_words)

print(hello())
print(greet("Shuntoria"))
print(calc(5, 2, "add"))
print(data_type_conversion("10", "int"))
print(grade(90, 80, 100))
print(repeat("hi", 3))
print(student_scores("best", Shuntoria=95, John=80))
print(titleize("the lord of the rings"))
print(hangman("alphabet", "ab"))
print(pig_latin("the quick dog"))
