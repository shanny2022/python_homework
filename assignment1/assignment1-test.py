import assignment1 as a1

def test_hello():
    assert a1.hello() == "Hello!" # type: ignore

def test_greet():
    assert a1.greet("James") == "Hello, James!" # type: ignore

def test_calc():
    assert a1.calc(5,6) == 30 # type: ignore
    assert a1.calc(5,6,"add") == 11 # type: ignore
    assert a1.calc(20,5,"divide") == 4 # type: ignore
    assert a1.calc(14,2.0,"multiply") == 28.0 # type: ignore
    assert a1.calc(12.6, 4.4, "subtract") == 8.2 # type: ignore
    assert a1.calc(9,5, "modulo") == 4 # type: ignore
    assert a1.calc(10,0,"divide") == "You can't divide by 0!" # type: ignore
    assert a1.calc("first", "second", "multiply") == "You can't multiply those values!" # type: ignore

def test_data_type_conversion():
    result = a1.data_type_conversion("110", "int") # type: ignore
    assert type(result).__name__ == "int"
    assert result == 110
    result = a1.data_type_conversion("5.5", "float") # type: ignore
    assert type(result).__name__ == "float"
    assert result == 5.5
    result = a1.data_type_conversion(7,"float") # type: ignore
    assert type(result).__name__ == "float"
    assert result == 7.0
    result = a1.data_type_conversion(91.1,"str") # type: ignore
    assert type(result).__name__ == "str"
    assert result == "91.1"
    assert a1.data_type_conversion("banana", "int") == "You can't convert banana into a int." # type: ignore

def test_grade():
    assert a1.grade(75,85,95) == "B" # type: ignore
    assert a1.grade("three", "blind", "mice") == "Invalid data was provided." # type: ignore

def test_repeat():
    assert a1.repeat("up,", 4) == "up,up,up,up," # type: ignore

def test_student_scores():
    assert a1.student_scores("mean", Tom=75, Dick=89, Angela=91) == (75 + 89 + 91) / 3 # type: ignore
    assert a1.student_scores("best", Tom=75, Dick=89, Angela=91, Frank=50 ) == "Angela" # type: ignore

def test_titleize():
    assert a1.titleize("war and peace") == "War and Peace" # type: ignore
    assert a1.titleize("a separate peace") == "A Separate Peace" # type: ignore
    assert a1.titleize("after on") == "After On" # type: ignore

def test_hangman():
    assert a1.hangman("difficulty","ic") == "_i__ic____" # type: ignore

def test_pig_latin():
    assert a1.pig_latin("apple") == "appleay" # type: ignore
    assert a1.pig_latin("banana") == "ananabay" # type: ignore
    assert a1.pig_latin("cherry") == "errychay" # type: ignore
    assert a1.pig_latin("quiet") == "ietquay" # type: ignore
    assert a1.pig_latin("square") == "aresquay" # type: ignore
    assert a1.pig_latin("the quick brown fox") == "ethay ickquay ownbray oxfay" # type: ignore
