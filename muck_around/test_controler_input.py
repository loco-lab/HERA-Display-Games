#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""hello please"""

import numpy as np
import asyncio
from hera_display_games.core import mechanics, keymapper
import time


async def recolor(sprite):
    time.sleep(10)
    return np.random.randint(0, 255, size=3).tolist()


my_sprite = mechanics.Sprite(np.array([0, 0]), color=[3, 137, 255])

my_board = mechanics.Board(sprites=[my_sprite])
my_board.draw()

device = keymapper.get_gamepad()
loop = asyncio.get_event_loop()
# task1 = loop.create_task(recolor(my_sprite))
# task2 = loop.create_task(keymapper.map_movement(device))

while True:
    response = loop.run_until_complete(keymapper.map_movement(device))
    if response in ["ul", "ur", "dl", "dr", "r", "l"]:
        my_sprite.move(response)
        my_board.draw()
