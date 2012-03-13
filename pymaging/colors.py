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
from collections import namedtuple


def _mixin_alpha(colors, alpha):
    from pymaging.utils import fdiv
    ratio = fdiv(alpha, 255)
    return [int(round(color *  ratio)) for color in colors]

class Color(object):
    def __init__(self, red, green, blue, alpha):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        
    def __str__(self):
        return 'Color: r:%s, g:%s, b:%s, a:%s' % (self.red, self.green, self.blue, self.alpha)
    
    def __repr__(self):
        return '<%s>' % self
    
    def __hash__(self):
        return hash(self.to_hexcode())
    
    def __eq__(self, other):
        return (
            self.red == other.red and
            self.green == other.green and
            self.blue == other.blue and
            self.alpha == other.alpha
        )

    @classmethod
    def from_pixel(cls, pixel):
        assert len(pixel) in (3,4), "Color.from_pixel only supports 3 and 4 value pixels"
        pixel = list(pixel)
        if len(pixel) == 3:
            pixel.append(255)
        return cls(*map(int,pixel))
    
    @classmethod
    def from_hexcode(cls, hexcode):
        hexcode = hexcode.strip('#')
        assert len(hexcode) in (3,4,6,8), "Hex codes must be 3, 4, 6 or 8 characters long"
        if len(hexcode) in (3,4):
            hexcode = ''.join(x*2 for x in hexcode)
        if len(hexcode) == 6:
            hexcode += 'ff'
        return cls(*[int(''.join(x), 16) for x in zip(hexcode[::2], hexcode[1::2])])
    
    def get_for_brightness(self, brightness):
        """
        Brightness is a float between 0 and 1
        """
        return Color(self.red, self.green, self.blue, self.alpha * brightness)
    
    def to_pixel(self, pixelsize):
        assert pixelsize in (3,4), "Color.to_pixel only supports 3 and 4 value pixels"
        if pixelsize == 3:
            return _mixin_alpha([self.red, self.green, self.blue], self.alpha)
        else:
            return [self.red, self.green, self.blue, self.alpha]
    
    def to_hexcode(self):
        return ''.join(hex(x)[2:] for x in (self.red, self.green, self.blue, self.alpha))
        

ColorType = namedtuple('ColorType', 'length')

RGB = ColorType(3)
RGBA = ColorType(4)
