from .command import Command
from PIL import Image
import glob, os, ntpath #EX: glob.glob("*.jpg") will get all files in current directory that are jpegs.

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
        DEFAULT_RESOLUTIONS = [(200,200), (500,500)] #TODO: Make this do something
        DEFAULT_QUALITY = 75
        DEFAULT_DIR = os.getcwd() #Default directory is current working directory

        # Supported formats may be found here: http://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
        SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.gif', '.png')

        #If no input files or directories are provided, use cwd
        #   NOTE: Should we require some sort of explicit information '.' instead of assuming working directory?
        inputs = self.options['<inputs>']
        inputs = DEFAULT_DIR if inputs is None or not inputs else inputs

        #If no output directory is provided, use cwd
        out_path = self.options['-o']
        out_path = DEFAULT_DIR if out_path is None else out_path

        quality = self.options['-c']
        quality = DEFAULT_QUALITY if quality is None else int(quality)

        resolutions = self.options['-r']
        resolutions = DEFAULT_RESOLUTIONS if resolutions is None or not resolutions else resolutions
        #NOTE: These resolutions will need to be parsed to remove 'x' char and to convert char's to int's

        for path in inputs:
            # NOTE: we only require the path here, no reason to declare unused variables and waste memory writes
            # This is ugly...
            #   NOTE: check if below works on windows and replace with that
            # extension = os.path.splittext(path)[1]
            extension = os.path.splitext(ntpath.split(path)[1])[1]

            if extension == '':
                # NOTE: output flag -o does not work with this right now
                # Apply recursive directory call
                try:
                    os.chdir(path)
                    files = os.listdir()
                    for current_file in files:
                        # NOTE: I implemented it this way rather than using glob so that way if we chose to include all filetypes that pillow 
                        # supports we wouldn't need write a call for each filetype. 
                        # This is subject to change if we agree that glob would be a better implementation.
                        extension = os.path.splitext(ntpath.split(current_file)[1])[1]
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
    filename, extension = os.path.splitext(ntpath.split(path)[1])
    img = Image.open(path)
    img.save(os.path.join(out_path, filename + "_cmprsd" + extension), optimize=True, quality=quality)
