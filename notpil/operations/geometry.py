# -*- coding: utf-8 -*-
import array
from collections import deque


def flip_top_bottom(source, cls):
    """
    Vertically flips the pixels of source into target 
    """
    return cls(
        source.width,
        source.height,
        [array.array(line.typecode, line) for line in reversed(source.pixels)],
        source.mode
    )


class Fliprow(object):
    def __init__(self, rowlength, pixelsize):
        self.indices = deque()
        indicesappend = self.indices.append
        tmp = deque()
        append = tmp.append
        pop = tmp.pop
        for i in range(rowlength - 1, -1, -1):
            append(i)
            if not i % pixelsize:
                while tmp:
                    indicesappend(pop())
    
    def flip(self, row):
        return array.array('B', (row[i] for i in self.indices))
                
def flip_left_right(source, cls):
    """
    Horizontally flips the pixels of source into target
    """
    flipper = Fliprow(source.width * source.pixelsize, source.pixelsize)
    target = cls(source.width, source.height, [flipper.flip(line) for line in source.pixels], source.mode)
    return target

def crop(source, width, height, padding_top, padding_left, cls):
    linestart = padding_left * source.pixelsize
    lineend = linestart + (width * source.pixelsize)
    return cls(
        width,
        height,
        [line[linestart:lineend] for line in source.pixels[padding_top:padding_top + height]],
        source.mode
    )
