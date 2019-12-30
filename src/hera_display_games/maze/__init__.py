#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple simulation of a random walk"""
import asyncio
import sys
import time

import click
from hera_display_games.core import mechanics, sprites, keymapper

begin = time.time()


class Player(sprites.RigidSprite):
    def encounter(self, other, prev_loc):
        if other.id == "target":
            print("YOU WIN!")
            print("TIME TAKEN: %.1fsec" % (time.time() - begin))
            sys.exit()
        super().encounter(other, prev_loc)


BROWN = (139, 69, 19)


@click.command()
@click.option(
    "-x",
    "-X",
    "--use-screen/--use-board",
    default=False,
    help="whether to use the physical HERA board",
)
def main(use_screen):
    wall_sprites = []
    for i in range(20):
        wall_sprites.append(sprites.RigidSprite([2 + i, i], color=BROWN, id="wall"))
    for i in range(20):
        wall_sprites.append(sprites.RigidSprite([i, i + 1], color=BROWN, id="wall"))

    player = Player([0, 0], color=(150, 0, 0), id="player")
    target = sprites.RigidSprite([20, 20], color=(0, 150, 0), id="target")

    if not use_screen:
        my_board = mechanics.Board(sprites=wall_sprites + [player, target])
    else:
        my_board = mechanics.VirtualBoard(sprites=wall_sprites + [player, target])
    my_board.draw()

    device = keymapper.get_gamepad()
    loop = asyncio.get_event_loop()

    while True:
        response = loop.run_until_complete(keymapper.map_movement(device))
        if response in ["ul", "ur", "dl", "dr", "r", "l"]:
            my_board.move_sprite(player, response)
            my_board.draw()
