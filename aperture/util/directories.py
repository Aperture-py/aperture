import os

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
# subdirectories for output if it does not exist. Return to
# the original directory afterward.
#
# (TODO):
# Need to make it so it doesnt just add all of the provided path
# to the end of the cwd. If a user supplies an absolute path whose
# base exists but has appended directories which dont exist, those
# extra directories should be added to the existing base path rather
# than just adding the whole thing to the cwd-path
#
##############################################################
def make_necessary_directories(path):
    original_dir = os.getcwd()

    # Split the path based off of the OS preferences. Allow windows
    # users to use forward slash if they would like
    directories = path.split(os.sep)
    if len(directories) == 1:
        directories = path.split('/')

    for dir in directories:
        if not os.path.isdir(dir):
            os.mkdir(dir)
        os.chdir(dir)

    os.chdir(original_dir)