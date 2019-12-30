try:
    import neopixel

    HAVE_NEOPIXEL = True
except ImportError:
    HAVE_NEOPIXEL = False

import math
import time
from abc import ABC, abstractmethod

import pygame

from . import map_dict

led_map = map_dict.led_map
# LED strip configuration:
LED_COUNT = 320  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 55  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

DIR_DICT = {
    "ul": [0, 1],
    "ur": [1, 1],
    "r": [1, 0],
    "dr": [0, -1],
    "dl": [-1, -1],
    "l": [-1, 0],
}


class OutOfBoundsError(Exception):
    pass


class SpriteCollision(Exception):
    pass


class Sprite:
    """Class for sprites."""

    def __init__(self, location=[0, 0], color=[0, 255, 0]):
        """Init for sprites."""
        self.location = location
        self.color = color

    def move(self, direction):
        try:
            self.location[0] += DIR_DICT[direction][0]
            self.location[1] += DIR_DICT[direction][1]
        except KeyError:
            raise ValueError("Direction not understood!")

    def goto(self, loc):
        """Move pixel to given loc. If loc is integer, go to that pixel *number*.
        If tuple, describes an x,y location."""
        if type(loc) == int:
            self.location[0] = map_dict.reverse_led_map[loc][0]
            self.location[1] = map_dict.reverse_led_map[loc][1]
        else:
            if len(loc) != 2:
                raise ValueError("loc should be a 2-tuple!")
            self.location = loc


class _BoardBase(ABC):
    """Class for a generic hexagonal board. Can be used either for a virtual board
    or a hardware board with LEDS."""

    def __init__(self, sprites=None, bg=None):
        """Init for the board."""

        self.sprites = sprites or []
        self.last_locs = [sp.location.copy() for sp in self.sprites]

        self.strip = self.make_strip()
        self.strip.begin()

        if bg is not None:
            self.bg = bg
        else:
            # Fill in with "off"
            self.bg = {key: [0, 0, 0] for key in led_map.keys()}
        self.clear()
        self.draw_background()

    @abstractmethod
    def make_strip(self):
        """Initialize a Strip object that deals with the actual pixel colours."""
        pass

    def set_pix(self, loc, rgb):
        """Set pixel color for location and rgb"""
        try:
            if led_map[tuple(loc)] != "dead":
                self.strip.setPixelColorRGB(led_map[tuple(loc)], rgb[0], rgb[1], rgb[2])
        except KeyError:
            raise OutOfBoundsError()

    def clear(self):
        """Turn off all LEDs"""
        for i in range(LED_COUNT):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
        self.strip.show()

    def draw_background(self):
        """Draw the background"""
        for loc in self.bg.keys():
            self.set_pix(loc, self.bg[loc])
        self.strip.show()

    def draw(self):
        """Draw the board and update the display"""
        # Update previous position of sprite with the background
        for loc in self.last_locs:
            self.set_pix(loc, self.bg[tuple(loc)])
        for i, sp in enumerate(self.sprites):
            # If the current sprite tries to move to the location of another
            # sprite, don't let it
            for sp_other in self.sprites[:i]:
                if sp.location == sp_other.location:
                    sp.location = self.last_locs[i]
            # Also don't let the sprite go out of the bounds of the board
            try:
                self.set_pix(sp.location, sp.color)
            except OutOfBoundsError:
                sp.location = self.last_locs[i]
                # Flash red if it can't move any further
                self.set_pix(sp.location, [155, 0, 0])
                self.strip.show()
                time.sleep(0.5)
                self.set_pix(sp.location, sp.color)
        self.last_locs = [sp.location.copy() for sp in self.sprites]
        self.strip.show()


class PyGameStrip:
    """Virtual LED strip made with pygame"""

    antenna_size = 10
    n_ants_per_side = 12  # including the middle dead strip
    y_up = math.cos(math.pi / 3) * antenna_size
    x_right = math.sin(math.pi / 3) * antenna_size

    def begin(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))

        self.grid_corners = self._make_grid()

        print(self.grid_corners)
        self.antenna_polygons = {}
        for pixel, corner in self.grid_corners.items():
            self.antenna_polygons[pixel] = pygame.draw.polygon(
                self.screen, [220, 220, 220], self._get_corners_from_left_corner(corner)
            )

    def _get_corners_from_left_corner(self, left_corner):
        """Left corner is the (x,y) tuple specifying the left corner coord in pixels."""
        x, y = left_corner
        return [
            left_corner,
            (x + self.x_right, y - self.y_up),
            (x + 2 * self.x_right, y),
            (x + 2 * self.x_right, y + self.antenna_size),
            (x + self.x_right, y + self.antenna_size + self.y_up),
            (x, y + self.antenna_size),
        ]

    def _make_grid(self):
        positions = {}
        for pixel, coord in map_dict.reverse_led_map.items():
            positions[pixel] = (
                coord[0] * (self.antenna_size + 2 * self.x_right)
                - coord[1] * (self.antenna_size + self.x_right),
                coord[1] * self.y_up,
            )

        return positions

    def setPixelColorRGB(self, pix_num, *rgb):
        self.antenna_polygons[pix_num] = pygame.draw.polygon(
            self.screen, rgb, self._get_corners_from_left_corner(self.grid_corners[pix_num])
        )

    def show(self):
        pygame.display.flip()


class Board(_BoardBase):
    """The standard hardware board"""

    def __init__(self, *args, **kwargs):
        if not HAVE_NEOPIXEL:
            raise ImportError(
                "You need to have the neopixel package installed to use the default board! You "
                "can still use the VirtualBoard."
            )

    def make_strip(self):
        return neopixel.Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
        )


class VirtualBoard(_BoardBase):
    def make_strip(self):
        return PyGameStrip()
