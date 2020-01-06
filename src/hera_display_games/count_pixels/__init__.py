#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple simulation of a random walk"""
import click
from hera_display_games.core import board, map_dict, sprites
import time


@click.command()
@click.option("-s", "--speed", type=float, default=1, help="Speed of sprite")
@click.option(
    "-x",
    "-X",
    "--use-screen/--use-board",
    default=False,
    help="whether to use the physical HERA board",
)
def main(speed, use_screen):
    if not 1 <= speed <= 100:
        raise ValueError("speed must be between 1 and 100")

    sprite = sprites.RigidSprite([0, 0])

    if not use_screen:
        my_board = board.Board(sprites=[sprite])
    else:
        my_board = board.VirtualBoard(sprites=[sprite])

    my_board.draw()

    for i in range(my_board.npixels):
        my_board.move_sprite(sprite, i)
        my_board.draw()
        time.sleep(1.0 / speed)
