import os, json

OPTION_TYPES = {
    'output': 'str',
    'quality': 'int',
    'resolutions': 'str',
    'verbose': 'bool'
}


def config_or_provided(option_key, flag, config_dict, options_dict):
    ''' Determine whether an option was provided by the user in the terminal, and if not use the option specified 
        in the config file if it exists. '''
    if config_dict is not None and option_key in config_dict and (
        (OPTION_TYPES[option_key] == 'bool' and options_dict[flag] is False) or
            options_dict[flag] is None):
        return config_dict[option_key]

    return options_dict[flag]


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


def validate_data(data):
    ''' Determine whether the config file contains valid syntax, datatypes, ect. '''
    for part in data:
        if not (part in OPTION_TYPES and
                isinstance(data[part], eval(OPTION_TYPES[part]))):
            data.pop(part)
    return data
