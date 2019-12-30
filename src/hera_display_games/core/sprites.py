from abc import ABC, abstractmethod
from . import map_dict

DIR_DICT = {
    "ul": [0, 1],
    "ur": [1, 1],
    "r": [1, 0],
    "dr": [0, -1],
    "dl": [-1, -1],
    "l": [-1, 0],
}


class Sprite(ABC):
    """Class for sprites."""

    def __init__(self, location=[0, 0], color=[0, 255, 0], id=None):
        """Init for sprites."""
        self.location = location
        self.color = color
        self.dead = False
        self.id = id

    def move(self, movement):
        try:
            self.location[0] += DIR_DICT[movement][0]
            self.location[1] += DIR_DICT[movement][1]
        except TypeError:
            if type(movement) == int:
                self.location[0] = map_dict.reverse_led_map[movement][0]
                self.location[1] = map_dict.reverse_led_map[movement][1]
            else:
                if len(movement) != 2:
                    raise ValueError("movement should be a 2-tuple!")
                self.location = movement.copy()
        except KeyError:
            raise ValueError("That was a bad string for movement")

    @abstractmethod
    def encounter(self, other, prev_loc):
        return True


class RigidSprite(Sprite):
    def encounter(self, other, prev_loc):
        self.move(prev_loc)
        return True


class HungrySprite(Sprite):
    def encounter(self, other, prev_loc):
        if self.dead or other.dead:
            return True

        print("{} encountering {} and killing it!".format(self.id, other.id, self.dead, other.dead))
        other.dead = True
        return True
