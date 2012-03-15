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
import array
import struct


def BITMAPINFOHEADER(decoder):
    (decoder.width, decoder.height, nplanes, decoder.bits_per_pixel,
     decoder.compression_method, decoder.bmp_bytesz, decoder.hres, decoder.vres,
     decoder.ncolors, decoder.nimpcolors) = struct.unpack_from('<IihhiiIIii', decoder.fileobj.read(36))
    assert nplanes == 1, nplanes
    if decoder.bits_per_pixel == 32:
        decoder.read_row = decoder.read_row_32bit

def BITMAPV2INFOHEADER(decoder):
    BITMAPINFOHEADER(decoder)

def BITMAPV3INFOHEADER(decoder):
    BITMAPINFOHEADER(decoder)

def BITMAPV4HEADER(decoder):
    BITMAPINFOHEADER(decoder)
    
def BITMAPV5HEADER(decoder):
    BITMAPINFOHEADER(decoder)

HEADERS = {
    40: BITMAPINFOHEADER,
    52: BITMAPV2INFOHEADER,
    56: BITMAPV3INFOHEADER,
    108: BITMAPV4HEADER,
    124: BITMAPV5HEADER,
}

class BMPDecoder(object):
    def __init__(self, fileobj):
        self.fileobj = fileobj
        self.read_header()
    
    def read_header(self):
        magic = struct.unpack('<bb', self.fileobj.  read(2))
        assert magic == (66, 77), magic
        self.filelength = struct.unpack('<i', self.fileobj.read(4))[0]
        self.fileobj.read(4) # reserved/unused stuff
        self.offset = struct.unpack('<i', self.fileobj.read(4))[0]
        headersize = struct.unpack('<i', self.fileobj.read(4))[0]
        palette_start = self.fileobj.tell() + headersize
        HEADERS[headersize](self)
        self.row_size = ((self.bits_per_pixel * self.width) // 32) * 4
        # there might be header stuff that wasn't read, so skip ahead to the 
        # start of the color palette
        self.fileobj.seek(palette_start) 
        palette = []
        for _ in range(self.ncolors):
            red, green, blue, _ = struct.unpack('<BBBB', self.fileobj.read(4))
            palette.append((red, green, blue))
        # set palette to None instead of empty list when there's no palette
        self.palette = palette or None
    
    def read_row_32bit(self):
        row = array.array('B')
        for _ in range(self.width):
            # not sure what the first thing is used for 
            _, b, g, r =  struct.unpack('<BBBB', self.fileobj.read(4))
            row.extend([r, g, b]) # bgr->rgb
        return row
    
    def get_image(self):
        # go to the start of the pixel array
        self.fileobj.seek(self.offset)
        # since bmps are stored upside down, initialize a pixel list
        pixels = [None for _ in range(self.height)]
        # iterate BACKWARDS over the line indices so we don't have to reverse
        # later. this is why we intialize pixels above.
        for index in range(self.height - 1, -1, -1):
            pixels[index] = self.read_row()
        # TODO: Not necessarily RGB
        return Image(self.width, self.height, pixels, RGB, palette=self.palette)
