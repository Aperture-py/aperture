'''Unit tests for module: aperture.util.files'''
import os
import shutil
import unittest
import datetime
from tests.util import util_test_helper
from aperture.util.files import get_files_in_directory_recursive


#pylint: disable=C0111
class FilesTest(util_test_helper.UtilTest):

    # ********
    # TODO: Learn to use mock instead of actually creating dirs / files
    def setUp(self):
        now = datetime.datetime.now()
        self.file_dir = str(now)
        file_dir_nested = self.file_dir + '/sub-dir'

        # Make dir with nested dir
        os.makedirs(file_dir_nested)

        self.num_files_root = 2
        self.num_files_nested = 3

        # Create empty files in top level dir
        for i in range(0, self.num_files_root):
            with open(os.path.join(self.file_dir, 'file-' + str(i)), 'w'):
                pass

        # Create empty files in nested dir
        for j in range(0, self.num_files_nested):
            with open(
                    os.path.join(file_dir_nested, 'file-nested-' + str(j)),
                    'w'):
                pass

    def tearDown(self):
        shutil.rmtree(self.file_dir)  # Remove all nested dirs and files

    def test_get_files_recursively(self):
        '''Test for the get_files_recursively function.

        Tests:
            1. Get files with depth of 0.
            2. Get files with depth > 0.
            3. Get files from directory with no read access.
        '''

        # make temp dir
        # make temp files

        # test 1

        files = get_files_in_directory_recursive(self.file_dir, 0)

        self.assertEqual(
            len(files), self.num_files_root,
            'gets only files in root dir when depth is 0')

        files = get_files_in_directory_recursive(self.file_dir, 1)

        total_files = self.num_files_root + self.num_files_nested

        self.assertEqual(
            len(files), total_files,
            'gets files in root and sub directory when depth is 1')

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