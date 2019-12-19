import numpy as np
from hera_display_games.core import mechanics
import time

my_sprite = mechanics.Sprite(np.array([0, 0]))

my_board = mechanics.Board(sprites=[my_sprite])
my_board.draw()

directions = ["r", "r", "dl", "ur", "ur", "ul"]

for dir in directions:
    time.sleep(1)
    my_sprite.move(dir)
    my_board.draw()