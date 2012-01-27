# -*- coding: utf-8 -*-
from notpil.utils import fdiv
import array


def nearest(source, width, height, pixelsize):
    assert pixelsize == 1, "yea... gotta implement this generically"
    pixels = [array.array('B', [0 for _ in  range(width)]) for _ in range(height)]
    x_ratio = fdiv(source.width, width)
    y_ratio = fdiv(source.height, height)
    for y, line in enumerate(pixels):
        source_y = int(round(y * y_ratio))
        for x, _ in enumerate(line):
            source_x = int(round(x * x_ratio))
            pixels[y][x] = source.pixels[source_y][source_x]
    return pixels
