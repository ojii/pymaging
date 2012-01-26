# -*- coding: utf-8 -*-
import struct

def int16(chart):
    return ord(chart[0]) + (ord(chart[1])<<8)

def read_raw_pixels(format, pixels):
    return [format(*struct.unpack('B' * format.length, pixels[i * format.length:(i + 1) * format.length])) for i in range(len(pixels) / format.length)]

def flat_to_nested(flatpixels, width):
    return [flatpixels[i*width:(i+1)*width] for i in range(len(flatpixels) / width)]

def get_pixel(pixels, pixelsize, x, y):
    """
    Get the pixel in an image.
    This returns a list of values, which depend on your mode.
    """
    line = pixels[y]
    start = x * pixelsize
    return line[start:start+pixelsize]
