"""
The core game class for the Tetris game
"""

import math
import tkinter as tk

from tetris_gui import *
from tetris_board import TetrisBoard
from tetris_ranking import TetrisRankingList

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

        self.ranking = TetrisRankingList("classic.score")

        try:
            self.highest_score = self.ranking[0][0]
        except IndexError:
            self.highest_score = 0

        self._create_buttons()
        self._create_labels()

        self.board = TetrisBoard(self)

        self._create_canvas()
        self._create_bindings()

        self.new_game()

        self.continue_game()
        self._update()

    def new_game(self):
        '''Starts a new game'''
        # Dropping interval of the current piece (ms)
        self._interval = 500

        self.score = 0
        self.level = 1

        self._is_game_over = False
        self.board.reset()

        self.shape = self.draw_piece(self.board.current_block)
        self.board.last_shape = self.shape

        self._status_var.set("Score: 0, Level: 1")

        # Clears the canvas
        self.canvas.delete("all")


    def draw_piece(self, piece, old=None):
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

        if not (self.paused or self._is_game_over):
            self.board.update()

        self.root.after(self._interval, self._update)

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

    def game_over(self):
        self._is_game_over = True
        for row in self.board.grid:
            for block in row:
                self.canvas.itemconfig(block, fill="grey")

        self.canvas.create_text(self.canvas.winfo_width() / 2,
                                self.canvas.winfo_height() / 2,
                                fill="red",
                                text="Game Over",
                                font=("Helvetica", 20, "bold")
        )

        self.ranking.add_record(self.score)

    def scoring(self, removed_row_count):
        """
        Updates the score when remove filled line and change
        level accordingly
        """
        self.score += 9 + self.level
        if self.score > self.highest_score:
            self.highest_score = self.score
            self._highest_score_var.set("Highest score: " + \
                                        str(self.highest_score))

        # Upgrade level
        if removed_row_count > (self.level * 5) and self.level < 21:
            self.level += 1
            self._interval = 500 - int(math.log10(self.level) * 300)

        self._status_var.set("Score: " + str(self.score) + \
                            ", Level: " + str(self.level))


    def _create_buttons(self):
        """
        Creates top buttons for the Tetris game
        """
        color = "lightcoral"
        self._buttoms = tk.Frame(self.root)
        self._buttoms.pack()

        new_bottom = TetrisButtom(self._buttoms, "new game",
                                  color, self.new_game)
        new_bottom.pack(side="left")

        self._pause_bottom = TetrisButtom(self._buttoms, "pause",
                                          color, self.pause_game)
        self._pause_bottom.pack(side="left")

        ranking_bottom = TetrisButtom(self._buttoms, "ranking",
                                            color, self.show_ranking)
        ranking_bottom.pack(side="left")

        quit_bottom = TetrisButtom(self._buttoms, "quit", color,
                                   self.root.destroy)
        quit_bottom.pack(side="left")

    def show_ranking(self):
        """
        Opens the ranking list
        """
        if not self.paused:
            self.pause_game()
        window = tk.Toplevel()

        text = tk.Text(window, height=13, width=30)
        text.insert(tk.END, "         High Scores\n\n")
        for i in range(0, len(self.ranking)):
            text.insert(tk.END, "No." + str(i + 1) + " " + \
                        self.ranking[i][1] + " " + \
                        str(self.ranking[i][0]) + "\n")
        text.pack()

    def _create_labels(self):
        """
        Creates text labels for the game
        """
        self._status_var = tk.StringVar()
        status_label = tk.Label(self.root,
                               textvariable=self._status_var,
                               font=("Helvetica", 10, "bold"))
        status_label.pack()

        self._highest_score_var = tk.StringVar()
        self._highest_score_var.set("Highest score: " + \
                                    str(self.highest_score))
        highest_score_label = tk.Label(self.root,
                                textvariable=self._highest_score_var,
                                font=("Helvetica", 10, "bold"))
        highest_score_label.pack(side='bottom')
        

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
