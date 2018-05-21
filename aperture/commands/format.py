from .command import Command
from PIL import Image
import os, ntpath
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


class Format(Command):
    """
    'format' command.
    """

    def run(self):
        #TODO: Make this do something
        DEFAULT_RESOLUTIONS = [(200, 200), (500, 500)]
        DEFAULT_QUALITY = 75
        #Default directory is current working directory
        DEFAULT_DIR = os.getcwd()
        DEFAULT_RECURSION_DEPTH = 0
        MAX_RECURSTION_DEPTH = 10

        # TODO: Fix this to read from cmd-line
        recursionDepth = DEFAULT_RECURSION_DEPTH

        # Supported formats may be found here: http://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
        SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.gif', '.png')

        #If no input files or directories are provided, use cwd
        #   NOTE: Should we require some sort of explicit information '.' instead of assuming working directory?
        inputs = self.options['<inputs>']
        inputs = DEFAULT_DIR if inputs is None or not inputs else inputs

        #If no output directory is provided, or supplied dir is invalid, use cwd
        out_path = self.options['-o']
        if out_path is None:
            out_path = DEFAULT_DIR
        elif not os.path.isdir(out_path):
            print(
                'E: Either the directory \'{}\' does not exist, or a file was provided. Using cwd instead'.
                format(out_path))
            out_path = DEFAULT_DIR

        quality = self.options['-c']
        try:
            quality = DEFAULT_QUALITY if quality is None else int(quality)
        except ValueError:
            print(
                'E: Supplied quality value \'{}\' is not valid. Quality must be an integer between 0 and 100. Using default value instead'.
                format(quality))
            quality = DEFAULT_QUALITY

        resolutions = self.options['-r']
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

        ##################################
        # This is the meat of this command
        ##################################
        for path in inputs:
            extension = os.path.splitext(path)[1]

            if extension == '':
                # NOTE: output flag -o does not work with this right now
                try:
                    #Gets all files (and only files) from supplied path and subdirectories recursively up to a given depth
                    files = getFilesRecursively(path, recursionDepth)

                    for current_file in files:
                        extension = os.path.splitext(current_file)[1]
                        if extension.lower() in SUPPORTED_EXTENSIONS:
                            compress(current_file, out_path, quality)
                except FileNotFoundError:
                    print('E: could not locate directory \'{}\''.format(path))

            elif extension.lower() in SUPPORTED_EXTENSIONS:
                try:
                    compress(path, out_path, quality)
                except FileNotFoundError:
                    print('E: unable to locate file \'{}\''.format(path))
            else:
                print('E: unsupported filetype \'{}\''.format(path))


# TODO: possibly keep track of file size before and after and display this with maybe a `--verbose` option
def compress(path, out_path, quality):
    # NOTE: not sure if we need ntpath, depends on windows
    # *** Pretty sure we do b/c w/o it, filename would be the full path + filename ***
    filename, extension = os.path.splitext(ntpath.split(path)[1])
    img = Image.open(path)
    img.save(
        os.path.join(out_path, filename + "_cmprsd" + extension),
        optimize=True,
        quality=quality)


##############################################################
# Returns paths to all files from a provided path. Recursively
# traverses subdirectories up to a given depth, retrieving
# files from those directories as well.
##############################################################
def getFilesRecursively(path, maxdepth):
    matches = []

    def do_scan(start_dir, output, depth=0):
        #Using scandir here instead of listdir. They do the same thing but
        # scandir has fewer stat() calls and so is much faster
        for entry in os.scandir(start_dir):
            if entry.is_dir(follow_symlinks=False):
                if depth < maxdepth:
                    do_scan(entry.path, output, depth + 1)
            else:
                output.append(entry.path)

    do_scan(path, matches, 0)
    return matches
