'''Unit tests for module: aperture.util.directories'''
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from tests.util.util_test_helper import UtilTest
from aperture.util.directories import make_necessary_directories


#pylint: disable=C0111
class DirectoriesTest(UtilTest):

    def setUp(self):
        self.dir_name = 'test-dir'

    @patch('os.makedirs')
    def test_make_necessary_directories(self, mock_makedirs):
        '''Test for the make_necessary_directories function.

        Tests:
            1. os.makedirs is called using a provided path.
            2. A PermissionError bubbles up when raised by os.makedirs
        '''

        # Mock the return value of os.makedirs.
        # We're really just testing to see if the os.makedirs gets called by our function,
        # as the functionality of os.makedirs is left up to it's own testing.
        mock_makedirs.return_value = MagicMock(None)

        # Test 1
        make_necessary_directories(self.dir_name)
        mock_makedirs.assert_called_with(
            self.dir_name, exist_ok=True)  # Ensure default was used too

        # Test 2
        mock_makedirs.side_effect = PermissionError()
        self.assertRaises(PermissionError, make_necessary_directories,
                          self.dir_name)


if __name__ == '__main__':
    unittest.main()
