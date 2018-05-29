from .command import Command
from PIL import Image
import os, ntpath, math, platform, re
"""
NOTES:

We can manipulate:
# Directories #
1. Provide no arg's. Converts all images in current directory and saves in current directory
2. Provide just 1-? input directories (space delimited). Converts all images in input directories and saves them in current directory
3. Provide just output directory. Converts all images in current directory and saves them in output directory
4. Provide in/out directories. Convers all images in input directories and saves them in output directory

# Files #
1. Provide 1-? input images (space delimited). Convert them and save in current directory
2. Provide 1-? input images (space delimited) and output directory. Convert input images and save in output directory

*Currently, allows any number of input files and/or directories. 
    -Files will be formatted individually (DONE)
    -Directories will be searched for images and all discovered images will be formatted (TO BE DONE) 

Can also take in:
-r : Desired output resolutions (WxH, space delimited, and each one MUST come after a '-r')
    e.g. "... -r 200x200 -r 400x400 -r 1000x1000 ..."
-c : Whether or not to compress. ('###' can be 0 to 100. Represents desired output quality)

##### Possible formats for cmd-line args #####
(MY FAV AND HOW IT IS CURRENTLY) aperture format [<inputs>...] [-o <opath>] [-c <qual>] [-r <res>...]
    -Accepts any number of space delimited input files and/or directories
(NOT MY FAV BUT STILL GOOD) aperture format [-f <ifiles>...|-d <ipath>] [-o <opath>] [-r <res>...] [-c <qual>]
    -Accepts and number of files ***OR*** directories based on provided flag.
    -Each file must come after a '-f' flag and each dir must come after a '-d' flag. 

"""

from ..util.files import get_file_paths_from_inputs, get_file_size_comparisson, bytes_to_readable
from ..util.directories import get_output_path


class Aperture(Command):
    """
    'format' command.
    """

    def run(self):

        # Pipeline:

        # 1. Process inputs
        # - there should be a single function that gets the list of input paths
        inputs = self.options['inputs']

        # 2. Process options dictionary
        # a. Process output location
        # - there should be a single function that returns an output path
        out_path = self.options['output']

        # b. Process options that affect the actual images (should be moved to a de-serlization function)
        quality = self.options['quality']
        resolutions = self.options['resolutions']
        verbose = self.options['verbose']

        # 3. Image processing

        # - apply options to each image
        for path in inputs:
            img = Image.open(path)
            filename, extension = os.path.splitext(ntpath.split(path)[1])
            out_file = os.path.join(out_path, filename + "_cmprsd" + extension)

            save_image(img, out_file, quality)

            if verbose:
                size_comp = get_file_size_comparisson(path, out_file)
                old_size = size_comp[0]
                new_size = size_comp[1]
                print('\t{} ({}) -> {} ({}) [{} saved]'.format(
                    path, bytes_to_readable(old_size), out_file,
                    bytes_to_readable(new_size),
                    bytes_to_readable(old_size - new_size)))

        # 4. Save


def save_image(img, out_file, quality):
    img.save(out_file, optimize=True, quality=quality)
