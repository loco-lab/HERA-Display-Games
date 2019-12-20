# hera-display-games
Games to be played on the HERA display

## Installation

It's not quite simply pip-installable, because you need to install `neopixel`,
which is kinda tricky.

## How to run our test scripts
The environment on the pi is really weird...

`source ~/Hera_games_env/bin/activate`

To run simple scripted movement:

`sudo /home/hera-led/Hera_games_env/bin/python scripts/test_movement`

`sudo /home/hera-led/Hera_games_env/bin/python muck_around/test_controler_input`

## How to write/add more games/simulations

There are two ways to add more games. The first is to write a new scripts in `scripts/`
and then add its name to the `scripts = ` keywords in `setup.cfg`.

The better long-term way is to create a new sub-package of `hera_display_games`, and
write the game loop in a function, then add a name and point to that function in
the `entry_points` keyword in `setup.cfg`.
