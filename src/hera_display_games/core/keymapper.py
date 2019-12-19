#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""A Module to map key inputs."""

import evdev
from evdev import ecodes
import asyncio


def get_gamepad():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device.path, device.name, device.phys)
        if "gamepad" in device.name:
            mydevice = device
            print("Using device: ", device.path, device.name, device.phys)
            break

    try:
        device = mydevice
    except NameError:
        raise IOError("Couldn't find gamepad device")

    return device


def get_next_movement(device):
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
    for event in device.read_loop():
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


async def map_movement(device):
    """Return human readable movement condition based on input.

    Returns
    -------
    str :
        Either 'ul', 'ur', 'dl', 'dr', 'l' or 'r'
    """

    while True:
        val, state = get_next_movement(device)

        # Releasing doesn't do anything yet.
        if not state:
            continue

        while val in "ud":
            newval, newstate = get_next_movement(device)

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
    device = get_gamepad()
    loop = asyncio.get_event_loop()
    while True:
        response = loop.run_until_complete(map_movement(device))
        print(response)
