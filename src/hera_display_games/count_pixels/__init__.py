#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple simulation of a random walk"""
import click
from hera_display_games.core import board, map_dict
import time
import random


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

    sprite = board.Sprite([0, 0])

    if not use_screen:
        my_board = board.Board(sprites=[sprite])
    else:
        my_board = board.VirtualBoard(sprites=[sprite])

    my_board.draw()

    max_pixel = max(map_dict.reverse_led_map.keys())
    for i in range(max_pixel):
        sprite.goto(i)
        my_board.draw()
        time.sleep(1.0 / speed)
