"""
The runner of the Tetris game
"""

from tetris_game import Tetris

def main():
    """
    The start point of the game
    """
    game = Tetris()
    game.root.mainloop()

if __name__ == '__main__':
    main()
