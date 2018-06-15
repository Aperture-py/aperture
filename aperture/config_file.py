import os, json

OPTION_TYPES = {
    'outpath': 'str',
    'quality': 'int',
    'resolutions': 'str',
    'verbose': 'bool',
    'max-depth': 'int',
    'wmark-img': 'str',
    'wmark-txt': 'str'
}

OPTION_DEFAULTS = {'quality': 75, 'max-depth': 0}


# BUG: Any defaults specified in docopt will always override a value in the config file
# even if not provided in the cmd line
def config_or_provided(option_key, config_dict, options_dict):
    ''' Determine whether an option was provided by the user in the terminal, and if not use the option specified 
        in the config file if it exists. '''

    flag = '--' + option_key

    # wasn't provided in terminal, so we have to check conf file
    if ((OPTION_TYPES[option_key] == 'bool' and options_dict[flag] is False) or
            options_dict[flag] is None):
        if config_dict is not None and option_key in config_dict:
            return config_dict[option_key]  # use config file value
        elif option_key in OPTION_DEFAULTS:  # wasnt in config file, use default
            return OPTION_DEFAULTS[option_key]

    return options_dict[flag]  # was provided in terminal, use that


def read_config():
    ''' Search for the aperture config file within the current working directory. 
        If it exists, read the json and return the dictionary of validated values. '''
    if os.path.isfile('.aperture'):
        with open('.aperture', 'r') as f:
            data = json.load(f)
        validated = validate_data(data)
        return validated
    else:
        return None


# BUG: If you set quality to True in the dict, it doesn't get removed
# from the dict even though its not an int
def validate_data(data):
    ''' Determine whether the config file contains valid syntax, datatypes, ect. '''
    to_remove = []
    for part in data:
        if not (part in OPTION_TYPES and
                isinstance(data[part], eval(OPTION_TYPES[part]))):
            to_remove.append(part)

    for part in to_remove:
        data.pop(part)

    return data