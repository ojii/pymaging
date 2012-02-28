# -*- coding: utf-8 -*-
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
