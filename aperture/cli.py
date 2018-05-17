# Main driver for the Aperture cli.

# DO NOT REMOVE - docopt uses the below docstring to describe the Aperture interface
# ===========================================================================

"""

Usage:
  aperture format [<inputs>...] [-o <opath>] [-c <qual>] [-r <res>...]

Commands:
  format                        Format images.

Options:
  -h --help                     Show help.
  -v --version                  Show version.
  -o <opath>                    Output directory for formatted images.
  -r <res>...                   Desired resolutions for output images.
  -c <qual>                     Quality of output images [0-100]. Lower number means lower quality but smaller files. Larger number means higher quality but larger files. [default: 75]

Examples:
  aperture format [<inputs>...] [-o <opath>] [-c <qual>] [-r <res>...]

Help:
  For help using this tool...
"""
# ===========================================================================

from docopt import docopt
from inspect import getmembers, isclass

# Aperture imports
from .meta import __version__ as VERSION
import aperture.commands


def main():
    options = docopt(__doc__, version=VERSION)

    for (k, v) in options.items():
        # check if the entered command matches an instance of a command class
        if hasattr(aperture.commands, k) and v:
            module = getattr(aperture.commands, k)
            aperture.commands = getmembers(module, isclass)
            command = [
                command[1]
                for command in aperture.commands
                if command[0] != 'Command'
            ][0]
            command = command(options)
            command.run()  # run the command
