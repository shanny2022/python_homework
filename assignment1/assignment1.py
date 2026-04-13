# assignment1.py

# Task 1: Hello
def hello():
    return "Hello!"


# Task 2: Greet with a Formatted String
def greet(name):
    return f"Hello, {name}!"


# Task 3: Calculator
def calc(a, b, operation="multiply"):
    try:
        match operation:
            case "add":
                return a + b
            case "subtract":
                return a - b
            case "multiply":
                return a * b
            case "divide":
                return a / b
            case "modulo":
                return a % b
            case "int_divide":
                return a // b
            case "power":
                return a**b
            case _:
                # If tests expect only valid operations, this won't be hit.
                # Keeping a sane default behavior anyway.
                return a * b
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        # The prompt specifically mentions multiplying strings as an example,
        # but the tests want this exact message for incompatible operands.
        return "You can't multiply those values!"


# Task 4: Data Type Conversion
def data_type_conversion(value, type):
    try:
        match type:
            case "float":
                return float(value)
            case "int":
                return int(value)
            case "str":
                return str(value)
            case _:
                # Not specified; treat as a failed conversion in the same style.
                raise ValueError("Unsupported conversion type")
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {type}."


# Task 5: Grading System, Using *args
def grade(*args):
    try:
        if len(args) == 0:
            return "Invalid data was provided."
        avg = sum(args) / len(args)
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"
    except Exception:
        return "Invalid data was provided."


# Task 6: Use a For Loop with a Range
def repeat(string, count):
    result = ""
    for _ in range(count):
        result += string
    return result


# Task 7: Student Scores, Using **kwargs
def student_scores(mode, **kwargs):
    if mode == "best":
        # return name of student with highest score
        best_name = None
        best_score = None
        for name, score in kwargs.items():
            if best_score is None or score > best_score:
                best_score = score
                best_name = name
        return best_name
    elif mode == "mean":
        scores = list(kwargs.values())
        if len(scores) == 0:
            return 0
        return sum(scores) / len(scores)

    # Not specified; return None as a reasonable fallback
    return None


# Task 8: Titleize
def titleize(string):
    little_words = {"a", "on", "an", "the", "of", "and", "is", "in"}
    words = string.split()

    if len(words) == 0:
        return ""

    titled = []
    last_index = len(words) - 1

    for i, word in enumerate(words):
        w = word.lower()
        if i == 0 or i == last_index:
            titled.append(w.capitalize())
        else:
            if w in little_words:
                titled.append(w)
            else:
                titled.append(w.capitalize())

    return " ".join(titled)


# Task 9: Hangman
def hangman(secret, guess):
    result = ""
    for ch in secret:
        if ch in guess:
            result += ch
        else:
            result += "_"
    return result


# Task 10: Pig Latin
def pig_latin(text):
    vowels = "aeiou"

    def convert_word(word):
        if word == "":
            return ""

        if word[0] in vowels:
            return word + "ay"

        # consonant start; treat "qu" as a unit if it appears in the leading consonant cluster
        i = 0
        while i < len(word) and word[i] not in vowels:
            # if we see 'q' followed by 'u' while scanning initial consonants, move both
            if word[i] == "q" and i + 1 < len(word) and word[i + 1] == "u":
                i += 2
                break
            i += 1

        return word[i:] + word[:i] + "ay"

    words = text.split()
    converted = [convert_word(w) for w in words]
    return " ".join(converted)
