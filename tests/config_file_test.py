'''Tests for the config_file module.'''
import unittest
from unittest.mock import patch
from unittest.mock import mock_open
import json
from aperture.config_file import config_or_provided
from aperture.config_file import OPTION_DEFAULTS
from aperture.config_file import validate_data
from aperture.config_file import read_config


class ConfigOrProvidedTest(unittest.TestCase):
    '''Tests for the config_or_provided function.'''

    def setUp(self):
        # Create a dict that matches that returned from a config file and docopt.
        self.opt_key = 'quality'
        self.cfg_opts = {
            self.opt_key: 1,
        }

        self.arg_key = '--' + self.opt_key
        self.arg_opts = {self.arg_key: None}

    def test_no_default(self):
        opt_value = self.cfg_opts[self.opt_key]
        test_opt_value = config_or_provided(self.opt_key, self.cfg_opts,
                                            self.arg_opts)

        self.assertEqual(
            test_opt_value, opt_value,
            'it uses the config file option instead of the default')

    def test_default(self):
        # Remove the option from config dict
        del self.cfg_opts[self.opt_key]
        # Option in arg dict is already none (see setUp), therefore we don't need to set it

        default_val = OPTION_DEFAULTS[self.opt_key]
        test_default_val = config_or_provided(self.opt_key, self.cfg_opts,
                                              self.arg_opts)

        self.assertEqual(
            test_default_val, default_val,
            'it uses default if the option is omitted in the config file and terminal arguments'
        )

    def test_override(self):
        override_val = 99
        self.arg_opts[self.arg_key] = override_val

        test_override_val = config_or_provided(self.opt_key, self.cfg_opts,
                                               self.arg_opts)

        self.assertEqual(
            test_override_val, override_val,
            'it uses options provided as arugments in the terminal over options provided in config file'
        )


class ValidateDataTest(unittest.TestCase):
    '''Tests for the validate_data function.'''

    def setUp(self):
        self.cfg_key = 'quality'  # key to use for dict manipulation
        self.cfg_opts = {
            self.cfg_key: 2,
            'verbose': True,
            'resolutions': 'some_resolution'
        }

    def test_no_data(self):
        test_data = validate_data({})
        self.assertDictEqual(test_data, {},
                             'it returns an empty dict if no options exist')

    def test_optionkey_invalid(self):
        num_opts = len(self.cfg_opts)
        bad_key = 'asdfqwer'
        good_key_val = self.cfg_opts[self.cfg_key]
        del self.cfg_opts[self.cfg_key]
        self.cfg_opts[bad_key] = good_key_val

        test_num_opts = len(validate_data(self.cfg_opts))
        self.assertEqual(test_num_opts, num_opts - 1,
                         'it removes an option if the key is incorrect')

    def test_datatype_invalid(self):
        num_opts = len(self.cfg_opts)
        bad_value = True
        self.cfg_opts[self.cfg_key] = bad_value

        test_num_opts = len(validate_data(self.cfg_opts))
        self.assertEqual(
            test_num_opts, num_opts - 1,
            'it removes an option if the data type for the key is incorrect')

    def test_all_valid(self):
        test_dict = validate_data(self.cfg_opts)
        self.assertDictEqual(
            test_dict, self.cfg_opts,
            'it returns the original dict if all options are valid')


class ReadConfigTest(unittest.TestCase):
    '''Tests for the read_config function.'''

    def setUp(self):
        self.cfg_opts = {'quality': 10, 'verbose': True}
        self.cfg_opts_json_valid = '{ "quality": 10, "verbose": true }'
        self.cfg_opts_json_invalid = 'asdf'

    @patch('os.path.isfile')
    def test_valid_config_file(self, mock_isfile):
        mock_isfile.return_value = True
        # Mock the built in 'open'; have it return a raw JSON string.
        with patch(
                'builtins.open',
                mock_open(read_data=self.cfg_opts_json_valid)) as m:
            test_cfg = read_config()
            mock_isfile.assert_called_with('.aperture')
            m.assert_called_with('.aperture', 'r')
            self.assertDictEqual(
                test_cfg, self.cfg_opts,
                'it returns a config dict when the config file exists and is valid'
            )

    @patch('os.path.isfile')
    def test_invalid_config_file(self, mock_isfile):
        mock_isfile.return_value = True
        # Mock built in 'open'; have it return a string with no JSON structure
        with patch(
                'builtins.open',
                mock_open(read_data=self.cfg_opts_json_invalid)):
            self.assertRaises(
                json.decoder.JSONDecodeError, read_config,
                'it raises an error if the config file contains invalid json')

    def test_not_found(self):
        self.assertIsNone(read_config(),
                          'it returns None if the config file does not exist')


if __name__ == '__main__':
    unittest.main()