import os, sys, logging
import aperture.util.files as utl_f
''' 
prev colors
    'INFO': '\033[0m',
    'SUCC': '\033[92m',
    'WARN': '\033[93m',
    'ERROR': '\033[91m',
'''

COLORS = {
    'INFO': '\u001b[0m',
    'SUCC': '\u001b[32m',
    'WARN': '\u001b[33m',
    'ERROR': '\u001b[31m',
    '.jpg': '\u001b[36;1m',
    '.gif': '\u001b[34;1m',
    '.png': '\u001b[35;1m'
}

widths = (40, 40, 10)


def log(message, level='INFO'):
    '''Print out a message to the console.

    Args:
        message: A string containing the message to be printed.
        level: A string containing the level of the message.

    '''

    level = level.upper()
    output = ''

    # If the os is windows ignore coloring
    if not 'nt' == os.name:
        output += COLORS[level]

    print(output + message)

    # Set the color to white after
    # NOTE: if there is some way to detect the default text
    # color this would be nice to apply here instead
    if not 'nt' == os.name:
        sys.stdout.write(COLORS['INFO'])


def display_verbose_table(files):
    '''Displays the verbose output table for all processed image.
    
    Displays the file size comparison of the original an new image.

    Args:
        files: A dictionary containing tuples of filenames and filesizes for various resolutions.
    '''

    print('\n\t{} | {} | {}'.format('original'.ljust(widths[0]), 'result'.ljust(
        widths[1]), 'savings'.ljust(widths[2])))
    print('\t{}'.format('-' * (sum(widths) + 6)))

    image_count = len(files['orig'])
    extra_line = len(files) > 2

    for image_index in range(image_count):
        orig_line = True
        orig = files['orig'][image_index]
        line = '\t{} | '.format(get_table_filename(orig).ljust(widths[0]))

        for output_index in range(1, len(files)):
            current = files[list(files)[output_index]][image_index]

            if orig_line:
                line += '{} | {}'.format(
                    get_table_filename(current).ljust(widths[1]),
                    utl_f.bytes_to_readable(orig[1] - current[1]).rjust(10))
                orig_line = False
            else:
                line = '\t{} | {} | {}'.format(
                    ' ' * widths[0],
                    get_table_filename(current).ljust(widths[1]),
                    utl_f.bytes_to_readable(orig[1] - current[1]).rjust(10))

            print(line)

        if extra_line and not image_index == image_count - 1:
            print('\t{} | {} |'.format(' ' * widths[0], ' ' * widths[1]))

    print('\n')


def get_table_filename(file_tuple, color_ext=False):
    filename = os.path.split(file_tuple[0])[1]
    filesize = '[{}]'.format(utl_f.bytes_to_readable(file_tuple[1]))

    # determine size of spaces between the two..

    filename_space = widths[0] - len(filesize)

    if len(filename) < filename_space:
        space_count = filename_space - len(filename)
        trunc_name = filename
    else:
        # Compress filename with an elipses
        space_count = 1
        # 17 + ext
        fn, ext = os.path.splitext(filename)
        len(fn)

        if color_ext == True and not os.name == 'nt':
            temp_ext = ext.lower()
            if temp_ext == '.jpeg':
                temp_ext = '.jpg'
            ext = '{}{}{}'.format(COLORS[temp_ext], ext, COLORS['INFO'])

        trunc_name = '{}...{}{}'.format(
            fn[:filename_space - len(ext) - len(fn) - 21], fn[len(fn) - 17:],
            ext)

    return '{}{}{}'.format(trunc_name, ' ' * space_count, filesize)
