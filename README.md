# hera-display-games
Games to be played on the HERA display

## Installation

It's not quite simply pip-installable, because you need to install `neopixel`,
which is kinda tricky. Other than that,

`pip install [-e] .`

### If you're on the Pi
If you need to setup a raspberry pi with this, we recommend doing the following:

    $ pip install virtualenv
    $ virtualenv ~/<ENVNAME>
    $ source ~/<ENVNAME>/bin/activate
    $ pip install [-e] .

Then do the following (this will help later):

    $ echo "export VENV=~/<ENVNAME>/bin" >> ~/.bashrc

## How to run our test scripts

### If you're on the Raspberry-Pi
The environment on the pi is really weird.
Anything that requires actually accessing the physical HERA board requires sudo, and
unfortunately, there's no way to tell `sudo` that the `$PATH` has been modified to
include the virtualenv, so you have to specify the full path.

`source ~/<ENVNAME>/bin/activate`

To run simple scripted movement:

`sudo -E $VENV/random_walk`

or

`sudo -E $VENV/test_controler`

### If you're not on the pi
Just do `source ~/<ENVNAME>/bin/activate` and then you can easily call the script-name
from any directory, eg::

`$ random_walk -n 4`

## How to write/add more games/simulations

There are two ways to add more games. The first is to write a new scripts in `scripts/`
and then add its name to the `scripts = ` keywords in `setup.cfg`.

The better long-term way is to create a new sub-package of `hera_display_games`, and
write the game loop in a function, then add a name and point to that function in
the `entry_points` keyword in `setup.cfg`.
