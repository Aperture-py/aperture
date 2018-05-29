# Main driver for the Aperture cli.

# DO NOT REMOVE - docopt uses the below docstring to describe the Aperture interface
# ===========================================================================
"""

Usage:
  aperture [<inputs>...] [-o <opath>] [-c <qual>] [-r <res>...] [--verbose]

Options:
  -h --help                     Show help.
  -v --version                  Show version.
  -o <opath>                    Output directory for formatted images.
  -r <res>...                   Desired resolutions for output images.
  -c <qual>                     Quality of output images [0-100]. Lower number means lower quality but smaller files. Larger number means higher quality but larger files. [default: 75]
  --verbose                     Verbosity, show what is happening under the hood
  
Examples:
  aperture [<inputs>...] [-o <opath>] [-c <qual>] [-r <res>...] [--verbose]

Help:
  For help using this tool...
"""
# ===========================================================================

from docopt import docopt
from aperture.options import deserialize_options

# Aperture imports
# How this version was chosen - https://packaging.python.org/tutorials/distributing-packages/#choosing-a-versioning-scheme
__version__ = '0.0.0dev1'

import aperture.commands


def main():
    options = docopt(__doc__, version=__version__)
    options_ds = deserialize_options(options)
    ap = aperture.commands.Aperture(options_ds)
    ap.run()


if __name__ == '__main__':
    main()
