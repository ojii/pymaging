# -*- coding: utf-8 -*-

def get_pixel(pixels, pixelsize, x, y, palette, colorlength):
    """
    Get the pixel in an image.
    This returns a list of values, which depend on your mode.
    """
    line = pixels[y]
    if pixelsize == 1:
        pixel = line[x]
        if palette:
            return palette[pixel]
        else:
            return [pixel]
    else:
        start = x * pixelsize
        return line[start:start+pixelsize]

def fdiv(a, b):
    return float(a) / float(b)
