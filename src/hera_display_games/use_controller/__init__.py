#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""hello please"""

import numpy as np
import asyncio
from hera_display_games.core import board, keymapper, sprites
import click


async def recolor(sprite):
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


async def update_board(board, speed=10.0):
    while True:
        await asyncio.sleep(1.0 / speed)
        board.draw()


# event loop and other code adapted from
# https://github.com/AlexElvers/pygame-with-asyncio
def pygame_event_loop(loop, event_queue):
    import pygame

    while True:
        event = pygame.event.wait()
        asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)


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
    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()

    if not use_screen:
        my_board = board.Board(sprites=[my_sprite])
    else:
        my_board = board.VirtualBoard(sprites=[my_sprite])
    my_board.draw()

    if input == "gamepad":
        device = keymapper.GamePad()
    elif input == "keyboard":
        device = keymapper.KeyBoardArrows(queue=event_queue)
        pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
    else:
        raise ValueError("incorrect input")

    color_task = asyncio.ensure_future(recolor(my_sprite))
    move_task = asyncio.ensure_future(move_sprite(device, my_board, my_sprite))
    board_task = asyncio.ensure_future(update_board(my_board))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if input == "keyboard":
            pygame_task.cancel()
        color_task.cancel()
        move_task.cancel()
        board_task.cancel()
        loop.stop()
