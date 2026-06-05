"""Task 4: Closure-based hangman game."""

# Task 4

def make_hangman(secret_word):
    """Return a closure that tracks guesses for the secret word."""
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)
        masked = "".join(char if char in guesses else "_" for char in secret_word)
        print(masked)
        return "_" not in masked

    return hangman_closure


if __name__ == "__main__":
    word = input("Enter the secret word: ").strip()
    game = make_hangman(word)

    done = False
    while not done:
        guess = input("Guess a letter: ").strip()
        if len(guess) != 1:
            print("Please enter one letter.")
            continue
        done = game(guess)

    print("You guessed the word!")
