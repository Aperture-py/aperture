'''Tests for the options module. '''
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch
from aperture.options import is_compatible_file
from aperture.options import parse_resolutions
from aperture.options import parse_quality
from aperture.options import parse_recursion_depth
from aperture.options import parse_inputs
from aperture.options import parse_outpath
from aperture.options import parse_watermark_image
from aperture.options import deserialize_options
from aperture.errors import ApertureError
from aperture.util.files import get_files_in_directory_recursive  # Patched by mock in ParseInputsTest
from aperture.util.directories import make_necessary_directories  # Patched by mock in ParseOutpathTest


def _touch_files(files):
    for name in files:
        open(name, 'a').close()


class DeserializeOptionsTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.file = os.path.join(self.test_dir, 'file.jpg')
        _touch_files([self.file])
        self.arg_opts = {
            '<input>': [self.file],
            '--quality': 25,
            '--resolutions': '800x800 400x400',
            '--verbose': False,
            '--max-depth': 2,
            '--outpath': self.test_dir,
            '--wmark-img': None,
            '--wmark-txt': 'text'
        }
        self.cfg_opts = {
            'quality': 90,
            'resolutions': '700x700',
            'verbose': True,
            'max-depth': 5,
            'outpath': self.test_dir,
            'wmark-img': None,
            'wmark-txt': 'some-other-text'
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_cmd_arg_opts(self):
        ds_opts = {
            'inputs': [self.file],
            'quality': 25,
            'resolutions': [(800, 800), (400, 400)],
            'verbose': False,
            'max-depth': 2,
            'output': self.test_dir,
            'wmark-img': None,
            'wmark-txt': 'text'
        }
        test_ds_opts = deserialize_options(self.arg_opts, None)
        self.assertDictEqual(
            test_ds_opts, ds_opts,
            'it returns a deserialized version of the cmd arg options')

    def test_cfg_file_opts(self):
        self.arg_opts['--quality'] = None
        self.arg_opts['--resolutions'] = None
        self.arg_opts['--verbose'] = None
        self.arg_opts['--max-depth'] = None
        self.arg_opts['--outpath'] = None
        self.arg_opts['--wmark-img'] = None
        self.arg_opts['--wmark-txt'] = None
        ds_opts = {
            'inputs': [self.file],
            'quality': 90,
            'resolutions': [(700, 700)],
            'verbose': True,
            'max-depth': 5,
            'output': self.test_dir,
            'wmark-img': None,
            'wmark-txt': 'some-other-text'
        }
        test_ds_opts = deserialize_options(self.arg_opts, self.cfg_opts)
        self.assertDictEqual(
            test_ds_opts, ds_opts,
            'it returns a deserialized version of the cfg file options')
        return None

    def test_both_opt_types(self):
        self.arg_opts['--verbose'] = None
        self.arg_opts['--outpath'] = None
        self.arg_opts['--wmark-img'] = None
        self.arg_opts['--wmark-txt'] = None

        test_ds_opts = deserialize_options(self.arg_opts, self.cfg_opts)

        did_cmd_args_overide_cfg = test_ds_opts['quality'] == self.arg_opts['--quality'] and test_ds_opts['max-depth'] == self.arg_opts['--max-depth']
        self.assertTrue(did_cmd_args_overide_cfg,
                        'it overwrote the cfg options with cmd arg options')


class ParseOutpathTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_no_outpath(self):
        test_outpath = parse_outpath(None)
        self.assertEqual(test_outpath, os.getcwd(),
                         'it returns the CWD if not outpath is provided')

    def test_dot_outpath(self):
        test_outpath = parse_outpath('.')
        self.assertEqual(test_outpath, os.getcwd(),
                         'it returns the CWD if the provided outpath is \'.\'')

    @patch('aperture.util.directories.make_necessary_directories')
    def test_no_permission(self, mock_mnd):
        # it raises an ApertureError if the output path does not have write access
        outpath = self.test_dir + 'hello'
        mock_mnd.side_effect = PermissionError()
        self.assertRaises(ApertureError, parse_outpath, outpath)

    @patch('aperture.util.directories.make_necessary_directories')
    def test_dir_creation_failure(self, mock_mnd):
        # it raises an ApertureError if the directory creation fails
        outpath = self.test_dir + 'hello'
        mock_mnd.side_effect = OSError()
        self.assertRaises(ApertureError, parse_outpath, outpath)

    def test_dir_creation(self):
        outpath = self.test_dir + 'hello'
        test_outpath = parse_outpath(outpath)
        was_created = os.path.exists(test_outpath)

        self.assertEqual(test_outpath, outpath,
                         'it returns the outpath when no errors occured')
        self.assertTrue(was_created, 'it created the outpath in the system')


class ParseRecursionDepthTest(unittest.TestCase):

    def test_not_int(self):
        # it raises an ApertureError if the recursion depth cannot be parsed into an int
        self.assertRaises(ApertureError, parse_recursion_depth, 'hello')

    def test_not_in_range(self):
        # it raises an ApertureError if the recursion depth is < 0
        depth = -1
        self.assertRaises(ApertureError, parse_recursion_depth, depth)

    def test_in_range(self):
        depth = 1
        test_depth = parse_recursion_depth(depth)
        self.assertEqual(test_depth, depth,
                         'it returns the depth if within the accepted range')


class ParseInputsTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _make_test_dir(self, name):
        fullpath = os.path.normpath(os.path.join(self.test_dir, name))
        os.makedirs(fullpath)
        return fullpath

    def test_no_files(self):
        # it raises an ApertureError if no input files were found
        self.assertRaises(ApertureError, parse_inputs, [self.test_dir], 0)

    def test_ignore_file_not_image(self):
        files = [
            os.path.join(self.test_dir, 'file1.jpg'),
            os.path.join(self.test_dir, 'file2')
        ]
        _touch_files(files)

        test_files = parse_inputs(files, 0)
        num_test_files = len(test_files)
        self.assertEqual(num_test_files, 1,
                         'it ignores files that are not images')

    @patch('aperture.util.files.get_files_in_directory_recursive')
    def test_no_permission(self, mock_gfr):
        # it raises an ApertureError if there is no read access for an input
        mock_gfr.side_effect = PermissionError()
        self.assertRaises(ApertureError, parse_inputs, self.test_dir, 0)

    def test_find_files(self):
        test_dir_1 = self._make_test_dir('test1')
        test_dir_2 = self._make_test_dir('test1/test2')
        files = [
            os.path.join(self.test_dir, 'file1.jpg'),
            os.path.join(test_dir_1, 'file2.jpg'),
            os.path.join(test_dir_2, 'file3.jpg'),
        ]
        _touch_files(files)

        test_files = parse_inputs([self.test_dir], 2)
        num_files = len(files)
        num_test_files = len(test_files)

        self.assertEqual(num_test_files, num_files,
                         'it finds all image files in the provided directory')


class ParseQualityTest(unittest.TestCase):

    def test_in_range(self):
        quality = 50
        test_quality = parse_quality(quality)

        self.assertEqual(test_quality, quality,
                         'it returns the quality if within the accepted range')

    def test_not_in_range(self):
        # it raises an ApertureError if the quality value is out of range
        self.assertRaises(ApertureError, parse_quality, -1)
        self.assertRaises(ApertureError, parse_quality, 101)

    def test_not_int(self):
        # it raises an Aperture Error if the quality value cannot be parsed into an int
        self.assertRaises(ApertureError, parse_quality, 'hello')


class ParseResolutions(unittest.TestCase):

    def test_no_resolutions(self):
        test_resolutions = parse_resolutions(None)
        self.assertListEqual(
            test_resolutions, [],
            'it returns an empty list if no resolutions are provided')

    def test_invalid_resolutions_string(self):
        # it raises an ApertureError if the resolution string cannot be parsed
        self.assertRaises(ApertureError, parse_resolutions, '')
        self.assertRaises(ApertureError, parse_resolutions, '800800 400400')
        self.assertRaises(ApertureError, parse_resolutions, '800x800400x400')

    def test_valid_resolutions(self):
        res_str = '800x800 400x400 200x200'
        test_res_lst = parse_resolutions(res_str)

        res_lst = [(800, 800), (400, 400), (200, 200)]

        self.assertListEqual(
            test_res_lst, res_lst,
            'it returns a list containing tuples for each resolution')


class ParseWatermarkImage(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_no_watermark_path(self):
        self.assertIsNone(
            parse_watermark_image(None),
            'it returns none if no watermark image is provided')

    def test_no_watermark_found(self):
        # it raises an ApertureError if the watermark path does not exist
        wmark_path = self.test_dir + 'wimg.jpg'
        self.assertRaises(ApertureError, parse_watermark_image, wmark_path)

    def test_not_compatible(self):
        # it raises an ApertureError if the watermark file is not an image
        wmark_path = os.path.join(self.test_dir, 'wimg.txt')
        _touch_files([wmark_path])

        self.assertRaises(ApertureError, parse_watermark_image, wmark_path)

    def test_find_watermark(self):
        wmark_path = os.path.join(self.test_dir, 'wimg.jpg')
        _touch_files([wmark_path])

        test_wmark_path = parse_watermark_image(wmark_path)
        self.assertEqual(test_wmark_path, wmark_path,
                         'it returns the watermark path if the file is found')


class IsCompatibleFileTest(unittest.TestCase):

    def setUp(self):
        self.compat_exts = ['.jpg']

    def test_compatible(self):
        name = 'file.jpg'
        test_is_compat = is_compatible_file(name, self.compat_exts)
        self.assertTrue(test_is_compat,
                        'it returns True if the file is compatible')

    def test_not_compatible(self):
        name = 'file.txt'
        test_is_compat = is_compatible_file(name, self.compat_exts)
        self.assertFalse(test_is_compat,
                         'it returns False if the file is not compatible')


if __name__ == '__main__':
    unittest.main()