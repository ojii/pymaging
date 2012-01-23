# -*- coding: utf-8 -*-
from collections import namedtuple

Color = namedtuple('Color', 'red green blue alpha')

WHITE = Color(255, 255, 255, 255)
BLACK = Color(0, 0, 0, 255)


def RGB(red, green, blue, alpha):
    return Color(red, green, blue, 255)
RGB.length = 3

def RGBA(red, green, blue, alpha):
    return Color(red, green, blue, alpha)
RGBA.length = 4
