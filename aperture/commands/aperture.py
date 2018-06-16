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

        # Dictionary required for success output
        res_keys = options['resolutions'].copy()
        files = {'orig': []}
        if res_keys == []:
            res_keys.append('new')
            files['new'] = []
        else:
            for res in res_keys:
                files[res] = []

        # lambda function to return filename and size as a tuple
        # where f is a file name
        filename_size = lambda f: (f, os.path.getsize(f))

        for image_path in inputs:
            results = apt.format_image(image_path, options)

            # Record the original size of the image once
            files['orig'].append(filename_size(image_path))

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
                files[res_keys[index]].append(filename_size(out_file))

                # Print the results of the pipeline
                if verbose:
                    utl_l.log('File \'{}\' created.'.format(out_file), 'info')

        # Print savings table if verbose
        if verbose:
            display_verbose_table(files)

        # Sum the image sizes for each element within the sizes
        sizes = {}
        for key in files:
            sizes[key] = sum(list(map(lambda x: x[1], files[key])))

        # Determine the savings for each specified resolution
        # (or once if no resolutions provided)
        if res_keys == ['new']:
            utl_l.log(
                'Total savings: {}'.format(
                    utl_f.bytes_to_readable(sizes['orig'] - sizes['new'])),
                'succ')
        else:
            for i in range(1, len(sizes)):
                res = res_keys[i - 1]
                res_str = '{}x{}'.format(res[0], res[1])
                utl_l.log(
                    'Total savings for resolution {}: {}'.format(
                        res_str,
                        utl_f.bytes_to_readable(sizes['orig'] -
                                                sizes[list(sizes)[i]])), 'succ')


def display_verbose_table(files):
    '''Displays the verbose output table for all processed image.
    
    Displays the file size comparison of the original an new image.

    Args:
        files: A dictionary containing tuples of filenames and filesizes for various resolutions.
    '''
    widths = (40, 40, 18)
    print('\n\t{} | {} | {}'.format('original'.ljust(widths[0]), 'result'.ljust(
        widths[1]), 'savings'.ljust(widths[2])))
    print('\t{}'.format('-' * (sum(widths) + 6)))

    image_count = len(files['orig'])
    format_file = lambda f: '{} [{}]'.format(f[0], utl_f.bytes_to_readable(f[1]))
    extra_line = len(files) > 2

    for image_index in range(image_count):
        orig_line = True
        orig = files['orig'][image_index]
        line = '\t{} | '.format(format_file(orig).ljust(widths[0]))

        for output_index in range(1, len(files)):
            current = files[list(files)[output_index]][image_index]

            if orig_line:
                line += '{} | {}'.format(
                    format_file(current).ljust(widths[1]),
                    utl_f.bytes_to_readable(orig[1] - current[1]).rjust(10))
                orig_line = False
            else:
                line = '\t{} | {} | {}'.format(
                    ' ' * widths[0],
                    format_file(current).ljust(widths[1]),
                    utl_f.bytes_to_readable(orig[1] - current[1]).rjust(10))

            print(line)

        if extra_line and not image_index == image_count - 1:
            print('\t{} | {} |'.format(' ' * widths[0], ' ' * widths[1]))

    print('\n')


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
