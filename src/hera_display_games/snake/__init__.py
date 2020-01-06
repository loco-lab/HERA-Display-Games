import asyncio
import random

import click
from hera_display_games.core import sprites, map_dict, board, keymapper
import copy


class Snake(sprites.Sprite):
    def __init__(self, *args, direction="ul", **kwargs):
        super(*args, **kwargs)
        self.initial_location = copy.copy(self.location)
        self.direction = direction
        self.initial_direction = copy.copy(direction)

    def encounter(self, other, prev_loc):
        if isinstance(other, Apple):
            self.grow(prev_loc)
            while other.location in self.pixels:
                other.location = random.choice(list(map_dict.reverse_led_map.values()))
        elif other is self:
            self.die()
        else:
            raise ValueError("Something went wrong.")

        return True

    def grow(self, prev_loc):
        pass
        # prev_pixels = [(x + prev_loc[0], y + prev_loc[1]) for x, y in self.region]

    def move(self, movement):
        current_pixels = self.pixels.copy()
        # prev_loc = self.location

        try:
            self.location = (
                self.location[0] + sprites.DIR_DICT[movement][0],
                self.location[1] + sprites.DIR_DICT[movement][1],
            )
        except KeyError:
            raise ValueError("That was a bad string for movement")
        # new_head = (0, 0)
        # new_body = self._region_from_loc_and_pixels(prev_loc, current_pixels[:-1])
        self.region = self._region_from_loc_and_pixels(self.loc, current_pixels[:-1])

    def die(self):
        self.location = self.initial_location
        self.direction = self.initial_direction

    def hit_boundary(self):
        self.die()


class Apple(sprites.RigidSprite):
    def __init__(self, location, color=(255, 0, 0), id="apple"):
        super().__init__(location=location, color=color, id=id)


async def change_direction(device, snake):
    while True:
        response = await keymapper.map_movement(device)
        if response in ["ul", "ur", "dl", "dr", "r", "l"]:
            snake.direction = response


async def update_board(board, snake, speed=10.0):
    while True:
        await asyncio.sleep(1.0 / speed)
        board.move_sprite(snake, snake.direction)
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
    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()

    if input == "gamepad":
        device = keymapper.GamePad()
    elif input == "keyboard":
        device = keymapper.KeyBoardArrows(queue=event_queue)
        pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
    else:
        raise ValueError("incorrect input")

    snake = Snake(location=(0, 2), region=[(0, 0), (0, -1), (0, -2)], color=(0, 255, 0), id="snake")
    apple = Apple(location=random.choice(list(map_dict.reverse_led_map.values())))

    if not use_screen:
        my_board = board.Board(sprites=[snake, apple])
    else:
        my_board = board.VirtualBoard(sprites=[snake, apple])
    my_board.draw()

    move_task = asyncio.ensure_future(change_direction(device, snake))
    board_task = asyncio.ensure_future(update_board(my_board))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if input == "keyboard":
            pygame_task.cancel()
        move_task.cancel()
        board_task.cancel()
        loop.stop()
