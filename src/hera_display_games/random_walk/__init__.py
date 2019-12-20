#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple simulation of a random walk"""
import click
from hera_display_games.core import mechanics
import time
import random


@click.command()
@click.option("-s", "--speed", type=float, help="Speed of sprite")
@click.option("-n", "--nsprites", type=int, help="number of sprites")
def main(speed, nsprites):
    if not 1 <= nsprites <= 6:
        raise ValueError("nsprites must be between 1 and 6")

    if not 1 <= speed <= 100:
        raise ValueError("speed must be between 1 and 100")

    my_sprites = []
    for i in range(nsprites):
        my_sprites.append(mechanics.Sprite([0, i]))

    my_board = mechanics.Board(sprites=my_sprites)
    my_board.draw()

    directions = ["r", "l", "dl", "dr", "ur", "ul"]

    while True:
        for sprite in my_sprites:
            sprite.move(random.choice(directions))

        my_board.draw()
        time.sleep(1.0 / speed)
