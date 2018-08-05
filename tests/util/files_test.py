'''Tests for util.files module.'''
import os
import tempfile
import shutil
import unittest
from unittest.mock import patch
from aperture.util.files import get_files_in_directory_recursive


def _touch_files(files):
    for name in files:
        open(name, 'a').close()


class GetFilesRecursivelyTest(unittest.TestCase):
    '''Tests for the get_files_recursively function.'''

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _make_test_dir(self, name):
        fullpath = os.path.normpath(os.path.join(self.test_dir, name))
        os.makedirs(fullpath)
        return fullpath

    def test_recursive_depth_0(self):
        test_files = [
            os.path.join(self.test_dir, 'file1'),
            os.path.join(self.test_dir, 'file2'),
            os.path.join(self.test_dir, 'file3')
        ]
        _touch_files(test_files)
        files = get_files_in_directory_recursive(self.test_dir, 0)

        num_test_files = len(test_files)
        num_files = len(files)
        self.assertEqual(num_test_files, num_files,
                         'it finds all the files in the root directory')

    def test_recursive_depth_gt_0(self):
        test_dir_1 = self._make_test_dir('test1')
        test_dir_2 = self._make_test_dir('test1/test2')
        test_dir_3 = self._make_test_dir('test1/test2/test3')

        # +test_dir          depth: 0
        #  |
        #  +test1            depth: 1
        #   | file1
        #   | file2
        #   + test2          depth: 2
        #     | file3
        #     | file4
        #     + test3        depth: 3
        #       | file5
        #       | file6

        files_d_1 = [
            os.path.join(test_dir_1, 'file1'),
            os.path.join(test_dir_1, 'file2')
        ]

        files_d_2 = [
            os.path.join(test_dir_2, 'file3'),
            os.path.join(test_dir_2, 'file4')
        ]

        files_d_3 = [
            os.path.join(test_dir_3, 'file5'),
            os.path.join(test_dir_3, 'file6')
        ]
        _touch_files(files_d_1)
        _touch_files(files_d_2)
        _touch_files(files_d_3)

        files = get_files_in_directory_recursive(self.test_dir, 2)

        num_test_files = len(files_d_1) + len(files_d_2)
        num_files = len(files)

        self.assertEqual(
            num_test_files, num_files,
            'it finds all files through recursive directory traversal up to a depth'
        )

    @patch('os.scandir')
    def test_no_permission(self, mock_scandir):
        # it raises a PermissionError if the directory does not have read access
        mock_scandir.side_effect = PermissionError()
        self.assertRaises(PermissionError, get_files_in_directory_recursive,
                          self.test_dir)


class BytesToReadableTest(unittest.TestCase):
    # TODO: Needs tests
    @unittest.skip('need to implement bytes_to_readable test')
    def test_something(self):
        return None


class GetFileSizeComparisonTest(unittest.TestCase):

    # TODO: Needs test
    @unittest.skip('need to implement get_file_size_comparison test')
    def test_something(self):
        return None


if __name__ == '__main__':
    unittest.main()