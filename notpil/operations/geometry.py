# -*- coding: utf-8 -*-
from copy import deepcopy
from notpil.operations.utils import copy_info, check_mode, check_size


def flip_vertically(source, target):
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
        target.pixels[index] = deepcopy(line)

    # return target
    return target
