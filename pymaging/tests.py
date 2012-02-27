# -*- coding: utf-8 -*-
"""
Just tests that the APIs work without error, does no actual testing of output.
"""
from __future__ import absolute_import
from pymaging.colors import RGB, Color
from pymaging.image import Image
import array
import unittest


class IntegrityTests(unittest.TestCase):
    def _get_fake_image(self):
        pixels = [
            array.array('B', [255, 255, 255, 155, 155, 155, 55, 55, 55]),
            array.array('B', [233, 233, 233, 133, 133, 133, 33, 33, 33]),
            array.array('B', [211, 211, 211, 111, 111, 111, 11, 11, 11]),
        ]
        return Image(3, 3, pixels, RGB)

    def test_crop(self):
        img = self._get_fake_image()
        img.crop(1, 1, 1, 1)
        
    def test_flip_left_right(self):
        img = self._get_fake_image()
        img.flip_left_right()
        
    def test_flip_top_bottom(self):
        img = self._get_fake_image()
        img.flip_top_bottom()
    
    def test_get_pixel(self):
        img = self._get_fake_image()
        color = img.get_color(0, 0)
        self.assertEqual(color, Color(255, 255, 255, 255))
        
    def test_set_pixel(self):
        img = self._get_fake_image()
        test_color = Color(123, 123, 123, 255)
        img.set_color(0, 0, test_color)
        color = img.get_color(0, 0)
        self.assertEqual(color, test_color)
