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
from pymaging import Image
from pymaging.colors import Color
from pymaging.incubator.formats import register
from pymaging.utils import get_test_file
from pymaging.webcolors import Black, White
import unittest

ALMOST_BLACK = Color(8, 8,8 , 255)

class JPGTests(unittest.TestCase):
    def setUp(self):
        register()

    def test_decode(self):
        img = Image.open_from_path(get_test_file(__file__, 'black-white-100.jpg'))
        self.assertEqual(img.get_color(0, 0), Black)
        # TODO: Is this correct? Is this just JPEG being JPEG or is the decoder
        #       buggy? 1/1 SHOULD be BLACK but it's 8 8 8.
        self.assertEqual(img.get_color(1, 1), ALMOST_BLACK)
        self.assertEqual(img.get_color(0, 1), White)
        self.assertEqual(img.get_color(1, 0), White)
