# -*- coding: utf-8 -*-
from pymaging.colors import Color
from pymaging.incubator.formats.bmp.codec import BMPDecoder
import os
import pymaging
import unittest


TESTDATA = os.path.join(os.path.dirname(pymaging.__file__), '..', 'testdata')

def _get_filepath(fname):
    return os.path.join(TESTDATA, fname)


BLACK = Color(0, 0, 0, 255)
WHITE = Color(255, 255, 255, 255)

class BMPTests(unittest.TestCase):
    def test_32bit_bmp_decoding(self):
        with open(_get_filepath('black-white-32bit.bmp'), 'rb') as fobj:
            decoder = BMPDecoder(fobj)
            img = decoder.get_image()
        self.assertEqual(img.width, 2)
        self.assertEqual(img.height, 2)
        self.assertEqual(img.palette, [])
        self.assertEqual(decoder.bits_per_pixel, 32)
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)
