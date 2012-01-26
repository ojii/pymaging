# -*- coding: utf-8 -*-
from notpil.colors import WHITE
from notpil.exceptions import FormatNotSupported
from notpil.formats import get_format
from notpil.incubator import geometry as incubator_geometry
from notpil.operations import geometry
from notpil.utils import get_pixel
import array
import os

class Image(object):
    def __init__(self, width, height, pixels, mode):
        self.width = width
        self.height = height
        self.pixels = pixels
        self.mode = mode
        self.pixelsize = self.mode.length

        # hacks
        self.palette = None
        self.image = self.pixels

    @classmethod
    def empty(cls, width, height, format, color=WHITE):
        pixels = [array.array('B', [0] * format.length * width) for _ in range(height)]
        return cls(width, height, pixels, format)

    def resize(self, width, height):
        raise NotImplementedError()
        target = Image.empty(width, height, self.mode)
        incubator_geometry.resize(target, self, incubator_geometry.nearest_filter)
        return target

    def flip_top_bottom(self):
        return geometry.flip_top_bottom(self, Image)
    
    def flip_left_right(self):
        return geometry.flip_left_right(self, Image)
    
    def crop(self, width, height, padding_top, padding_left):
        return geometry.crop(self, width, height, padding_top, padding_left, Image)
    
    def get_color(self, x, y):
        return get_pixel(self.pixels, self.pixelsize, x, y)

    def save(self, fileobj, format):
        format_object = get_format(format)
        if not format_object:
            raise FormatNotSupported(format)
        format_object.save(self, fileobj)

    def save_to_path(self, filepath, format=None):
        if not format:
            format = os.path.splitext(filepath)[1][1:]
        with open(filepath, 'wb') as fobj:
            self.save(fobj, format)
