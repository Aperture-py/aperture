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
import aperture.util.files as utl_f
import aperture.aperturelib as aptlib


class Aperture(Command):

    def run(self):
        """Runs the 'aperture' command.
        """

        options = self.options

        inputs = options['inputs']
        out_path = options['output']
        quality = options['quality']
        verbose = options['verbose']

        for path in inputs:
            # Send image through the pipeline
            image = Image.open(path)
            image_pipeline_results = pipeline_image(image, options)

            for image in image_pipeline_results:
                # Get the output path
                filename, extension = os.path.splitext(ntpath.split(path)[1])
                out_file = os.path.join(out_path,
                                        filename + "_cmprsd" + extension)
                # Save the image
                save_image(image, out_file, quality)

                # Print the results of the pipeline
                if verbose:
                    print_pipeline_results(path, out_file)


def pipeline_image(image, options):
    """Sends an image through a processing pipeline.

    Applies all (relevant) provided options to a given image.

    Args:
        image: An instance of a PIL Image.
        options: Options to apply to the image (i.e. quality and resolutions).

    Returns:
        A list containing instances of PIL Images. This list will always be length
        1 if no options exist that require multiple copies to be created for a single
        image (i.e resolutions).
    """
    results = []

    # resolutions = options['resolutions']
    #     for res in resolutions:
    #         img_res = aptlib.resize.resize_image(image.copy(), res, true)

    results.append(image)
    return results


def print_pipeline_results(orig_path, new_path):
    """Prints the results of the pipeline-ing process for a given image.

    Args:
        orig_path: The path to the original image.
        new_path: The path to the newly created image.
    """
    size_comp = utl_f.get_file_size_comparison(orig_path, new_path)
    old_size = size_comp[0]
    new_size = size_comp[1]
    print('\t{} ({}) -> {} ({}) [{} saved]'.format(
        orig_path, utl_f.bytes_to_readable(old_size), new_path,
        utl_f.bytes_to_readable(new_size),
        utl_f.bytes_to_readable(old_size - new_size)))


def save_image(img, out_file, quality):
    """Saves an instance of a PIL Image to the system.

    This is a wrapper for the PIL Image save function.

    Args:
        img: An instance of a PIL Image.
        out_file: Path to save the image to.
        quality: Quality to apply to the image.
    """
    img.save(out_file, optimize=True, quality=quality)
