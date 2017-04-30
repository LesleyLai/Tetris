"""
The main file for the Tetris game
"""

import random
import tkinter as tk

from tetris_gui import *

class TetrisPiece:
    """
    class responsible for the pieces and their movements
    """

    def __init__(self, rotations, board):
        "Create a new TetrisPoece from a given point list"
        self.all_rotations = rotations
        self.rotation_index = 0 # TODO: randomize it
        self.board = board
        self.color = random.sample(self.ALL_COLORS, 1)[0]
        self.moved = True
        self.position = (4, 1)

    def drop_one(self):
        """
        Drop the piece by one
        """
        self.move((0, 1), 0)

    def move(self, delta_position, delta_rotation):
        """
        takes the intended movement in position and rotation and checks
        to see if the movement is possible.  If it is, makes this
        movement.
        """
        self.moved = True
        
        rotation_index = (self.rotation_index + delta_rotation) % \
                         len(self.all_rotations)
        potential = self.all_rotations[rotation_index]

        # for each individual block in the piece, checks if the
        # intended move will put this block in an occupied space
        for pos in potential:
            if not self.board.empty_at((pos[0] + self.position[0] +
                                        delta_position[0],
                                        pos[1] + self.position[1] +
                                        delta_position[1])):
                self.moved = False
            
        if self.moved:
            self.position = (self.position[0] + delta_position[0],
                             self.position[1] + delta_position[1])

    @classmethod
    def generate_piece(cls, board):
        return TetrisPiece(random.sample(cls.ALL_PIECES, 1)[0], board)
    
    ALL_PIECES = [[[(0, 0), (1, 0), (0, 1), (1, 1)]], # square
                  [[(0, 0), (-1, 0), (1, 0), (2, 0)], # long
                   [(0, 0), (0, -1), (0, 1), (0, 2)]]]
        
    ALL_COLORS = ['DarkGreen', 'dark blue', 'blue', 'dark red',
                  'gold2', 'Purple3', 'OrangeRed2', 'LightSkyBlue']
        

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

        # Grid of the blocks store the information whether a block
        # occupies a point
        self.grid = [[None for x in range(self.columns_count)]
                     for y in range(self.rows_count)]
        
        self.score = 0
        self.level = 1
        self.current_block = TetrisPiece.generate_piece(self)

    def empty_at(self, point):
        """
        Takes a point and checks to see if it is in the bounds of the
        board and currently empty.
        """
        if point[0] < 0 or point[0] >= self.columns_count or \
           point[1] >= self.rows_count:
            return False # out of index
        else:
            return self.grid[point[1]][point[0]] == None
        

    def move_left(self):
        '''Moves the current block to left'''
        self.current_block.move((-1, 0), 0)

    def move_right(self):
        '''Moves the current block to right'''
        self.current_block.move((1, 0), 0)
        
class Tetris:
    """
    The main Tetris class
    """

    def __init__(self):
        """
        Constructor of Tetris class
        """
        self.root = tk.Tk()
        self.root.title("Tetris")

        self.score = 0
        self._create_buttons()

        self.board = TetrisBoard(self)
        self._create_canvas()
        self._create_bindings()

         # Dropping interval of the current piece (ms)
        self.interval = 500

        self.shape = self.draw_piece(self.board.current_block)

        self.continue_game()
        self._update()
        self._render()
        
        self.root.mainloop()

    def draw_piece (self, piece, old=None):
        """
        takes a piece and optionally the list of old rectangle
        corresponding to it and returns a new set of rectangle
        which are how the piece is visible to the user.
        """
        block_size = self.board.block_size
        color = piece.color
        canvas = self.canvas
        new_shape = []

        if old != None:
            for rect in old:
                canvas.delete(rect)
        
        for point in piece.all_rotations[piece.rotation_index]:
            x = (point[0] + piece.position[0]) * block_size
            y = (point[1] + piece.position[1]) * block_size
            rect = canvas.create_rectangle(x, y,
                                           block_size + x,
                                           block_size + y,
                                           fill=color)
            new_shape.append(rect)
        return new_shape

    def _update(self):
        """
        Makes the current_block drop by one, do nothing if the game 
        paused.
        """
        if not self.paused:
            self.board.current_block.drop_one()
            
        self.root.after(self.interval, self._update)

    def _render(self):
        """
        Redraws the canvas
        """
        self.shape = self.draw_piece(self.board.current_block,
                                         self.shape)

        self.root.after(33, self._render)

    def pause_game(self):
        """
        Pauses the game
        """
        self.paused = True
        self._pause_bottom["text"] = "continue"
        self._pause_bottom['bg'] = "green"
        self._pause_bottom['command'] = self.continue_game

        self.root.unbind('<space>')
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')

    def continue_game(self):
        """
        Continues the game after pause
        """
        self.paused = False
        self._pause_bottom["text"] = "pause"
        self._pause_bottom['bg'] = "lightcoral"
        self._pause_bottom['command'] = self.pause_game

        self.root.bind('<space>',
                       lambda event: self.board.current_block.drop_one())
        self.root.bind('<Left>',
                       lambda event: self.board.move_left())
        self.root.bind('<Right>',
                       lambda event: self.board.move_right())

    def _create_buttons(self):
        """
        Creates buttons for the tetris game
        """        
        color = "lightcoral"
        self._buttoms = tk.Frame(self.root)
        self._buttoms.pack()
        
        self._new_bottom = TetrisButtom(self._buttoms, "new game", color)
        self._new_bottom.pack(side="left")

        self._pause_bottom = TetrisButtom(self._buttoms, "pause",
                                          color, self.pause_game)
        self._pause_bottom.pack(side="left")

        self._quit_bottom = TetrisButtom(self._buttoms, "quit", color,
                                        self.root.destroy)
        self._quit_bottom.pack(side="left")

        self.status_var = tk.StringVar() 
        self.status_var.set("Score: 0, Level: 1")
        self._status_label = tk.Label(self.root,
                               textvariable=self.status_var, 
                               font=("Helvetica", 10, "bold"))
        self._status_label.pack()

    def _create_canvas(self):
        self.canvas = tk.Canvas(
            self.root,
            width=self.board.block_size * self.board.columns_count,
            height=self.board.block_size * self.board.rows_count,
            bg="purple")
        self.canvas.pack()

    def _create_bindings(self):
        self.root.bind('q', lambda event: self.root.destroy())

        
        
def main():
    game = Tetris()

if __name__ == '__main__':
    main()
