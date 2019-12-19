#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""A Module to map key inputs."""

import evdev
from evdev import ecodes


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
    for event in device.read_loop():
        cat = event.type
        if cat == ecodes.EV_ABS:
            if ecodes.ABS[event.code] == "ABS_Y":
                if event.value == 0:
                    return "u"
                elif event.value == 255:
                    return "d"
                else:
                    return None  # 'release'
            else:
                if event.value == 0:
                    return "l"
                elif event.value == 255:
                    return "r"
                else:
                    return None  # 'release'

        elif cat == ecodes.EV_KEY:
            return


#            print(ecodes.BTN[event.code])


def map_movement(device):
    """Return human readable movement condition based on input.

    Returns
    -------
    str :
        Either 'ul', 'ur', 'dl', 'dr', 'l' or 'r'
    """

    while True:
        val = get_next_movement(device)
        # unmapped key press
        if val is None:
            continue

        while val in "ud":
            newval = get_next_movement(device)

            if newval is None:
                continue

            if newval in "lr":
                return f"{val}{newval}"
            elif newval == val:
                continue
            elif newval:
                break
            else:
                continue

        if val in "lr":
            return val


if __name__ == "__main__":
    device = get_gamepad()
    print(evdev.ecodes.ABS)

    while True:
        print(map_movement(device))
