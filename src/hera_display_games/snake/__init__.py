import random
from hera_display_games.core import sprites,map_dict

class Snake(sprites.Sprite):

    def encounter(self, other, prev_loc):
        if isinstance(other, Apple):
            self.grow()
            while other.location in self.pixels:
                other.location = random.choice(map_dict.)

            other.move()

    def die(self):

    def hit_boundary(self):

class Apple(object):



     #random location generation: define how close it should be to the boundary for reaction time
     #what happens when it gets eaten?
