import os, sys

COLORS = {
    'INFO': '\033[0m',
    'SUCC': '\033[92m',
    'WARN': '\033[93m',
    'ERROR': '\033[91m'
}


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
    sys.stdout.write(COLORS['INFO'])


def draw_table(elems):
    pass
