from abc import ABC, abstractmethod

from . import map_dict
import copy

DIR_DICT = {
    "ul": [0, 1],
    "ur": [1, 1],
    "r": [1, 0],
    "dr": [0, -1],
    "dl": [-1, -1],
    "l": [-1, 0],
}


class OutOfBoundsError(Exception):
    pass


class Sprite(ABC):
    """Class for sprites."""

    def __init__(self, location=(0, 0), pixels=None, color=(0, 255, 0), id=None):
        """Init for sprites."""
        self.location = location

        self.pixels = pixels or [location]

        assert location in self.pixels, "the pixels need to contain the location"

        if len(color) == 3 and isinstance(color[0], int):
            self.color = [color] * len(self.pixels)
        elif isinstance(color[0], tuple) and len(color[0]) == 3:
            self.color = list(color)
        else:
            raise ValueError("color should be either a list of 3-tuples or a single 3-tuple.")

        assert all(len(c) == 3 for c in self.color), "color should be a 3-tuple or list of such"

        self.dead = False
        self.id = id

    def move(self, movement):
        if isinstance(movement, int):
            try:
                self.location[0] = map_dict.reverse_led_map[movement][0]
                self.location[1] = map_dict.reverse_led_map[movement][1]
            except KeyError:
                raise OutOfBoundsError
        elif isinstance(movement, str):
            try:
                self.location = (
                    self.location[0] + DIR_DICT[movement][0],
                    self.location[1] + DIR_DICT[movement][1],
                )
            except KeyError:
                raise ValueError("That was a bad string for movement")
        elif hasattr(movement, "__len__"):
            if len(movement) != 2:
                raise ValueError("movement should be a 2-tuple!")
            self.location = copy.copy(movement)
        else:
            raise ValueError("Could not understand movement type.")

        if any(loc not in map_dict.led_map for loc in self.pixels):
            raise OutOfBoundsError

    @abstractmethod
    def encounter(self, other, prev_loc):
        return True

    @abstractmethod
    def hit_boundary(self, prev_loc):
        pass


class RigidSprite(Sprite):
    def encounter(self, other, prev_loc):
        self.move(prev_loc)
        return True

    def hit_boundary(self, prev_loc):
        self.move(prev_loc)


class HungrySprite(RigidSprite):
    def encounter(self, other, prev_loc):
        if self.dead or other.dead:
            return True

        print("{} encountering {} and killing it!".format(self.id, other.id, self.dead, other.dead))
        other.dead = True
        return True
