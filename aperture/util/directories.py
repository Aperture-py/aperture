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


##############################################################
# Recursively make any necessary directories and
# subdirectories for output if it does not exist. Current
# working directory will not be affected
##############################################################
def _old_make_necessary_directories(path):

    # Get the absolute version of whatever path was specified.
    # -If an absolute path was specified, it will be unchanged
    # -If a relative path was specified, it will be appended to the cwd
    abspath = os.path.abspath(path)

    # Split the path based off of the OS preferences. Allow windows
    # users to use forward slash if they would like
    directories = abspath.split(os.sep)
    if len(directories) == 1:
        directories = abspath.split('/')

    #If on windows, and path begins with 'letter, colon, slash' drive format,
    # it needs to be addressed properly. Otherwise, it will be treated as 'letter
    # colon NO SLASH' which will be interpreted as cwd which will mess things
    # up. This is annoying and messy, but must be done
    driveformat = False
    if (platform.system().lower() == "windows"):
        if (re.match(r'[a-zA-Z]:[\\/]', abspath[0:3])):
            driveformat = True

    curpath = ""
    for dir in directories:
        if driveformat:
            dir += "\\"
            driveformat = False
        curpath = os.path.join(curpath, dir)
        if not os.path.isdir(curpath):
            os.mkdir(curpath)