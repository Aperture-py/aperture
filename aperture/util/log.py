import os

COLORS = {
    'INFO': '\033[95m',
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

    if not 'nt' == os.name:
        output += COLORS[level]

    print(output + message)


def draw_table(elems):
    pass
