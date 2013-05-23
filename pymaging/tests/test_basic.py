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
from pymaging.colors import Color, RGBA
from pymaging.exceptions import FormatNotSupported
from pymaging.image import Image
from pymaging.shapes import Line, Pixel
from pymaging.test_utils import PymagingBaseTestCase, image_factory
from pymaging.webcolors import Red, Green, Blue, Black, White, Lime
try: # pragma: no-cover
    # 2.x
    from StringIO import StringIO
except ImportError: # pragma: no-cover
    # 3.x
    from io import StringIO


class BasicTests(PymagingBaseTestCase):
    def _get_fake_image(self):
        return image_factory([
            [Red, Green, Blue],
            [Green, Blue, Red],
            [Blue, Red, Green],
        ])

    def test_open_invalid_image(self):
        self.assertRaises(FormatNotSupported, Image.open, StringIO(''))

    def test_crop(self):
        img = self._get_fake_image()
        img.crop(1, 1, 1, 1)

    def test_flip_left_right(self):
        img = self._get_fake_image()
        l2r = img.flip_left_right()
        self.assertImage(l2r, [
            [Blue, Green, Red],
            [Red, Blue, Green],
            [Green, Red, Blue],
        ])

    def test_flip_top_bottom(self):
        img = self._get_fake_image()
        t2b = img.flip_top_bottom()
        self.assertImage(t2b, [
            [Blue, Red, Green],
            [Green, Blue, Red],
            [Red, Green, Blue],
        ])

    def test_get_pixel(self):
        img = self._get_fake_image()
        color = img.get_color(0, 0)
        self.assertEqual(color, Red)

    def test_set_pixel(self):
        img = image_factory([
            [Black, Black],
            [Black, Black],
        ])
        img.set_color(0, 0, White)
        self.assertImage(img, [
            [White, Black],
            [Black, Black],
        ])

    def test_color_mix_with(self):
        base = Red
        color = Lime.get_for_brightness(0.5)
        result = base.cover_with(color)
        self.assertEqual(result, Color(128, 127, 0, 255))

    def test_color_mix_with_fastpath(self):
        base = Red
        color = Lime
        result = base.cover_with(color)
        self.assertEqual(result, Lime)

    def test_new(self):
        img = Image.new(5, 5, Black, RGBA)
        self.assertImage(img, [
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            ])



class DrawTests(PymagingBaseTestCase):
    def test_draw_pixel(self):
        img = image_factory([
            [Black, Black],
            [Black, Black],
        ])
        pixel = Pixel(0, 0)
        img.draw(pixel, White)
        self.assertImage(img, [
            [White, Black],
            [Black, Black],
        ])

    def test_alpha_mixing(self):
        img = image_factory([[Red]])
        semi_transparent_green = Lime.get_for_brightness(0.5)
        img.draw(Pixel(0, 0), semi_transparent_green)
        result = img.get_color(0, 0)
        self.assertEqual(result, Color(128, 127, 0, 255))

    def test_draw_line_topleft_bottomright(self):
        img = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        line = Line(0, 0, 4, 4)
        img.draw(line, White)
        self.assertImage(img, [
            [White, Black, Black, Black, Black],
            [Black, White, Black, Black, Black],
            [Black, Black, White, Black, Black],
            [Black, Black, Black, White, Black],
            [Black, Black, Black, Black, White],
        ])

    def test_draw_line_bottomright_topleft(self):
        img = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        line = Line(4, 4, 0, 0)
        img.draw(line, White)
        self.assertImage(img, [
            [White, Black, Black, Black, Black],
            [Black, White, Black, Black, Black],
            [Black, Black, White, Black, Black],
            [Black, Black, Black, White, Black],
            [Black, Black, Black, Black, White],
        ])

    def test_draw_line_bottomleft_topright(self):
        img = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        line = Line(0, 4, 4, 0)
        img.draw(line, White)
        self.assertImage(img, [
            [Black, Black, Black, Black, White],
            [Black, Black, Black, White, Black],
            [Black, Black, White, Black, Black],
            [Black, White, Black, Black, Black],
            [White, Black, Black, Black, Black],
        ])

    def test_draw_line_topright_bottomleft(self):
        img = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        line = Line(4, 0, 0, 4)
        img.draw(line, White)
        self.assertImage(img, [
            [Black, Black, Black, Black, White],
            [Black, Black, Black, White, Black],
            [Black, Black, White, Black, Black],
            [Black, White, Black, Black, Black],
            [White, Black, Black, Black, Black],
        ])

    def test_draw_line_steep(self):
        img = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        line = Line(0, 0, 1, 4)
        img.draw(line, White)
        self.assertImage(img, [
            [White, Black, Black, Black, Black],
            [White, Black, Black, Black, Black],
            [Black, White, Black, Black, Black],
            [Black, White, Black, Black, Black],
            [Black, White, Black, Black, Black],
        ])

    def test_blit_simple(self):
        main = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        other =image_factory([
            [White, White, White],
            [White, White, White],
            [White, White, White],
        ])
        main.blit(1, 1, other)
        self.assertImage(main, [
            [Black, Black, Black, Black, Black],
            [Black, White, White, White, Black],
            [Black, White, White, White, Black],
            [Black, White, White, White, Black],
            [Black, Black, Black, Black, Black],
        ])

    def test_blit_partial(self):
        main = image_factory([
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
        ])
        other =image_factory([
            [White, White, White],
            [White, White, White],
            [White, White, White],
        ])
        main.blit(3, 3, other)
        self.assertImage(main, [
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, Black, Black],
            [Black, Black, Black, White, White],
            [Black, Black, Black, White, White],
        ])
