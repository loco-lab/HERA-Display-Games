import asyncio
import random

import click
from hera_display_games.core import sprites, map_dict, board, keymapper
import copy


class Snake(sprites.Sprite):
    def __init__(self, *args, direction="ul", speed=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_location = copy.copy(self.location)
        self.initial_pixels = self.pixels
        self.direction = direction
        self.initial_direction = copy.copy(direction)
        self.speed = speed

    def encounter(self, other, prev_loc):
        if isinstance(other, Apple):
            self.grow(prev_loc)
            self.speed += 1
            while other.location in self.pixels:
                other.location = random.choice(list(map_dict.reverse_led_map.values()))
                other.pixels = [other.location]

        elif other is self:
            self.die()
        else:
            raise ValueError("Something went wrong.")

        return True

    def grow(self, prev_loc):
        self.pixels.append(prev_loc[-1])

    def move(self, movement):
        try:
            self.location = (
                self.location[0] + sprites.DIR_DICT[movement][0],
                self.location[1] + sprites.DIR_DICT[movement][1],
            )

        except KeyError:
            raise ValueError("That was a bad string for movement")

        self.pixels = [self.location] + self.pixels[:-1]

        if any(loc not in map_dict.led_map for loc in self.pixels):
            raise sprites.OutOfBoundsError

    def die(self):
        self.location = copy.copy(self.initial_location)
        self.direction = self.initial_direction
        self.pixels = copy.copy(self.initial_pixels)

    def hit_boundary(self, prev_loc):
        self.die()


class Apple(sprites.RigidSprite):
    def __init__(self, location, color=(255, 0, 0), id="apple"):
        super().__init__(location=location, color=color, id=id)


async def move_sprite(device, snake):
    while True:
        response = await keymapper.map_movement(device)
        if response in ["ul", "ur", "dl", "dr", "r", "l"]:
            snake.direction = response


async def update_board(board, snake):
    while True:
        await asyncio.sleep(1.0 / snake.speed)
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

    snake = Snake(location=(0, 2), pixels=[(0, 2), (0, 1), (0, 0)], color=(0, 255, 0), id="snake")
    apple_loc = (0, 0)
    while apple_loc in snake.pixels:
        apple_loc = random.choice(list(map_dict.reverse_led_map.values()))
    apple = Apple(location=apple_loc)

    if not use_screen:
        my_board = board.Board(sprites=[snake, apple])
    else:
        my_board = board.VirtualBoard(sprites=[snake, apple])
    my_board.draw()

    if input == "gamepad":
        device = keymapper.GamePad()
    elif input == "keyboard":
        device = keymapper.KeyBoardArrows(queue=event_queue)
        pygame_task = loop.run_in_executor(None, pygame_event_loop, loop, event_queue)
    else:
        raise ValueError("incorrect input")

    move_task = asyncio.ensure_future(move_sprite(device, snake))
    board_task = asyncio.ensure_future(update_board(my_board, snake))

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
