# -*- coding: utf-8 -*-
from notpil.colors import WHITE
from notpil.exceptions import FormatNotSupported
from notpil.formats import get_format
from notpil.incubator import geometry

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
        pixels = [[format(*color) for _ in range(width)] for _ in range(height)]
        return cls(width, height, pixels, format)

    def resize(self, width, height):
        target = Image.empty(width, height, self.mode)
        geometry.resize(target, self, geometry.nearest_filter)
        return target
    
    def flip_vertically(self):
        target = Image.empty(self.width, self.height, self.mode)
        geometry.flip_top_bottom(target, self)
        return target
    
    def save(self, fileobj, format):
        format_object = get_format(format)
        if not format_object:
            raise FormatNotSupported(format)
        format_object.save(self, fileobj)
