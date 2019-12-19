#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""A Module to map key inputs."""

import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
