import unittest
from tests.commands import commands_test_helper


class ApertureTest(commands_test_helper.CommandTest):

    @unittest.skip('need to implement run test')
    def test_run(self):
        """Test for the run function of the 'aperture' command.

        This test will also need alot of test fixtures to be created, such as:
            - a config file
            - images
            - directories with images
            - etc...
        """
        return None

    @unittest.skip('need to implement pipline_image test')
    def test_pipeline_image(self):
        """Test for the pipline_image function.
        """
        return None

    @unittest.skip('need to implement print_pipline_results test')
    def test_print_pipeline_results(self):
        """Test for the print_pipeline_results function.
        """
        return None

    @unittest.skip('need to implement get_image_out_path test')
    def test_get_image_out_path(self):
        """Test for the get_image_out_path function.
        """
        return None

    @unittest.skip('need to implement save_image test')
    def test_save_image(self):
        """Test for the save_image function
        """
        return None


if __name__ == '__main__':
    unittest.main()