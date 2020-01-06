#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""A Module to map key inputs."""

import evdev
from evdev import ecodes
import asyncio
from abc import ABC, abstractmethod

try:
    import pygame

    HAVE_PYGAME = True
except ImportError:
    HAVE_PYGAME = False


class Device(ABC):
    @abstractmethod
    def get_next_movement(self):
        """
        Returns a human-readable output given *single* device press.

        Returns
        -------
        tuple :
            First element is a string giving the button that was pressed/released.
            The second element is an int: 1 for press, 0 for release.
            Note: if the thing that is released is any button on the DPAD, the first
            element will be None.
        """
        pass


class EvDevDevice(Device):
    def __init__(self):
        self.device = self.get_device()

    @abstractmethod
    def is_this_device(self, device):
        pass

    def get_device(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        for device in devices:
            if self.is_this_device(device):
                mydevice = device
                print("Using device: ", device.path, device.name, device.phys)
                break

        try:
            device = mydevice
        except (NameError, UnboundLocalError):
            for device in devices:
                print(device.path, device.name, device.phys)
            raise IOError("Couldn't find gamepad device")

        return device


class GamePad(EvDevDevice):
    def is_this_device(self, device):
        return "gamepad" in device.name

    async def get_next_movement(self):
        async for event in self.device.async_read_loop():
            cat = event.type

            # EV_ABS seems like its the type for direction pressing
            if cat == ecodes.EV_ABS:
                if ecodes.ABS[event.code] == "ABS_Y":
                    if event.value == 0:
                        return "u", 1
                    elif event.value == 255:
                        return "d", 1
                    else:
                        return None, 0  # 'release'
                else:
                    if event.value == 0:
                        return "l", 1
                    elif event.value == 255:
                        return "r", 1
                    else:
                        return None, 0  # 'release'

            # EV_KEY seems like any other kind of key.
            elif cat == ecodes.EV_KEY:
                if type(ecodes.BTN[event.code]) == list:
                    return "x", event.value
                return (
                    {
                        "BTN_BASE3": "select",
                        "BTN_BASE4": "start",
                        "BTN_TOP": "y",
                        "BTN_THUMB2": "b",
                        "BTN_THUMB": "a",
                        "BTN_BASE": "r-trigger",
                        "BTN_TOP2": "l-trigger",
                    }[ecodes.BTN[event.code]],
                    event.value,
                )


class KeyBoardArrows(Device):
    def __init__(self, init=False, queue=None):
        if not HAVE_PYGAME:
            raise ImportError("YOu can't use keyboard without pygame")
        if init:
            pygame.display.init()
            pygame.display.set_mode((300, 300))
        if queue is not None:
            self.set_event_queue(queue)

    def set_event_queue(self, queue):
        self.event_queue = queue

    async def get_next_movement(self):
        while True:
            event = await self.event_queue.get()
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    return "d", 1
                elif event.key == pygame.K_UP:
                    return "u", 1
                elif event.key == pygame.K_LEFT:
                    return "l", 1
                elif event.key == pygame.K_RIGHT:
                    return "r", 1
                elif event.key == pygame.K_a:
                    return "l-trigger", 1
                elif event.key == pygame.K_d:
                    return "r-trigger", 1
                else:
                    return event.key, 1

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                    return None, 0
                else:
                    return event.key, 0

    @staticmethod
    def pygame_event_loop(loop, event_queue):
        """
        event loop and other code adapted from
        https://github.com/AlexElvers/pygame-with-asyncio
        """
        while True:
            event = pygame.event.wait()
            asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)


async def map_movement(device):
    """Return human readable movement condition based on input.

    Returns
    -------
    str :
        Either 'ul', 'ur', 'dl', 'dr', 'l' or 'r'
    """

    while True:
        val, state = await device.get_next_movement()

        # Releasing doesn't do anything yet.
        if not state:
            continue

        while val in "ud":
            newval, newstate = await device.get_next_movement()

            if not newstate:
                continue

            if newval in "lr":
                return f"{val}{newval}"
            elif newval == val:
                continue
            elif newval in "ud":
                break
            else:
                return newval

        if val not in "ud":
            return val


if __name__ == "__main__":
    device = KeyBoardArrows(init=True)  # GamePad()
    loop = asyncio.get_event_loop()
    while True:
        response = loop.run_until_complete(map_movement(device))
        print(response)
