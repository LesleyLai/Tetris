"""
The board manages pieces and communicates with the game
"""

from tetris_piece import TetrisPiece

def all_filled(collection):
    """
    Return true if all the element in a collection is not None
    """
    for elem in collection:
        if elem is None:
            return False

    return True

class TetrisBoard:
    """
    Does the interaction between the pieces and the game itself
    """

    def __init__(self, game):
        "Initialize the board"
        self.game = game

        self.block_size = 18
        self.columns_count = 10
        self.rows_count = 27

        self.reset()

    def reset(self):
        """
        Clears board for the new game
        """

        # How many rows are eliminated, decided level of the game
        self.removed_row_count = 0

        # Grid of the blocks store the information whether a block
        # occupies a point
        self.grid = [[None for x in range(self.columns_count)]
                     for y in range(self.rows_count)]

        self.current_block = TetrisPiece.generate_piece(self)
        self.last_shape = None

    def update(self):
        """
        Drop the current block by one
        """
        if self.is_game_over():
            self.game.game_over()
        elif not self.current_block.drop_one():
            self._store_current()
            self.next_piece()

    def empty_at(self, point):
        """
        Takes a point and checks to see if it is in the bounds of the
        board and currently empty.
        """
        if point[0] < 0 or point[0] >= self.columns_count or \
           point[1] >= self.rows_count:
            return False # out of index
        else:
            return self.grid[point[1]][point[0]] is None

    def move_down(self):
        '''Moves the current block down'''
        if not self.game.paused:
            self.current_block.drop_one()

    def move_left(self):
        '''Moves the current block to left'''
        if not self.game.paused:
            self.current_block.move((-1, 0), 0)

    def move_right(self):
        '''Moves the current block to right'''
        if not self.game.paused:
            self.current_block.move((1, 0), 0)

    def rotate_clockwise(self):
        '''Rotates the current piece clockwise'''
        if not self.game.paused:
            self.current_block.move((0, 0), 1)

    def rotate_counterclockwise(self):
        '''Rotates the current piece counterclockwise'''
        if not self.game.paused:
            self.current_block.move((0, 0), -1)

    def next_piece(self):
        '''Gets the next piece'''
        self.current_block = TetrisPiece.generate_piece(self)
        self.last_shape = None

    def is_game_over(self):
        """
        Returns true if the the player lost
        """
        for pos in self.grid[0]:
            if not pos is None:
                return True

        return False

    def _store_current(self):
        """
        Gets the information from the current piece about where it is
        and uses this to store the piece on the board itself. And then
        calls remove_filled.
        """
        positions = self.current_block.all_rotations[
            self.current_block.rotation_index]
        displacement = self.current_block.position
        for i, pos in enumerate(positions):
            self.grid[
                pos[1] + displacement[1]][pos[0] + displacement[0]] \
            = self.last_shape[i]
        self._remove_filled()

    def _remove_filled(self):
        """
        Removes all filled rows and replaces them with empty ones,
        dropping all rows above them down each time a row is removed
        and increasing the score.
        """
        for i in range(1, len(self.grid)):
            row = self.grid[i]
            if all_filled(row):
                for block in row:
                    self.game.canvas.delete(block)
                self.grid[i] = [None for x in row]

                # Moves down all rows above and move their blocks on
                # the canvas
                for j in reversed(range(1, i)):
                    for block in self.grid[j - 1]:
                        if not block is None:
                            self.game.canvas.move(block,
                                                  0, self.block_size)

                    if (j - 1 >= 0):
                        self.grid[j] = self.grid[j - 1]

                self.removed_row_count += 1
                self.game.scoring(self.removed_row_count)

    def draw(self):
        """
        Draws the current piece
        """
        self.last_shape = self.game.draw_piece(self.current_block,
                                               self.last_shape)
