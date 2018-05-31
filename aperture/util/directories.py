import os, platform, re

DEFAULT_DIR = os.getcwd()


def get_output_path(out_path):
    #If no output directory is provided, or supplied dir is invalid, use cwd
    if out_path is None:
        out_path = DEFAULT_DIR
    elif not os.path.isdir(out_path):
        # Attempt to create the output directory
        # NOTE: haven't tested with directories where user does not have write permissions
        # (definitely won't work, just dont know what error to catch)
        make_necessary_directories(out_path)

    return out_path


##############################################################
# Recursively make any necessary directories and
# subdirectories for output if it does not exist. Current
# working directory will not be affected
##############################################################
def make_necessary_directories(path):
    #Get the absolute version of whatever path was specified.
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