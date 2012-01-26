# -*- coding: utf-8 -*-
from notpil.exceptions import FormatNotSupported
from notpil.formats import get_format, get_format_objects
from notpil.helpers import Fliprow
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
    
    #==========================================================================
    # Constructors
    #==========================================================================
    
    @classmethod
    def open(cls, fileobj):
        for format in get_format_objects():
            image = format.open(fileobj)
            if image:
                return image
        raise FormatNotSupported()

    @classmethod
    def open_from_path(cls, filepath):
        with open(filepath, 'rb') as fobj:
            return cls.open(fobj)
        
    #==========================================================================
    # Saving 
    #==========================================================================

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
            
    #==========================================================================
    # Geometry Operations 
    #==========================================================================

    def resize(self, width, height, algorithm=Nearest):
        raise NotImplementedError()
        target = Image.empty(width, height, self.mode)
        incubator_geometry.resize(target, self, incubator_geometry.nearest_filter)
        return target

    def get_color(self, x, y):
        return get_pixel(self.pixels, self.pixelsize, x, y)

    def flip_top_bottom(self):
        """
        Vertically flips the pixels of source into target 
        """
        return Image(
            self.width,
            self.height,
            [array.array(line.typecode, line) for line in reversed(self.pixels)],
            self.mode
        )
                    
    def flip_left_right(self):
        """
        Horizontally flips the pixels of source into target
        """
        flipper = Fliprow(self.width * self.pixelsize, self.pixelsize)
        return Image(
            self.width,
            self.height,
            [flipper.flip(line) for line in self.pixels],
            self.mode
        )
    
    def crop(self, width, height, padding_top, padding_left):
        linestart = padding_left * self.pixelsize
        lineend = linestart + (width * self.pixelsize)
        return Image(
            width,
            height,
            [line[linestart:lineend] for line in self.pixels[padding_top:padding_top + height]],
            self.mode
        )
