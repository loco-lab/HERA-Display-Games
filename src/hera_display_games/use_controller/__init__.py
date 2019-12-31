#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""hello please"""

import numpy as np
import asyncio
from hera_display_games.core import mechanics, keymapper
import time
import click


async def recolor(sprite):
    time.sleep(10)
    return np.random.randint(0, 255, size=3).tolist()


@click.command()
@click.option(
    "-x",
    "-X",
    "--use-screen/--use-board",
    default=False,
    help="whether to use the physical HERA board",
)
@click.option("--input", default="gamepad", type=click.Choice(["gamepad", "keyboard"]))
def main(use_screen, input):
    my_sprite = mechanics.Sprite(np.array([0, 0]), color=[3, 137, 255])

    if not use_screen:
        my_board = mechanics.Board(sprites=[my_sprite])
    else:
        my_board = mechanics.VirtualBoard(sprites=[my_sprite])
    my_board.draw()

    if input == "gamepad":
        device = keymapper.GamePad()
    elif input == "keyboard":
        device = keymapper.KeyBoardArrows()
    else:
        raise ValueError("incorrect input")

    loop = asyncio.get_event_loop()
    # task1 = loop.create_task(recolor(my_sprite))
    # task2 = loop.create_task(keymapper.map_movement(device))

    while True:
        response = loop.run_until_complete(keymapper.map_movement(device))
        if response in ["ul", "ur", "dl", "dr", "r", "l"]:
            my_sprite.move(response)
            my_board.draw()
        elif response in ["r-trigger", "l-trigger"]:
            my_sprite.color = np.random.randint(0, 255, size=3).astype(int).tolist()
            my_board.draw()
