"""
The piece of the tetris
"""
import random

def rotations(points):
    """
    Figures out the different rotations of the provided piece
    """
    rot1 = list(map(lambda pos: (-pos[1], pos[0]), points))
    rot2 = list(map(lambda pos: (-pos[0], -pos[1]), points))
    rot3 = list(map(lambda pos: (pos[1], -pos[0]), points))
    return [points, rot1, rot2, rot3]

class TetrisPiece:
    """
    class responsible for the pieces and their movements
    """

    def __init__(self, rotation, board):
        "Create a new TetrisPoece from a given point list"
        self.all_rotations = rotation
        self.rotation_index = 0 # TODO: randomize it
        self.board = board
        self.color = random.sample(self.ALL_COLORS, 1)[0]
        self.position = (4, 1)

    def drop_one(self):
        """
        Drop the piece by one, and returns whether we can drop it
        """
        return self.move((0, 1), 0)

    def move(self, delta_position, delta_rotation):
        """
        Takes the intended movement in position and rotation and check
        to see if the movement is possible. If it is, makes this
        movement and return true, otherwise return false.
        """
        moved = True

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
                moved = False

        if moved:
            self.position = (self.position[0] + delta_position[0],
                             self.position[1] + delta_position[1])
            self.rotation_index = rotation_index

        self.board.draw()
        return moved

    @classmethod
    def generate_piece(cls, board):
        '''Chooses the next piece'''
        return TetrisPiece(random.sample(cls.ALL_PIECES, 1)[0], board)

    ALL_PIECES = [[[(0, 0), (1, 0), (0, 1), (1, 1)]], # square
                  [[(0, 0), (-1, 0), (1, 0), (2, 0)], # long
                   [(0, 0), (0, -1), (0, 1), (0, 2)]],
                  rotations([(0, 0), (0, -1), (0, 1), (1, 1)]), # L
                  rotations([(0, 0), (0, -1), (0, 1), (-1, 1)]), # _|
                  rotations([(0, 0), (-1, 0), (0, -1), (1, -1)]), # S
                  rotations([(0, 0), (1, 0), (0, -1), (-1, -1)])] # Z

    ALL_COLORS = ['DarkGreen', 'dark blue', 'blue', 'dark red',
                  'gold2', 'Purple3', 'OrangeRed2', 'LightSkyBlue']
