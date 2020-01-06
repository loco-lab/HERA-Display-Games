#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""hello please"""

import numpy as np
import asyncio
from hera_display_games.core import board, keymapper, sprites
import click
from hera_display_games.core.game import Game


async def recolor(device, my_board, sprite):
    while True:
        await asyncio.sleep(5)
        sprite.color = np.random.randint(0, 255, size=3).tolist()


async def move_sprite(device, my_board, sprite):
    while True:
        response = await keymapper.map_movement(device)
        if response in ["ul", "ur", "dl", "dr", "r", "l"]:
            my_board.move_sprite(sprite, response)
        elif response in ["r-trigger", "l-trigger"]:
            sprite.color = np.random.randint(0, 255, size=3).astype(int).tolist()


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
    my_sprite = sprites.RigidSprite(np.array([0, 0]), color=[3, 137, 255])

    if not use_screen:
        my_board = board.Board(sprites=[my_sprite])
    else:
        my_board = board.VirtualBoard(sprites=[my_sprite])

    game = Game(my_board, input, (recolor, move_sprite))
    game.run()
