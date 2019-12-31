#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""hello please"""

import numpy as np
import asyncio
from hera_display_games.core import mechanics, keymapper
import click


async def recolor(sprite, board):
    while True:
        await asyncio.sleep(5)
        sprite.color = np.random.randint(0, 255, size=3).tolist()
        board.draw()


async def move_sprite(device, sprite, board):
    while True:
        response = await keymapper.map_movement(device)
        if response in ["ul", "ur", "dl", "dr", "r", "l"]:
            sprite.move(response)
            board.draw()
        elif response in ["r-trigger", "l-trigger"]:
            sprite.color = np.random.randint(0, 255, size=3).astype(int).tolist()
            board.draw()


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
    my_sprite = mechanics.Sprite(np.array([0, 0]), color=[3, 137, 255])
    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()

    if not use_screen:
        my_board = mechanics.Board(sprites=[my_sprite])
    else:
        my_board = mechanics.VirtualBoard(sprites=[my_sprite])
    my_board.draw()

    if input == "gamepad":
        device = keymapper.GamePad()
    elif input == "keyboard":
        device = keymapper.KeyBoardArrows(queue=event_queue)
        pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
    else:
        raise ValueError("incorrect input")

    color_task = asyncio.ensure_future(recolor(my_sprite, my_board))
    move_tast = asyncio.ensure_future(move_sprite(device, my_sprite, my_board))

    # task1 = loop.create_task(recolor(my_sprite))
    # task2 = loop.create_task(keymapper.map_movement(device))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if input == "keyboard":
            pygame_task.cancel()
        color_task.cancel()
        move_tast.cancel()
        loop.stop()
