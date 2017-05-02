#!/usr/bin/env python3

"""
The runner of the Tetris game
"""

import sys
from tetris_game import Tetris

def run_classic_game():
    ''' Runs the classic tetris'''
    game = Tetris()
    game.root.mainloop()

def main():
    """
    The start point of the game
    """
    if len(sys.argv) == 1:
        option = input(
            "Choose the Tetris version [classic | enhanced]")
        if option == 'classic':
            run_classic_game()
        elif option == 'enhanced':
            pass
        else:
            print("Error: Unknown option")
    elif len(sys.argv) == 2:
        option = sys.argv[1]
        if option == 'classic':
            run_classic_game()
        elif option == 'enhanced':
            pass
        else:
            print("Error: Unknown option")
    else:
        print("usage: tetris.py [classic | enhanced]")
    


if __name__ == '__main__':
    main()
