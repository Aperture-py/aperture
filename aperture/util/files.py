import os

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.gif', '.png')
DEFAULT_RECURSION_DEPTH = 0
MAX_RECURSTION_DEPTH = 10
DEFAULT_DIR = os.getcwd()


def get_file_paths_from_inputs(inputs):
    file_paths = []

    # TODO: Fix this to read from cmd-line
    recursionDepth = DEFAULT_RECURSION_DEPTH

    #If no input files or directories are provided, use cwd
    #   NOTE: Should we require some sort of explicit information '.' instead of assuming working directory?
    inputs = DEFAULT_DIR if inputs is None or not inputs else inputs

    ##################################
    # This is the meat of this command
    ##################################
    for path in inputs:
        extension = os.path.splitext(path)[1]

        if extension == '':
            try:
                #Gets all files (and only files) from supplied path and subdirectories recursively up to a given depth
                files = get_files_recursively(path, recursionDepth)

                for current_file in files:
                    extension = os.path.splitext(current_file)[1]
                    if extension.lower() in SUPPORTED_EXTENSIONS:
                        file_paths.append(current_file)
            except FileNotFoundError:
                print('E: could not locate directory \'{}\''.format(path))

        elif extension.lower() in SUPPORTED_EXTENSIONS:
            try:
                file_paths.append(path)
            except FileNotFoundError:
                print('E: unable to locate file \'{}\''.format(path))
        else:
            print('E: unsupported filetype \'{}\''.format(path))

    return file_paths


##############################################################
# Returns paths to all files from a provided path. Recursively
# traverses subdirectories up to a given depth, retrieving
# files from those directories as well.
##############################################################
def get_files_recursively(path, maxdepth):
    matches = []

    def do_scan(start_dir, output, depth=0):
        #Using scandir here instead of listdir. They do the same thing but
        # scandir has fewer stat() calls and so is much faster
        for entry in os.scandir(start_dir):
            if entry.is_dir(follow_symlinks=False):
                if depth < maxdepth:
                    do_scan(entry.path, output, depth + 1)
            else:
                output.append(entry.path)

    do_scan(path, matches, 0)
    return matches