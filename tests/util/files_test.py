'''Unit tests for module: aperture.util.files'''
from unittest.mock import patch
import unittest
from tests.util.util_test_helper import UtilTest, fakeFileEntry
from aperture.util.files import get_files_in_directory_recursive


#pylint: disable=C0111
class FilesTest(UtilTest):

    def setUp(self):
        self.file_dir = 'test-files'

    @patch('os.scandir')
    def test_get_files_recursively(self, mock_scandir):
        '''Test for the get_files_recursively function.

        Tests:
            1. Get files with depth of 0.
            2. Get files with depth > 0.
            3. Get files from directory with no read access.
        '''
        # Create fake file entries (mimics an instance of a os.DirEntry class returned from os.scandir)
        f1 = fakeFileEntry('file-1')
        f2 = fakeFileEntry('file-2')
        f3 = fakeFileEntry('file-3')
        f4 = fakeFileEntry('file-4')
        f5 = fakeFileEntry('file-5')

        total_files = 5

        # Test 1
        t_1_files = [f1, f2, f3]
        mock_scandir.side_effect = [t_1_files]  # Mock root dir

        files = get_files_in_directory_recursive(self.file_dir, 0)
        # Make sure os.scandir is called with correct path
        mock_scandir.assert_called_with(self.file_dir)
        self.assertEqual(
            len(files), len(t_1_files),
            'finds all the files in dir when depth is 0')

        # End Test 1

        # Create fake directories
        d1 = fakeFileEntry('dir-1', True)  # Mock dir at root
        d2 = fakeFileEntry('dir-2', True)  # Mock dir nested below root
        # Mock the a nested dir structure:
        #
        # file
        # file
        # dir
        #   | file
        #   | file
        #   | dir
        #     | file

        # Test 2
        t_2_files_lvl_1 = [f1, f2, d1]  # Depth = 0
        t_2_files_lvl_2 = [f3, f4, d2]  # Depth = 1
        t_2_files_lvl_3 = [f5]  # Depth = 2

        # Mock the return values for each depth
        mock_scandir.side_effect = [
            t_2_files_lvl_1, t_2_files_lvl_2, t_2_files_lvl_3
        ]

        files = get_files_in_directory_recursive(None, 2)
        self.assertEqual(
            len(files), total_files,
            'finds all files in root and 2 nested dirs')

        # Test 3
        mock_scandir.side_effect = PermissionError()
        self.assertRaises(PermissionError, get_files_in_directory_recursive,
                          self.file_dir)

    # TODO: Needs tests
    @unittest.skip('need to implement bytes_to_readable test')
    def test_bytes_to_readable(self):
        """Test for the bytes_to_readable function.
        """
        return None

    # TODO: Needs test
    @unittest.skip('need to implement get_file_size_comparison test')
    def test_get_file_size_comparison(self):
        """Test for the get_file_size_comparison function.
        """
        return None


if __name__ == '__main__':
    unittest.main()