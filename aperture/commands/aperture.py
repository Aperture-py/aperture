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
import aperture.aperturelib.resize as apt_resize


class Aperture(Command):

    def run(self):
        """Runs the 'aperture' command."""

        options = self.options

        inputs = options['inputs']
        out_path = options['output']
        quality = options['quality']
        verbose = options['verbose']

        for orig_path in inputs:
            # Send image through the pipeline
            image = Image.open(orig_path)
            image_pipeline_results = pipeline_image(image, options)

            for image_result in image_pipeline_results:
                # Get the output file path
                out_file = get_image_out_path(image_result, orig_path, out_path,
                                              options)

                # Save the image, apply quality LAST
                save_image(image_result, out_file, quality)

                # Print the results of the pipeline
                if verbose:
                    print_pipeline_results(orig_path, out_file)


def pipeline_image(image, options):
    """Sends an image through a processing pipeline.

    Applies all (relevant) provided options to a given image.

    Args:
        image: An instance of a PIL Image.
        options: Options to apply to the image (i.e. resolutions).

    Returns:
        A list containing instances of PIL Images. This list will always be length
        1 if no options exist that require multiple copies to be created for a single
        image (i.e resolutions).
    """
    results = []

    # Begin pipline

    # 1. Create image copies for each resolution

    resolutions = options['resolutions']  # List of resolution tuples
    for res in resolutions:
        img_rs = apt_resize.resize_image(image, res)  # Resized image

        # Add image to result set. This result set will be pulled from
        # throughout the pipelining process to perform more processing (watermarking).
        results.append(img_rs)

    # 2. Apply watermark to each image copy
    # TODO: Watermark images from results here.

    # Fallback: Nothing was done to the image
    if len(results) == 0:
        results.append(image)

    return results


def print_pipeline_results(orig_path, new_path):
    """Prints the results of the pipelining process for a given image.

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


def get_image_out_path(image, orig_path, out_path, options):
    """Gets the output path for an image.

    Extracts an apporpriate name for the image file based on
    the provided options. This file name is then included in
    the output path for the image.

    Args:
        image: An instance of a PIL image.
        orig_path: The path to the original image.
        out_path: The path to the output directory.
        options: A dictionary of options from the command class instance.

    Returns:
        A string containing the complete output path for the image.
    """
    filename, extension = os.path.splitext(ntpath.split(orig_path)[1])
    added_text = ''

    # Assume that if resolutions existed, resizing occurred.
    if options['resolutions']:
        # Include resized resolution into file name for now.
        size = image.size
        added_text += '_' + str(size[0]) + '_' + str(size[1]) + '_'

    # TODO: Replace with a "--postfix" option or something from cmd args.
    added_text += 'cmprsd'

    out_file = os.path.join(out_path, filename + added_text + extension)

    return out_file


def save_image(image, out_file, quality):
    """Saves an instance of a PIL Image to the system.

    This is a wrapper for the PIL Image save function.

    Args:
        img: An instance of a PIL Image.
        out_file: Path to save the image to.
        quality: Quality to apply to the image.
    """
    image.save(out_file, optimize=True, quality=quality)
