import unittest


class UtilTest(unittest.TestCase):
    """An extension of the unittest TestCase base class to provide
    helper methods or text fixtures to be used in util tests.
    """


class fakeFileEntry():

    def __init__(self, path, is_a_dir=False):
        self.path = path
        self.is_a_dir = is_a_dir

    def is_dir(self, **kwargs):
        return self.is_a_dir
