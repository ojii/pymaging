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
from pymaging.incubator.formats.gif.decoder import GIFDecoder
from pymaging.webcolors import Black, Red, Blue, Lime
import os
import pymaging
import unittest


TESTDATA = os.path.join(os.path.dirname(pymaging.__file__), '..', 'testdata')

def _get_filepath(fname):
    return os.path.join(TESTDATA, fname)


class BMPTests(unittest.TestCase):
    def test_gif_red_green_blue_black(self):
        with open(_get_filepath('red-green-blue-black.gif'), 'rb') as fobj:
            decoder = GIFDecoder(fobj)
            img = decoder.get_image()
        self.assertEqual(img.width, 2)
        self.assertEqual(img.height, 2)
        self.assertEqual(img.get_color(0, 0), Red)
        self.assertEqual(img.get_color(1, 0), Lime)
        self.assertEqual(img.get_color(0, 1), Blue)
        self.assertEqual(img.get_color(1, 1), Black)
