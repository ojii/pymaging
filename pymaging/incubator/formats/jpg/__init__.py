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
from pymaging.exceptions import FormatNotSupported
from pymaging.formats import Format
from pymaging.image import Image
from pymaging.incubator.formats.jpg.raw import TonyJpegDecoder
import array

def decode(fileobj):
    decoder = TonyJpegDecoder()
    jpegsrc = fileobj.read()
    try:
        bmpout = decoder.DecompressImage(jpegsrc)
    except:
        fileobj.seek(0)
        raise
    # bmpout is in bgr format, bottom to top. it has padding stuff.
    pixels = []
    for _ in range(0, decoder.Height):
        #TODO: flip bgr to rgb
        pixels.append(array.array('B', bmpout[:3 * decoder.Width]))
        del bmpout[:3 * decoder.Width]
        del bmpout[:2] # kill padding
    return Image(decoder.Width, decoder.Height, list(reversed(pixels)), RGB)

def encode(image, fileobj):
    raise FormatNotSupported('jpeg')

JPG = Format(decode, encode, ['jpg', 'jpeg'])
