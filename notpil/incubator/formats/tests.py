from notpil.colors import Color
from notpil.image import Image
import notpil
import os
import unittest

TESTDATA = os.path.join(os.path.dirname(notpil.__file__), '..', 'testdata')

def _get_filepath(fname):
    return os.path.join(TESTDATA, fname)

BLACK = Color(0, 0, 0, 255)
WHITE = Color(255, 255, 255, 255)

class PNGTests(unittest.TestCase):
    def test_indexed(self):
        img = Image.open_from_path(_get_filepath('black-white-indexed.png'))
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)
        
    def test_non_indexed(self):
        img = Image.open_from_path(_get_filepath('black-white-non-indexed.png'))
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)
        
    def test_non_indexed_interlaced(self):
        img = Image.open_from_path(_get_filepath('black-white-non-indexed-interlaced-adam7.png'))
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)

if __name__ == "__main__":
    unittest.main()
