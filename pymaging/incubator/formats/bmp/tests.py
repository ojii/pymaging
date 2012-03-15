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
RED = Color(255, 0, 0, 255)
GREEN = Color(0, 255, 0, 255)
BLUE = Color(0, 0, 255, 255)


class BMPTests(unittest.TestCase):
    def test_32bit_bmp_decoding(self):
        with open(_get_filepath('black-white-32bit.bmp'), 'rb') as fobj:
            decoder = BMPDecoder(fobj)
            img = decoder.get_image()
        self.assertEqual(img.width, 2)
        self.assertEqual(img.height, 2)
        self.assertEqual(img.palette, None)
        self.assertEqual(decoder.bits_per_pixel, 32)
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)
        
    def test_32bit_bmp_decoding_colorful(self):
        with open(_get_filepath('red-green-blue-black-32bit.bmp'), 'rb') as fobj:
            decoder = BMPDecoder(fobj)
            img = decoder.get_image()
        self.assertEqual(img.width, 2)
        self.assertEqual(img.height, 2)
        self.assertEqual(img.palette, None)
        self.assertEqual(decoder.bits_per_pixel, 32)
        self.assertEqual(img.get_color(0, 0), RED)
        self.assertEqual(img.get_color(1, 0), GREEN)
        self.assertEqual(img.get_color(0, 1), BLUE)
        self.assertEqual(img.get_color(1, 1), BLACK)
    
    def test_24bit_bmp_decoding(self):
        with open(_get_filepath('black-white-24bit.bmp'), 'rb') as fobj:
            decoder = BMPDecoder(fobj)
            img = decoder.get_image()
        self.assertEqual(img.width, 2)
        self.assertEqual(img.height, 2)
        self.assertEqual(img.palette, None)
        self.assertEqual(decoder.bits_per_pixel, 24)
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)
    
    def test_1bit_bmp_decoding(self):
        with open(_get_filepath('black-white.bmp'), 'rb') as fobj:
            decoder = BMPDecoder(fobj)
            img = decoder.get_image()
        self.assertEqual(img.width, 2)
        self.assertEqual(img.height, 2)
        self.assertNotEqual(img.palette, None)
        self.assertEqual(decoder.bits_per_pixel, 1)
        self.assertEqual(img.get_color(0, 0), BLACK)
        self.assertEqual(img.get_color(1, 1), BLACK)
        self.assertEqual(img.get_color(0, 1), WHITE)
        self.assertEqual(img.get_color(1, 0), WHITE)
