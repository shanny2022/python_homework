# Task 4: Closure practice


def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        if letter not in guesses:
            guesses.append(letter)

        displayed_word = ""

        for secret_letter in secret_word:
            if secret_letter in guesses:
                displayed_word += secret_letter
            else:
                displayed_word += "_"

        print(displayed_word)

        return "_" not in displayed_word

    return hangman_closure


def play_hangman():
    secret_word = input("Enter the secret word: ").lower()

    hangman_game = make_hangman(secret_word)
    word_complete = False

    while not word_complete:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1:
            print("Please enter one letter.")
            continue

        word_complete = hangman_game(guess)

    print("You guessed the full word!")


if __name__ == "__main__":
    play_hangman()
