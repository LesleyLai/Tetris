"""
The core game class for the Tetris game
"""

import tkinter as tk

from tetris_gui import *
from tetris_board import TetrisBoard
        
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

        self._create_buttons()

        self.board = TetrisBoard(self)
        
        self._create_canvas()
        self._create_bindings()


        self.new_game()
        
        self.continue_game()
        self._update()
        
        self.root.mainloop()

    def new_game(self):
        '''Starts a new game'''
        # Dropping interval of the current piece (ms)
        self.interval = 500

        self.score = 0

        self.shape = self.draw_piece(self.board.current_block)
        self.board.last_shape = self.shape

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
        '''Update the board, do nothing if the game paused.'''
        
        if not self.paused:
            self.board.update()
            
        self.root.after(self.interval, self._update)

    def pause_game(self):
        """
        Pauses the game
        """
        self.paused = True
        self._pause_bottom["text"] = "continue"
        self._pause_bottom['bg'] = "green"
        self._pause_bottom['command'] = self.continue_game

    def continue_game(self):
        """
        Continues the game after pause
        """
        self.paused = False
        self._pause_bottom["text"] = "pause"
        self._pause_bottom['bg'] = "lightcoral"
        self._pause_bottom['command'] = self.pause_game

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
            bg="white")
        self.canvas.pack()

    def _create_bindings(self):
        self.root.bind('q', lambda event: self.root.destroy())

        self.root.bind('<space>',
                       lambda event: self.board.move_down())
        self.root.bind('<Left>',
                       lambda event: self.board.move_left())
        self.root.bind('<Right>',
                       lambda event: self.board.move_right())
        self.root.bind('<Up>',
                       lambda event: self.board.rotate_counterclockwise())
        self.root.bind('<Down>',
                       lambda event: self.board.rotate_clockwise())

        
        
def main():
    game = Tetris()

if __name__ == '__main__':
    main()
