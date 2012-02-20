# -*- coding: utf-8 -*-
from notpil.colors import Color
from notpil.exceptions import InvalidColor
import array

def get_pixel(pixels, pixelsize, x, y, palette):
    """
    Get the pixel in an image.
    This returns a list of values, which depend on your mode.
    """
    line = pixels[y]
    if pixelsize == 1:
        pixel = line[x]
        if palette:
            return Color.from_pixel(palette[pixel])
        else:
            return Color.from_pixel([pixel])
    else:
        start = x * pixelsize
        return Color.from_pixel(line[start:start+pixelsize])

def set_pixel(pixels, pixelsize, x, y, reverse_palette, color):
    if reverse_palette and pixelsize == 1:
        if color not in reverse_palette:
            raise InvalidColor(str(color))
        index = reverse_palette[color]
        pixels[y][x] = index
    else:
        start = x * pixelsize
        end = x * pixelsize
        pixel = color.to_pixel(pixelsize)
        pixels[y][start:end] = array.array('B', pixel)

def fdiv(a, b):
    return float(a) / float(b)
