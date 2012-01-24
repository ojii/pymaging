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

def _fliprow(iterable, pixelsize):
    tmp = deque(maxlen=pixelsize)
    for i, x in enumerate(reversed(iterable), 1):
        tmp.append(x)
        if not i % pixelsize:
            while tmp:
                yield tmp.pop()

def flip_left_right(source, target):
    """
    Horizontally flips the pixels of source into target
    """
    # check mode match
    check_mode(source, target)
    # check size match
    check_size(source, target)
    # copy palette
    copy_info(source, target)
    
    for index, line in enumerate(source.pixels):
        target.pixels[index] = array.array('B', _fliprow(line, source.pixelsize))
    
    return target
