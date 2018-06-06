import os, platform, re


def make_necessary_directories(path):
    '''Makes necessary directories for a desired directory path.

    NOTE: Using this function for now instead of the old version,
    as the old function would always fail since it would attempt 
    to create a directory of name '' in root (atleast on MAC).

    Args:
        path: A string containing the desired directory path.
    '''
    os.makedirs(path)