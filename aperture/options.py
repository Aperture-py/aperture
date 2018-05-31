import aperture.util.files as utl_f
import aperture.util.directories as utl_d
import aperture.util.config as utl_c

DEFAULT_RESOLUTIONS = [(200, 200), (500, 500)]
DEFAULT_QUALITY = 75


def deserialize_options(options, config_dict):

    deserialized = {}

    inputs = options['<inputs>']

    out_dir = utl_c.config_or_provided('output', '-o', config_dict, options)
    quality = utl_c.config_or_provided('quality', '-c', config_dict, options)
    resolutions = utl_c.config_or_provided('resolutions', '-r', config_dict,
                                           options)
    verbose = utl_c.config_or_provided('verbose', '--verbose', config_dict,
                                       options)

    deserialized['inputs'] = utl_f.get_file_paths_from_inputs(inputs)
    deserialized['output'] = utl_d.get_output_path(out_dir)
    deserialized['quality'] = get_quality(quality)
    deserialized['resolutions'] = get_resolutions(resolutions)
    deserialized['verbose'] = verbose

    return deserialized


def get_quality(quality):
    try:
        quality = DEFAULT_QUALITY if quality is None else int(quality)
    except ValueError:
        print(
            'E: Supplied quality value \'{}\' is not valid. Quality must be an integer between 0 and 100. Using default value instead'.
            format(quality))
        quality = DEFAULT_QUALITY

    return quality


def get_resolutions(resolutions):
    """Extracts the resolutions to use for resizing each image.

    Args:
        resolution: A string containing image resolutions.
            The resolution string is expected to have an 'x' used to separate
            the dimensions of each resolution, with each resolution separated
            by a space.
            
            Example: 
            "1600x900 1280x1024"
    Returns:
        A list of tuples for each resolution, where each tuple is (width, height).

        Example:

        [(1600, 900), (1280, 1024)]
    """
    if resolutions is None or not resolutions:
        resolutions = DEFAULT_RESOLUTIONS
    else:
        temp = []
        resolutions = resolutions.split(' ')
        for res in resolutions:
            try:
                w, h = res.lower().split('x')
                r = (int(w), int(h))
                temp.append(r)
            except ValueError:
                print(
                    'E: Supplied resolution \'{}\' is not valid. Resolutions must be in form \'-r <width>x<height>\''.
                    format(res))
        resolutions = temp
        if not resolutions:
            print(
                'E: All supplied resolution were invalid. Images will not be resized'
            )
    return resolutions