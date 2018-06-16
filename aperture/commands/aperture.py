import os
import ntpath
import aperturelib as apt
import aperture.util.files as utl_f
from .command import Command
import aperture.util.log as utl_l


class Aperture(Command):

    def run(self):
        '''Runs the 'aperture' command.'''

        options = self.options

        inputs = options['inputs']
        out_path = options['output']
        quality = options['quality']
        verbose = options['verbose']
        resolutions = options['resolutions']

        # Dictionary required for success output
        sizes_keys = resolutions.copy()
        sizes = {'orig': []}
        if sizes_keys == []:
            sizes_keys.append('new')
            sizes['new'] = []
        else:
            for size in sizes_keys:
                sizes[size] = []

        for image_path in inputs:
            results = apt.format_image(image_path, options)

            # Record the original size of the image once
            sizes['orig'].append(os.path.getsize(image_path))

            for index in range(len(results)):
                image = results[index]

                # Get the output file path
                out_file = get_image_out_path(image, image_path, out_path,
                                              options)

                # Save the image, apply quality LAST
                pil_opts = {'quality': quality}
                apt.save(image, out_file, **pil_opts)

                # For each resolution (if no resolution specified do once with key 'new')
                # record the resulting file size
                sizes[sizes_keys[index]].append(os.path.getsize(out_file))

                # Print the results of the pipeline
                if verbose:
                    print_verbose(image_path, out_file)

        # Sum the image sizes for each element within the sizes
        for s in sizes:
            sizes[s] = sum(sizes[s])

        # Determine the savings for each specified resolution
        # (or once if no resolutions provided)
        if resolutions == []:
            utl_l.log('Total savings: {}'.format(
                utl_f.bytes_to_readable(sizes['orig'] - sizes['new'])), 'succ')
        else:
            for i in range(1, len(sizes)):
                res = resolutions[i - 1]
                res_str = '{}x{}'.format(res[0], res[1])
                utl_l.log('Total savings for resolution {}: {}'.format(
                    res_str,
                    utl_f.bytes_to_readable(
                        sizes['orig'] - sizes[list(sizes)[i]])), 'succ')


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
    utl_l.log('\t{} ({}) -> {} ({}) [{} saved]'.format(
        orig_path, utl_f.bytes_to_readable(old_size), new_path,
        utl_f.bytes_to_readable(new_size),
        utl_f.bytes_to_readable(old_size - new_size)), 'info')


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
