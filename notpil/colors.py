# -*- coding: utf-8 -*-
from collections import namedtuple

def _mixin_alpha(colors, alpha):
    from notpil.utils import fdiv
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
