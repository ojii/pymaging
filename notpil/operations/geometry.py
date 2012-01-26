# -*- coding: utf-8 -*-
from notpil.operations.utils import copy_info, check_mode, check_size
import array
from collections import deque


def flip_top_bottom(source, target):
    """
    Vertically flips the pixels of source into target 
    """
    # check mode match
    check_mode(source, target)
    # check size match
    check_size(source, target)
    # copy palette
    copy_info(source, target)

    # copy pixels reversed (y axis)
    for index, line in enumerate(reversed(source.pixels)):
        target.pixels[index] = array.array(line.typecode, line)

    # return target
    return target


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
