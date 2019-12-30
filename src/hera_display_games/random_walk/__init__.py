#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple simulation of a random walk"""
import click
from hera_display_games.core import mechanics, sprites
import time
import random


@click.command()
@click.option("-s", "--speed", type=float, default=1, help="Speed of sprite")
@click.option("-n", "--nsprites", type=int, default=1, help="number of sprites")
@click.option("-e/-E", "--eat/--rigid", default=True, help="whether sprites eat each other")
@click.option(
    "-x",
    "-X",
    "--use-screen/--use-board",
    default=False,
    help="whether to use the physical HERA board",
)
def main(speed, nsprites, eat, use_screen):
    if not 1 <= nsprites <= 6:
        raise ValueError("nsprites must be between 1 and 6")

    if not 1 <= speed <= 100:
        raise ValueError("speed must be between 1 and 100")

    cls = sprites.HungrySprite if eat else sprites.RigidSprite
    my_sprites = []
    for i in range(nsprites):
        my_sprites.append(
            cls(
                [0, i],
                color=(
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                ),
                id=i,
            )
        )

    if not use_screen:
        my_board = mechanics.Board(sprites=my_sprites)
    else:
        my_board = mechanics.VirtualBoard(sprites=my_sprites)

    my_board.draw()

    directions = ["r", "l", "dl", "dr", "ur", "ul"]

    while True:
        for sprite in my_board.sprites:
            my_board.move_sprite(sprite, random.choice(directions))

        my_board.draw()
        time.sleep(1.0 / speed)
