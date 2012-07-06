# -*- coding: utf-8 -*-
import unittest
import array
from pymaging.colors import ColorType
from pymaging.image import Image
from pymaging.pixelarray import get_pixel_array


def image_factory(colors, alpha=True):
    height = len(colors)
    width = len(colors[0]) if height else 0
    pixel_size = 4 if alpha else 3
    pixel_array = get_pixel_array(array.array('B', [0] * width * height * pixel_size), width, height, pixel_size)
    for y in range(height):
        for x in range(width):
            pixel_array.set(x, y, colors[y][x].to_pixel(pixel_size))
    return Image(pixel_array, ColorType(pixel_size, alpha))


class PymagingBaseTestCase(unittest.TestCase):
    def assertImage(self, img, colors, alpha=True):
        check = image_factory(colors, alpha)
        self.assertEqual(img.pixels, check.pixels)
