# Task 6: Tic-Tac-Toe using classes


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
        "lower right"
    ]

    def __init__(self):
        self.board_array = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

        self.turn = "X"
        self.last_move = None

    def __str__(self):
        lines = []

        lines.append(
            f" {self.board_array[0][0]} | "
            f"{self.board_array[0][1]} | "
            f"{self.board_array[0][2]} \n"
        )

        lines.append("-----------\n")

        lines.append(
            f" {self.board_array[1][0]} | "
            f"{self.board_array[1][1]} | "
            f"{self.board_array[1][2]} \n"
        )

        lines.append("-----------\n")

        lines.append(
            f" {self.board_array[2][0]} | "
            f"{self.board_array[2][1]} | "
            f"{self.board_array[2][2]} \n"
        )

        return "".join(lines)

    def move(self, move_string):
        move_string = move_string.lower().strip()

        if move_string not in Board.valid_moves:
            raise TictactoeException(
                "That's not a valid move."
            )

        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3

        if self.board_array[row][column] != " ":
            raise TictactoeException(
                "That spot is taken."
            )

        current_player = self.turn
        self.board_array[row][column] = current_player
        self.last_move = (row, column)

        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        winner = self.check_winner()

        if winner is not None:
            return True, f"{winner} has won"

        board_full = all(
            space != " "
            for row in self.board_array
            for space in row
        )

        if board_full:
            return True, "Cat's Game"

        return False, f"{self.turn}'s turn"

    def check_winner(self):
        winning_lines = []

        # Rows
        winning_lines.extend(self.board_array)

        # Columns
        for column in range(3):
            winning_lines.append([
                self.board_array[0][column],
                self.board_array[1][column],
                self.board_array[2][column]
            ])

        # Diagonals
        winning_lines.append([
            self.board_array[0][0],
            self.board_array[1][1],
            self.board_array[2][2]
        ])

        winning_lines.append([
            self.board_array[0][2],
            self.board_array[1][1],
            self.board_array[2][0]
        ])

        for line in winning_lines:
            if line[0] != " " and line[0] == line[1] == line[2]:
                return line[0]

        return None


def play_game():
    board = Board()
    game_over = False

    print("Valid moves:")

    for move_name in Board.valid_moves:
        print(f"- {move_name}")

    while not game_over:
        print()
        print(board)

        move_prompt = f"{board.turn}'s move: "
        move_string = input(move_prompt)

        try:
            board.move(move_string)
        except TictactoeException as exception:
            print(exception.message)
            continue

        game_over, message = board.whats_next()
        print(message)

    print()
    print(board)


if __name__ == "__main__":
    play_game()
