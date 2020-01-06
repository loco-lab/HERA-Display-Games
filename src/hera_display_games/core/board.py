try:
    import neopixel

    HAVE_NEOPIXEL = True
except ImportError:
    HAVE_NEOPIXEL = False

import math
from abc import ABC, abstractmethod

try:
    import pygame

    HAVE_PYGAME = True
except ImportError:
    HAVE_PYGAME = False

from . import map_dict
from .sprites import OutOfBoundsError


class _BoardBase(ABC):
    """Class for a generic hexagonal board. Can be used either for a virtual board
    or a hardware board with LEDS."""

    def __init__(self, sprites=None, bg=None):
        """Init for the board."""

        self.sprites = sprites or []
        self.last_locs = [sp.location.copy() for sp in self.sprites]

        self.moved_sprites = []

        self.strip = self.make_strip()
        self.strip.begin()

        if bg is not None:
            self.bg = bg
        else:
            # Fill in with "off"
            self.bg = {key: [0, 0, 0] for key in map_dict.led_map.keys()}
        self.clear()
        self.draw_background()

    @abstractmethod
    def make_strip(self):
        """Initialize a Strip object that deals with the actual pixel colours."""
        pass

    @abstractmethod
    @property
    def npixels(self):
        pass

    def set_pix(self, loc, rgb):
        """Set pixel color for location and rgb"""
        if map_dict.led_map[tuple(loc)] != "dead":
            self.strip.setPixelColorRGB(map_dict.led_map[tuple(loc)], rgb[0], rgb[1], rgb[2])

    def clear(self):
        """Turn off all LEDs"""
        for i in range(self.npixels):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
        self.strip.show()

    def draw_background(self):
        """Draw the background"""
        for loc in self.bg.keys():
            self.set_pix(loc, self.bg[loc])
        self.strip.show()

    def move_sprite(self, sprite, movement):
        prev_loc = sprite.location.copy()
        try:
            sprite.move(movement)
        except OutOfBoundsError:
            self.sprite_hit_boundary(sprite, prev_loc)

        # Check against other sprites.
        done = False
        while not done:
            done = True
            for other in self.sprites:
                if sprite is not other and sprite.location == other.location:
                    done = sprite.encounter(other, prev_loc,)
            self.kill_sprites()
        # Check against the borders.
        # also do logic like making it flash and stuff.
        if tuple(sprite.location) not in map_dict.led_map:
            sprite.move(prev_loc)

    def sprite_hit_boundary(self, sprite, prev_loc):
        """Decide on what to do if a sprite hits a boundary."""
        sprite.hit_boundary(prev_loc)

    def kill_sprites(self):
        self.sprites = [sprite for sprite in self.sprites if not sprite.dead]

    def draw(self):
        """Draw the board and update the display"""
        # Update previous position of sprite with the background
        for loc in self.last_locs:
            self.set_pix(loc, self.bg[tuple(loc)])

        for i, sp in enumerate(self.sprites):
            self.set_pix(sp.location, sp.color)

        self.last_locs = [sp.location.copy() for sp in self.sprites]
        self.strip.show()


class PyGameStrip:
    """Virtual LED strip made with pygame"""

    antenna_size = 20
    n_ants_per_side = 12  # including the middle dead strip
    y_up = math.cos(math.pi / 3) * antenna_size
    x_right = math.sin(math.pi / 3) * antenna_size

    max_x = max(x for x, y in map_dict.led_map.keys()) + 1
    max_y = max(y for x, y in map_dict.led_map.keys()) + 1

    zeroth_column_size = max(y for x, y in map_dict.led_map.keys() if x == 0)

    def begin(self):
        pygame.init()

        # Make screen size based on hexagon size.
        self.screen = pygame.display.set_mode(
            (
                int(self.x_right * 2 * self.max_x + self.antenna_size),
                int((self.antenna_size + self.y_up) * self.max_y + self.antenna_size + self.y_up),
            )
        )

        # Make full background black
        self.screen.fill((0, 0, 0))

        # A single corner from each "antenna" (bottom-left)
        self.grid_corners = self._make_grid()

        # Set pixel background colors to some kind of grey.
        for pixel, corner in self.grid_corners.items():
            pygame.draw.polygon(
                self.screen, [150, 150, 150], self._get_corners_from_left_corner(corner),
            )

        # Set pixel borders to darker grey.
        self.antenna_polygons = {}
        for pixel, corner in self.grid_corners.items():
            self.antenna_polygons[pixel] = pygame.draw.polygon(
                self.screen, [200, 200, 200], self._get_corners_from_left_corner(corner), 3
            )

        pygame.display.flip()

    def _get_corners_from_left_corner(self, left_corner):
        """Left corner is the (x,y) tuple specifying the left corner coord in pixels."""
        x, y = left_corner
        return [
            left_corner,
            (x + self.x_right, y + self.y_up),
            (x + 2 * self.x_right, y),
            (x + 2 * self.x_right, y - self.antenna_size),
            (x + self.x_right, y - self.antenna_size - self.y_up),
            (x, y - self.antenna_size),
        ]

    def _make_grid(self):
        positions = {}
        for pixel, coord in map_dict.reverse_led_map.items():
            positions[pixel] = (
                self.antenna_size / 2
                + self.zeroth_column_size * self.x_right
                + coord[0] * 2 * self.x_right
                - coord[1] * self.x_right,
                self.screen.get_size()[1]
                - self.antenna_size / 2
                - self.y_up
                - coord[1] * (self.y_up + self.antenna_size),
            )

        return positions

    def setPixelColorRGB(self, pix_num, *rgb):
        self.antenna_polygons[pix_num] = pygame.draw.polygon(
            self.screen, rgb, self._get_corners_from_left_corner(self.grid_corners[pix_num]), 3
        )

    def show(self):
        pygame.display.flip()


class Board(_BoardBase):
    """The standard hardware board"""

    # LED strip configuration:
    LED_COUNT = 320  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 55  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

    def __init__(self, *args, **kwargs):
        if not HAVE_NEOPIXEL:
            raise ImportError(
                "You need to have the neopixel package installed to use the default board! You "
                "can still use the VirtualBoard."
            )
        super().__init__(*args, **kwargs)

    def make_strip(self):
        return neopixel.Adafruit_NeoPixel(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL,
        )

    @property
    def npixels(self):
        return self.LED_COUNT


class VirtualBoard(_BoardBase):
    def __init__(self, *args, **kwargs):
        if not HAVE_PYGAME:
            raise ImportError(
                "You need to have the pygame package installed to use the virtual board! You "
                "can still use the default Board."
            )
        super().__init__(*args, **kwargs)

    def make_strip(self):
        return PyGameStrip()

    @property
    def npixels(self):
        return len(self.strip.grid_corners)
