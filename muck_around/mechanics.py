import numpy as np


DIR_DICT = {
    "ul": np.array([0, 1]),
    "ur": np.array([1, 1]),
    "r": np.array([1, 0]),
    "dr": np.array([0, -1]),
    "dl": np.array([-1, -1]),
    "l": np.array([-1, 0]),
}


class Sprite:
    """Class for sprites."""

    def __init__(self, location=np.array([0, 0])):
        """Init for sprites."""
        self.location = location

    def move(self, direction):
        try:
            self.location += DIR_DICT[direction]
        except KeyError:
            raise ValueError("Direction not understood!")


class Board:
    """Class for the board."""

    def __init__(self, sprites=[]):
        """Init for the board."""
        self.sprites = sprites
