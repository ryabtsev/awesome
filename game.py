import numpy as np


class ColumnIsFull(Exception):
    pass


class InvalidColumn(Exception):
    pass


class Game:
    def __init__(self, row_count=6, column_count=7, players_count=2, connect_count=4):
        self.row_count = row_count
        self.column_count = column_count
        self.players_count = players_count
        self.connect_count = connect_count

        self.board = np.full((self.row_count, self.column_count), 0)

    def ui_input(self, player: int):
        col = input(
            f"Player number {player} your move. "
            f"Enter column number [1-{self.column_count}]:"
        )
        try:
            col = int(col)
        except ValueError:
            raise InvalidColumn
        if col < 1 or col > self.column_count:
            raise InvalidColumn
        return col - 1

    def ui_display_board(self):
        print(np.flip(self.board, 0))

    def check(self, player_point):
        # check rows and diagonals, then rotate 90 degrees and check again
        # Concerned about time complexity on rotation using numpy , but it looks understandable enough
        for bord_view in [self.board, np.rot90(self.board)]:
            row_count, column_count = bord_view.shape
            for c in range(column_count - self.connect_count + 1):
                for r in range(row_count):
                    if all(bord_view[r][c + i] == player_point for i in range(self.connect_count)):
                        return True

            for c in range(column_count - self.connect_count + 1):
                for r in range(row_count - self.connect_count + 1):
                    if all(bord_view[r + i][c + i] == player_point for i in range(self.connect_count)):
                        return True

    def move(self, col, player):
        row = None
        for r in range(self.row_count ):
            if self.board[r][col] == 0:
                row = r
                break
        if row is None:
            raise ColumnIsFull

        self.board[row][col] = player

    def run(self):
        winner = False
        current_player = 1

        self.ui_display_board()

        while not winner:
            try:
                col = self.ui_input(current_player)
            except InvalidColumn:
                print("Invalid column")
                continue

            try:
                self.move(col, current_player)
            except ColumnIsFull:
                print("Column is full")
                continue

            self.ui_display_board()

            if self.check(current_player):
                print(f"\n\nPlayer number {current_player} wins!")
                print(f"\nCongratulations!\n")
                winner = current_player

            current_player += 1
            if current_player > self.players_count:
                current_player = 1


if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        pass
