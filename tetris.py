"""
The main file for the Tetris game
"""

from tetris_gui import *

class Tetris(tk.Frame):
    """
    The main Tetris class
    """

    def __init__(self):
        """
        Constructor of Tetris class
        """
        self.root = tk.Tk()
        self.root.title("Tetris")
        super().__init__(self.root)

        self.pack()

        self.canvas = tk.Canvas(self, bg="green", width=240, height=600)
        self.canvas.pack(side="bottom")

        self._create_buttons()

    def _create_buttons(self):
        """
        Creates buttons for the tetris game
        """
        self.buttons = tk.Frame(self)
        self.buttons.pack(side="top")

        self.new_bottom = TetrisButtom(self.buttons, "new game", \
                                       "lightcoral")
        #self.new_buttom["command"] = self.new_game
        self.new_bottom.pack(side="left")

        self.pause_bottom = TetrisButtom(self.buttons, "pause", \
                                       "lightcoral")
        self.pause_bottom.pack(side="left")

        self.quit_bottom = TetrisButtom(self.buttons, "quit", \
                                        "lightcoral", \
                                        self.root.destroy)
        self.quit_bottom.pack(side="left")

def main():
    app = Tetris()
    app.mainloop()

if __name__ == '__main__':
    main()
