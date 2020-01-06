"""Module defining a high-level Game class to be inherited by any particular game."""

import asyncio

from . import keymapper


async def update_board(board, refresh_rate):
    while True:
        await asyncio.sleep(refresh_rate)
        board.draw()


class Game:
    """A high-level game class."""

    def __init__(self, board, device, movers, refresh_rate=0.05):
        self.board = board

        self.loop = asyncio.get_event_loop()
        self.event_queue = asyncio.Queue()

        if device is not None:
            if device == "gamepad":
                self.device = keymapper.GamePad()
            elif device == "keyboard":
                self.device = keymapper.KeyBoardArrows(queue=self.event_queue)
                self._pygame_task = self.loop.run_in_executor(
                    None, self.device.pygame_event_loop, self.loop, self.event_queue
                )
            else:
                raise ValueError("incorrect input")

        self.movers = movers

        self.mover_tasks = []
        for mover in self.movers:
            self.mover_tasks.append(asyncio.ensure_future(mover(self.device, self.board)))

        self.mover_tasks.append(asyncio.ensure_future(update_board(self.board, refresh_rate)))

    def run(self):
        """Actually run the game."""
        self.board.draw()

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            if isinstance(self.device, keymapper.KeyBoardArrows):
                self._pygame_task.cancel()
            for task in self.mover_tasks:
                task.cancel()
            self.loop.stop()
