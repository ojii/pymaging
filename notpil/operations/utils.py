# -*- coding: utf-8 -*-
from copy import deepcopy
from notpil.exceptions import ImageModeError, ImageSizeMismatch

def copy_info(source, target):
    """
    Copies the palette of source to target
    """
    target.palette = deepcopy(source.palette)

def check_mode(im1, im2):
    if im1.mode != im2.mode:
        raise ImageModeError()

def check_size(im1, im2):
    if im1.width != im2.width or im1.height != im2.height:
        raise ImageSizeMismatch()
