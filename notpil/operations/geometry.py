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

def _fliprow(row, pixelsize):
    """
    "flips" a row of pixels (row).
    
    with row being [1,2,3, 4,5,6, 7,8,9] and pixelsize 3 this will return an
    iterator which, if cast to a list is [7,8,9, 4,5,6, 1,2,3] (spaces added
    for readability)
    """
    tmp = deque()
    append = tmp.append
    pop = tmp.pop
    for i, x in enumerate(reversed(row), 1):
        append(x)
        if not i % pixelsize:
            while tmp:
                yield pop()

def flip_left_right(source, cls):
    """
    Horizontally flips the pixels of source into target
    """
    target = cls(source.width, source.height, [], source.mode)
    
    append = target.pixels.append
    pixelsize = source.pixelsize
    
    for line in source.pixels:
        append(array.array('B', _fliprow(line, pixelsize)))
    
    return target
