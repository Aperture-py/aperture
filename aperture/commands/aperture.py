from .command import Command
from PIL import Image
import os, ntpath, math
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

#TODO: Make this do something
DEFAULT_RESOLUTIONS = [(200, 200), (500, 500)]
DEFAULT_QUALITY = 75
DEFAULT_DIR = os.getcwd()

#Default directory is current working directory

# Supported formats may be found here: http://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
from ..util.files import get_file_paths_from_inputs
from ..util.directories import get_output_path


class Aperture(Command):
    """
    'format' command.
    """

    def run(self):

        # Pipeline:

        # 1. Process inputs
        # - there should be a single function that gets the list of input paths
        inputs = self.options['<inputs>']
        inputs = get_file_paths_from_inputs(inputs)
        print("Inputs after: ", inputs)

        # 2. Process options dictionary
        # a. Process output location
        # - there should be a single function that returns an output path
        out_path = self.options['-o']
        out_path = get_output_path(out_path)

        print("Output path after: ", out_path)
        # b. Process options that affect the actual images (should be moved to a de-serlization function)
        resolutions = self.options['-r']
        quality = self.options['-c']
        verbose = self.options['--verbose']

        try:
            quality = DEFAULT_QUALITY if quality is None else int(quality)
        except ValueError:
            print(
                'E: Supplied quality value \'{}\' is not valid. Quality must be an integer between 0 and 100. Using default value instead'.
                format(quality))
            quality = DEFAULT_QUALITY

        if resolutions is None or not resolutions:
            resolutions = DEFAULT_RESOLUTIONS
        else:
            temp = []
            for res in resolutions:
                try:
                    w, h = res.lower().split('x')
                    r = (int(w), int(h))
                    temp.append(r)
                except ValueError:
                    print(
                        'E: Supplied resolution \'{}\' is not valid. Resolutions must be in form \'-r <width>x<height>\''.
                        format(res))
            resolutions = temp
            if not resolutions:
                print(
                    'E: All supplied resolution were invalid. Images will not be resized'
                )

        # 3. Image processing

        # - apply options to each image
        for path in inputs:
            img = Image.open(path)
            filename, extension = os.path.splitext(ntpath.split(path)[1])
            out_file = os.path.join(out_path, filename + "_cmprsd" + extension)
            save_image(img, out_file, quality)

            if verbose:
                size_comp = get_size_comparisson(path, out_file)
                old_size = size_comp[0]
                new_size = size_comp[1]
                print('\t{} ({}) -> {} ({}) [{} saved]'.format(
                    path, bytes_to_readable(old_size), out_file,
                    bytes_to_readable(new_size),
                    bytes_to_readable(old_size - new_size)))

    # 4. Save


def save_image(img, out_file, quality):
    img.save(out_file, optimize=True, quality=quality)


def get_size_comparisson(old_path, new_path):
    old_size = os.path.getsize(old_path)
    new_size = os.path.getsize(new_path)
    return (old_size, new_size)


##############################################################
# From an integer of bytes, convert to human readable format
# and return a string.
##############################################################
def bytes_to_readable(bytes):
    if bytes < 0:
        return '<0 bytes'
    else:
        mem_sizes = ('bytes', 'KB', 'MB', 'GB', 'TB')
        level = math.floor(math.log(bytes, 1024))
        return '{:.2f} {}'.format(bytes / 1024**level, mem_sizes[level])
