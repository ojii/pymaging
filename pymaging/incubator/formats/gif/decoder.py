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
from pymaging.colors import RGB
from pymaging.image import Image
from pymaging.incubator.formats.gif.lzw import GifLZWDecompressor
from pymaging.utils import bitstruct
import struct



IMAGE_SEPARATOR = 0x2C
EXTENSION_INTRODUCER = 0x21
TRAILER = 0x3B



class GIFDecoder(object):
    def __init__(self, fileobj):
        self.fileobj = fileobj
        self.read_headers()
        
    def read_headers(self):
        signature, version = struct.unpack('<3s', self.fileobj.read(3))[0], struct.unpack('<3s', self.fileobj.read(3))[0]
        assert signature == b'GIF', signature
        assert version in [b'87a', b'89a'], version
        self.fileobj.read(4) # screen width/height
        packed, self.background, self.aspect_ratio = struct.unpack('<BBB', self.fileobj.read(3))
        # discarded values are color resolution and sort flag
        indexed, _, _, size_of_global_color_table = bitstruct((1, 3, 1, 3), packed)
        # 3 x 2^(Size of Global Color Table+1).
        if indexed:
            self.size_of_palette = 2 ** (size_of_global_color_table + 1)
            self.read_palette(self.size_of_palette)
        else:
            self.palette = [(x, x, x) for x in range(256)]
        # discarded values are left/top
        separator, _, _, self.width, self.height, packed = struct.unpack('<BHHHHB', self.fileobj.read(10))
        assert separator == IMAGE_SEPARATOR, separator
        # discarded values are sort flag and Reserved
        local_indexed, self.interlaced, _, _, size_of_local_color_table = bitstruct((1, 1, 1, 2, 3), packed)
        if local_indexed:
            self.size_of_palette = 2 ** (size_of_local_color_table + 1)
            self.read_palette(self.size_of_palette)
    
    def read_palette(self, size):
        self.palette = [struct.unpack('<BBB', self.fileobj.read(3)) for _ in range(size)]
        
    def get_image(self):
        print self.palette
        code_size = struct.unpack('<B', self.fileobj.read(1))[0]
        decompressor = GifLZWDecompressor(self.fileobj, code_size, self.width)
        pixels = decompressor.decompress()
        return Image(self.width, self.height, pixels, RGB, self.palette)
    