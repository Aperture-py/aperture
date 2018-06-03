# Main driver for the Aperture cli.

# docopt uses the below docstring to describe the Aperture interface
'''
Aperture

Usage:
  aperture <input>... [options]

Options:
  -o <opath>, --outpath <opath>     Pass output location for the processed images.
  -q <qual>, --quality <qual>       Pass quality level applied to each image. [default: 75]
  -r <res>, --resolutions <res>     Pass set of resolutions applied to each image.
  -m <depth>, --max-depth <depth>   Maximum recursion depth for directory traversal. [default: 0]
  -v --verbose                      Output real-time processing statistics.

Examples:
  aperture .
  aperture . -o .
  aperture images/ -o out/ -q 80
  aperture images/ -o out/ -r 400x400
  aperture images/ -o out/ -r "800x800 400x400 200x200" -q 60 -v

Help:
  <inputs>  Must be: .jpg .jpeg .png
'''

from docopt import docopt, DocoptExit
from aperture.options import deserialize_options
import aperture.config_file as conf
import aperture.errors as errors
import sys

# Aperture imports
# How this version was chosen - https://packaging.python.org/tutorials/distributing-packages/#choosing-a-versioning-scheme
__version__ = '0.0.0dev1'

import aperture.commands


def main():
    try:
        options = docopt(__doc__, version=__version__)
    except DocoptExit:
        # Always print entire docopt if you enter just 'aperture', instead of just showing usage patterns.
        print(__doc__)
    else:
        config = conf.read_config()
        options_ds = deserialize_options(options, config)
        ap = aperture.commands.Aperture(options_ds)
        ap.run()


def run_main():
    '''Main driver for aperture.'''
    try:
        sys.exit(main())
    except errors.ApertureError as e:
        sys.stderr.write('aperture: ' + str(e) + '\n')
        sys.exit(1)


if __name__ == '__main__':
    run_main()
