# -*- coding: utf-8 -*-
from pymaging.utils import fdiv
import array


def nearest(source, width, height, pixelsize):
    assert pixelsize == 1, "yea... gotta implement this generically"
    pixels = []
    pixelappend = pixels.append # cache for cpython
    x_ratio = fdiv(source.width, width) # get the x-axis ratio
    y_ratio = fdiv(source.height, height) # get the y-axis ratio
    y_range = range(height) # an iterator over the indices of all lines (y-axis)
    x_range = range(width) # an iterator over the indices of all rows (x-axis)
    for y in y_range:
        source_y = int(round(y * y_ratio)) # get the source line
        line = array.array('B') # initialize a new line
        lineappend = line.append # cache for cypthon
        for x in x_range:
            source_x = int(round(x * x_ratio)) # get the source row
            lineappend(source.pixels[source_y][source_x])
        pixelappend(line)
    return pixels
