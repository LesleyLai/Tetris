"""
The main file for the Tetris game
"""

from tetris_gui import *
import tkinter as tk

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

        self.status_var = tk.StringVar() 
        self.status_var.set("Score: 0, Level: 1")
        self.status = tk.Label(self.root,
                               textvariable=self.status_var, 
                               font=("Helvetica", 10, "bold"))
        self.status.pack()
        
        self.canvas = tk.Canvas(
                self.root, width=300, height=500, bg="green")
        self.canvas.pack()

        self.root.mainloop()

    def _create_buttons(self):
        """
        Creates buttons for the tetris game
        """        
        color = "lightcoral"
        self._buttoms = tk.Frame(self.root)
        self._buttoms.pack()
        
        self.new_bottom = TetrisButtom(self._buttoms, "new game", color)
        self.new_bottom.pack(side="left")

        self.pause_bottom = TetrisButtom(self._buttoms, "pause", color)
        self.pause_bottom.pack(side="left")

        self.quit_bottom = TetrisButtom(self._buttoms, "quit", color,
                                        self.root.destroy)
        self.quit_bottom.pack(side="left")
        
def main():
    game = Tetris()

if __name__ == '__main__':
    main()
