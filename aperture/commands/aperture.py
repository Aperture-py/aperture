import os
import ntpath
import aperture.aperturelib as apt
import aperture.util.files as utl_f
from .command import Command


class Aperture(Command):

    def run(self):
        '''Runs the 'aperture' command.'''

        options = self.options

        inputs = options['inputs']
        out_path = options['output']
        quality = options['quality']
        verbose = options['verbose']

        for image_path in inputs:
            results = apt.format_image(image_path, options)

            for image in results:
                # Get the output file path
                out_file = get_image_out_path(image, image_path, out_path,
                                              options)

                # Save the image, apply quality LAST
                apt.save(image, out_file, quality)

                # Print the results of the pipeline
                if verbose:
                    print_verbose(image_path, out_file)


def print_verbose(orig_path, new_path):
    '''Prints the verbose output for a given image.
    
    Prints the file size comparison of the original an new image.

    Args:
        orig_path: The path to the original image.
        new_path: The path to the newly created image.
    '''
    size_comp = utl_f.get_file_size_comparison(orig_path, new_path)
    old_size = size_comp[0]
    new_size = size_comp[1]
    print('\t{} ({}) -> {} ({}) [{} saved]'.format(
        orig_path, utl_f.bytes_to_readable(old_size), new_path,
        utl_f.bytes_to_readable(new_size),
        utl_f.bytes_to_readable(old_size - new_size)))


def get_image_out_path(image, orig_path, out_path, options):
    '''Gets the output path for an image.

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
    '''
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
