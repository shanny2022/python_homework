"""Task 6: Tic-Tac-Toe using classes and custom exceptions."""

# Task 6


class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    valid_moves = [
        "upper left",
        "upper center",
        "upper right",
        "middle left",
        "center",
        "middle right",
        "lower left",
        "lower center",
        "lower right",
    ]

    def __init__(self):
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.last_move = None

    def __str__(self):
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)

    def move(self, move_string):
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")
        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3
        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")
        self.board_array[row][column] = self.turn
        self.last_move = move_string
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        win = False
        winner = None

        for i in range(3):
            if self.board_array[i][0] != " " and self.board_array[i][0] == self.board_array[i][1] == self.board_array[i][2]:
                win = True
                winner = self.board_array[i][0]
                break

        if not win:
            for i in range(3):
                if self.board_array[0][i] != " " and self.board_array[0][i] == self.board_array[1][i] == self.board_array[2][i]:
                    win = True
                    winner = self.board_array[0][i]
                    break

        if not win and self.board_array[1][1] != " ":
            if self.board_array[0][0] == self.board_array[1][1] == self.board_array[2][2]:
                win = True
                winner = self.board_array[1][1]
            elif self.board_array[0][2] == self.board_array[1][1] == self.board_array[2][0]:
                win = True
                winner = self.board_array[1][1]

        if win:
            return (True, f"{winner} has won")

        board_full = all(cell != " " for row in self.board_array for cell in row)
        if board_full:
            return (True, "Cat's Game")

        return (False, f"{self.turn}'s turn")


if __name__ == "__main__":
    board = Board()
    game_over = False

    print("Welcome to Tic-Tac-Toe!")
    while not game_over:
        print(board)
        prompt = f"{board.turn}'s move ({', '.join(Board.valid_moves)}): "
        move_text = input(prompt).strip().lower()
        try:
            board.move(move_text)
        except TictactoeException as error:
            print(error.message)
            continue

        game_over, message = board.whats_next()
        if game_over:
            print(board)
            print(message)
