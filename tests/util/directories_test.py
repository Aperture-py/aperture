'''Tests for the util.directories module.'''
import unittest
from unittest.mock import patch
from aperture.util.directories import make_necessary_directories


class MakeNecessaryDirectories(unittest.TestCase):
    '''Tests for the make_necessary_directories function.'''

    def setUp(self):
        self.dir_name = 'testdir'

    @patch('os.makedirs')
    def test_make_directory(self, mock_makedirs):
        # it calls os.makedirs with the provided path
        make_necessary_directories(self.dir_name)
        mock_makedirs.assert_called_with(
            self.dir_name,
            exist_ok=True,
        )  # Ensure default we have for exist_ok was used too

    @patch('os.makedirs')
    def test_no_permission(self, mock_makedirs):
        'it raises a PermissionError if the there is no write access'
        mock_makedirs.side_effect = PermissionError()
        self.assertRaises(PermissionError, make_necessary_directories,
                          self.dir_name)


if __name__ == '__main__':
    unittest.main()
