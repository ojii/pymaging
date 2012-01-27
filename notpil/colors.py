# -*- coding: utf-8 -*-
from collections import namedtuple

ColorType = namedtuple('ColorType', 'length')

RGB = ColorType(3)
RGBA = ColorType(4)
