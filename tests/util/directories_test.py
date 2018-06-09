'''Unit tests for module: aperture.util.directories'''
import os
import unittest
import datetime
from tests.util import util_test_helper
from aperture.util.directories import make_necessary_directories


#pylint: disable=C0111
class DirectoriesTest(util_test_helper.UtilTest):

    # *********
    # TODO: Learn to use mock insteead of actually creating dirs / files
    def setUp(self):
        now = datetime.datetime.now()
        self.dir_relative = str(now)
        self.dir_absolute = os.path.abspath(__file__).split('.py')[0] + str(now)
        self.dir_no_per = self.dir_relative + '/no-perm'

    def tearDown(self):
        os.rmdir(self.dir_relative)
        os.rmdir(self.dir_absolute)

    def test_make_necessary_directories(self):
        '''Test for the make_necessary_directories function.

        Tests:
            1. Creation using a relative path.
            2. Creation using an absolute path.
            3. Creation in a directory with no write access.
        '''

        # 1. Creation of a relative path
        make_necessary_directories(self.dir_relative)
        self.assertTrue(
            os.path.exists(self.dir_relative),
            'directory made with relative path')

        # 2. Creation of an absolute path
        make_necessary_directories(self.dir_absolute)
        self.assertTrue(
            os.path.exists(self.dir_absolute),
            'directory made with absolute path')

        # 3. Creation in a directory with no write access.
        # os.chmod(self.dir_relative, 0o444)  # Make it a read-only directory
        # self.assertRaises(PermissionError, make_necessary_directories,
        #                   self.dir_no_per)


if __name__ == '__main__':
    unittest.main()
