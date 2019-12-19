import numpy as np
import neopixel
import time
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
    "ul": np.array([0, 1]),
    "ur": np.array([1, 1]),
    "r": np.array([1, 0]),
    "dr": np.array([0, -1]),
    "dl": np.array([-1, -1]),
    "l": np.array([-1, 0]),
}


class OutOfBoundsError(Exception):
    pass


class SpriteCollision(Exception):
    pass


class Sprite:
    """Class for sprites."""

    def __init__(self, location=np.array([0, 0]), color=[0, 255, 0]):
        """Init for sprites."""
        self.location = location
        self.color = color

    def move(self, direction):
        try:
            self.location += DIR_DICT[direction]
        except KeyError:
            raise ValueError("Direction not understood!")


class Board:
    """Class for the board."""

    def __init__(self, sprites=[], bg=None):
        """Init for the board."""
        self.sprites = sprites
        self.last_locs = [sp.location.copy() for sp in self.sprites]
        self.strip = neopixel.Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
        )
        if bg is not None:
            self.bg = bg
        else:
            # Fill in with "off"
            self.bg = {key: [0, 0, 0] for key in led_map.keys()}
        self.strip.begin()
        self.draw_background()

    def set_pix(self, loc, rgb):
        """Set pixel color for location and rgb"""
        try:
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
                time.sleep(0.5)
                self.set_pix(sp.location, sp.color)
        self.last_locs = [sp.location.copy() for sp in self.sprites]
        self.strip.show()
