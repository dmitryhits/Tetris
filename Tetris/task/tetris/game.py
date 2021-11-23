# Write your code here
import numpy as np


class TetrisFigure:
    def __init__(self, symbol=None, orientation=0):
        O = [[4, 14, 15, 5]]
        I = [[4, 14, 24, 34], [3, 4, 5, 6]]
        S = [[5, 4, 14, 13], [4, 14, 15, 25]]
        Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
        L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
        J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
        T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]
        pieces = dict(L=L, I=I, O=O, T=T, Z=Z, S=S, J=J)
        if symbol:
            self.piece = np.array(pieces[symbol])
        else:
            self.piece = np.array([[]])
        self.max_turns = len(self.piece)
        self.orientation = orientation
        self.frozen = False

    def set_next_orientation(self):
        if self.orientation < self.max_turns - 1:
            self.orientation += 1
        else:
            self.orientation = 0

    def get_current_view(self):
        return self.piece[self.orientation]

    def advance_piece(self, number):
        """adds a number to all rotations of the figure
        Is used for shifting pieces left, right, and down on the board"""
        self.piece += number

    def is_frozen(self):
        return self.frozen

    def freeze(self):
        self.frozen = True

    def delete(self):
        self.piece = np.array([[]])
        self.orientation = 0
        self.max_turns = 0


class TetrisBoard:
    def __init__(self, n_cols=10, n_rows=20):
        self.bottom_pieces = []
        self.active_piece = TetrisFigure()
        self.cols = n_cols
        self.rows = n_rows
        self.last_row = np.arange(n_rows * n_cols)[-n_cols:]
        self.top_row = np.arange(n_cols)
        print(self.draw_board())

    def add_piece(self):
        symbol = input()
        # symbol = input("piece: ")

        # check that the new piece does not intersect with the bottom pieces
        # print('bottom', self.bottom_pieces)
        if np.intersect1d(TetrisFigure(symbol).get_current_view(), self.bottom_pieces).size > 0:
            print("Game Over!")
            exit()
        self.active_piece = TetrisFigure(symbol)

    def rotate(self):
        self.active_piece.set_next_orientation()

    def shift(self, direction):
        touching_right = ((self.active_piece.get_current_view() + 1) % self.cols == 0).any()
        touching_left = ((self.active_piece.get_current_view()) % self.cols == 0).any()

        if direction == 'right' and not touching_right:
            self.active_piece.advance_piece(1)
        elif direction == 'left' and not touching_left:
            self.active_piece.advance_piece(-1)

    def down(self):
        self.active_piece.advance_piece(self.cols)

    def draw_board(self):
        matrix = ''
        # print(figure)
        pieces = np.union1d(self.active_piece.get_current_view(), self.bottom_pieces)
        for r in range(self.rows):
            # initialize the row
            row = ''
            for c in range(self.cols):
                # draw figure in the middle of the row
                if r * self.cols + c in pieces and c != self.cols - 1:
                    row += '0 '
                # draw figure at the end of the row
                elif r * self.cols + c in pieces and c == self.cols - 1:
                    row += '0\n'
                # draw an empty cell in the middle of the row
                elif c != self.cols - 1:
                    row += '- '
                # draw an empty cell at the end of the row
                else:
                    row += '-\n'
            matrix += row
        return matrix

    def check_stop(self):
        """Checks whether the current view of the active piece intersects with the last row
        or shifting the piece one row down will intersect it with the pieces on the bottom
        if it is then add it to the bottom pieces and freeze it"""
        if np.intersect1d(self.active_piece.get_current_view(), self.last_row).size > 0 \
                or np.intersect1d(self.active_piece.get_current_view() + self.cols, self.bottom_pieces).size > 0:
            # print('adding to bottom pieces')
            self.bottom_pieces = np.union1d(self.active_piece.get_current_view(), self.bottom_pieces)
            self.active_piece.delete()
            # print(bool(self.active_piece.get_current_view().size))
            # self.check_full_row()


    def check_end_game(self):
        # print('checking end game', np.intersect1d(self.bottom_pieces, self.top_row))
        if np.intersect1d(self.bottom_pieces, self.top_row).size > 0:
            print(self.draw_board())
            print("Game Over!")
            exit()

    def check_full_row(self):
        # print('checking full row')
        for i_row in range(self.rows):
            row_array = np.arange(i_row * self.cols, (i_row + 1) * self.cols)
            # print("row_array", row_array)
            # print(self.bottom_pieces)
            if np.in1d(row_array, self.bottom_pieces).all():
                # remove the full row
                # print('removing full row')
                self.bottom_pieces = np.setdiff1d(self.bottom_pieces, row_array)
                # print('bottom 1: ', self.bottom_pieces)
                # then shift the parts above one row down
                self.bottom_pieces[self.bottom_pieces < i_row * self.cols] += self.cols
                # print('bottom 2: ', self.bottom_pieces)

    def command(self, command):
        move_commands = ['rotate', 'right', 'left', 'down']
        if command in move_commands:
            self.check_stop()
            # print(self.active_piece.get_current_view())
            if self.active_piece.get_current_view().size == 0:
                self.check_end_game()
            else:
                if command == 'rotate':
                    self.down()
                    self.rotate()
                elif command == 'right':
                    self.down()
                    self.shift('right')
                elif command == 'left':
                    self.down()
                    self.shift('left')
                elif command == 'down':
                    self.down()
        elif command == 'break':
            self.check_full_row()
        elif command == 'piece':
            self.add_piece()
            self.check_stop()
        elif command == 'exit':
            exit()
        print(self.draw_board())


if __name__ == '__main__':
    x, y = input().split()
    # x, y = input('board dimension: ').split()
    x, y = int(x), int(y)
    print()
    board = TetrisBoard(x, y)
    while True:
        input_command = input()
        board.command(input_command)
