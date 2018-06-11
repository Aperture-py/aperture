'''Unit tests for module: aperture.util.files'''
import os
from unittest.mock import patch
from unittest.mock import MagicMock
import shutil
import unittest
import datetime
from tests.util.util_test_helper import UtilTest, fakeFileEntry
from aperture.util.files import get_files_in_directory_recursive


#pylint: disable=C0111
class FilesTest(UtilTest):

    # ********
    # TODO: Learn to use mock instead of actually creating dirs / files
    # def setUp(self):
    #     now = datetime.datetime.now()
    #     self.file_dir = str(now)
    #     file_dir_nested = self.file_dir + '/sub-dir'

    #     # Make dir with nested dir
    #     os.makedirs(file_dir_nested)

    #     self.num_files_root = 2
    #     self.num_files_nested = 3

    #     # Create empty files in top level dir
    #     for i in range(0, self.num_files_root):
    #         with open(os.path.join(self.file_dir, 'file-' + str(i)), 'w'):
    #             pass

    #     # Create empty files in nested dir
    #     for j in range(0, self.num_files_nested):
    #         with open(
    #                 os.path.join(file_dir_nested, 'file-nested-' + str(j)),
    #                 'w'):
    #             pass

    # def tearDown(self):
    #     shutil.rmtree(self.file_dir)  # Remove all nested dirs and files

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

        f1 = fakeFileEntry('file-1')
        f2 = fakeFileEntry('file-2')
        f3 = fakeFileEntry('file-3')
        f4 = fakeFileEntry('file-4')
        f5 = fakeFileEntry('file-5')

        t_1_files = [f1, f2, f3]
        mock_scandir.side_effect = [t_1_files]

        files = get_files_in_directory_recursive(self.file_dir, 0)
        print('files: ', files)
        mock_scandir.assert_called_with(self.file_dir)
        self.assertEqual(
            len(files), len(t_1_files),
            'finds all the files in dir when depth is 0')

        d1 = fakeFileEntry('dir-1', True)
        d2 = fakeFileEntry('dir-2', True)

        t_2_files_lvl_1 = [f1, f2, d1]
        t_2_files_lvl_2 = [f3, f4, d2]
        t_2_files_lvl_3 = [f5]

        t_2_total_files = 4

        mock_scandir.side_effect = [
            t_2_files_lvl_1, t_2_files_lvl_2, t_2_files_lvl_3
        ]

        files = get_files_in_directory_recursive(None, 2)
        self.assertEqual(
            len(files), 4, 'finds all files in root and 2 nested dirs')

        # make temp dir
        # make temp files
        # test 1

        # files = get_files_in_directory_recursive(self.file_dir, 0)

        # self.assertEqual(
        #     len(files), self.num_files_root,
        #     'gets only files in root dir when depth is 0')

        # files = get_files_in_directory_recursive(self.file_dir, 1)

        # total_files = self.num_files_root + self.num_files_nested

        # self.assertEqual(
        #     len(files), total_files,
        #     'gets files in root and sub directory when depth is 1')

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