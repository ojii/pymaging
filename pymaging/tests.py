# Copyright (c) 2012, Jonas Obrist
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Jonas Obrist nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JONAS OBRIST BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from __future__ import absolute_import
from pymaging.colors import Color, ColorType
from pymaging.image import Image
from pymaging.shapes import Line, Pixel, AntiAliasedLine
import array
import itertools
import unittest


RED = Color(255, 0, 0, 255)
GREEN = Color(0, 255, 0, 255)
BLUE = Color(0, 0, 255, 255)
BLACK = Color(0, 0, 0, 255)
WHITE = Color(255, 255, 255, 255)

def image_factory(colors, alpha=True):
    height = len(colors)
    width = len(colors[0]) if height else 0
    pixelsize = 4 if alpha else 3
    pixels = [array.array('B', itertools.chain(*[color.to_pixel(pixelsize) for color in row])) for row in colors]
    return Image(width, height, pixels, ColorType(pixelsize))


class PymagingBaseTestCase(unittest.TestCase):
    def assertImage(self, img, colors, alpha=True):
        check = image_factory(colors, alpha)
        self.maxDiff = None
        self.assertEqual(img.pixels, check.pixels)


class BasicTests(PymagingBaseTestCase):
    def _get_fake_image(self):
        return image_factory([
            [RED, GREEN, BLUE],
            [GREEN, BLUE, RED],
            [BLUE, RED, GREEN],
        ])

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
        self.assertEqual(color, RED)
        
    def test_set_pixel(self):
        img = image_factory([
            [BLACK, BLACK],
            [BLACK, BLACK],
        ])
        img.set_color(0, 0, WHITE)
        self.assertImage(img, [
            [WHITE, BLACK],
            [BLACK, BLACK],
        ])


class ResizeCropTests(PymagingBaseTestCase):
    def test_resize(self):
        img = image_factory([
            [RED, GREEN, BLUE],
            [GREEN, BLUE, RED],
            [BLUE, RED, GREEN],
        ])
        img = img.resize(2, 2)
        self.assertImage(img, [
            [RED, BLUE],
            [BLUE, GREEN],
        ])


class DrawTests(PymagingBaseTestCase):
    def test_draw_pixel(self):
        img = image_factory([
            [BLACK, BLACK],
            [BLACK, BLACK],
        ])
        pixel = Pixel(0, 0)
        img.draw(pixel, WHITE)
        self.assertImage(img, [
            [WHITE, BLACK],
            [BLACK, BLACK],
        ])
        
    def test_draw_line_topleft_bottomright(self):
        img = image_factory([
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
        ])
        line = Line(0, 0, 4, 4)
        img.draw(line, WHITE)
        self.assertImage(img, [
            [WHITE, BLACK, BLACK, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
            [BLACK, BLACK, WHITE, BLACK, BLACK],
            [BLACK, BLACK, BLACK, WHITE, BLACK],
            [BLACK, BLACK, BLACK, BLACK, WHITE],
        ])
        
    def test_draw_line_bottomright_topleft(self):
        img = image_factory([
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
        ])
        line = Line(4, 4, 0, 0)
        img.draw(line, WHITE)
        self.assertImage(img, [
            [WHITE, BLACK, BLACK, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
            [BLACK, BLACK, WHITE, BLACK, BLACK],
            [BLACK, BLACK, BLACK, WHITE, BLACK],
            [BLACK, BLACK, BLACK, BLACK, WHITE],
        ])
        
    def test_draw_line_bottomleft_topright(self):
        img = image_factory([
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
        ])
        line = Line(0, 4, 4, 0)
        img.draw(line, WHITE)
        self.assertImage(img, [
            [BLACK, BLACK, BLACK, BLACK, WHITE],
            [BLACK, BLACK, BLACK, WHITE, BLACK],
            [BLACK, BLACK, WHITE, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
            [WHITE, BLACK, BLACK, BLACK, BLACK],
        ])
        
    def test_draw_line_topright_bottomleft(self):
        img = image_factory([
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
        ])
        line = Line(4, 0, 0, 4)
        img.draw(line, WHITE)
        self.assertImage(img, [
            [BLACK, BLACK, BLACK, BLACK, WHITE],
            [BLACK, BLACK, BLACK, WHITE, BLACK],
            [BLACK, BLACK, WHITE, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
            [WHITE, BLACK, BLACK, BLACK, BLACK],
        ])
        
    def test_draw_line_steep(self):
        img = image_factory([
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
        ])
        line = Line(0, 0, 1, 4)
        img.draw(line, WHITE)
        self.assertImage(img, [
            [WHITE, BLACK, BLACK, BLACK, BLACK],
            [WHITE, BLACK, BLACK, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
            [BLACK, WHITE, BLACK, BLACK, BLACK],
        ])
    
    def test_xiaolin_wu_line_drawing(self):
        img = image_factory([
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
            [BLACK, BLACK, BLACK, BLACK, BLACK],
        ])
        line = AntiAliasedLine(0, 0, 4, 4)
        img.draw(line, WHITE)
        print(img.pixels)
