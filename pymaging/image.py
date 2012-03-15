# -*- coding: utf-8 -*-
# Copyright (c) 2012, Jonas Obrist
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Jonas Obrist nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JONAS OBRIST BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from pymaging.colors import Color
from pymaging.exceptions import FormatNotSupported, InvalidColor
from pymaging.formats import get_format, get_format_objects
from pymaging.helpers import Fliprow
from pymaging.resample import nearest
import array
import os


class Image(object):
    def __init__(self, width, height, pixels, mode, palette=None):
        self.width = width
        self.height = height
        self.pixels = pixels
        self.mode = mode
        self.palette = palette
        self.reverse_palette = None
        self.pixelsize = 1 if self.palette else self.mode.length
    
    #==========================================================================
    # Constructors
    #==========================================================================
    
    @classmethod
    def open(cls, fileobj):
        for format in get_format_objects():
            image = format.decode(fileobj)
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
        format_object.encode(self, fileobj)

    def save_to_path(self, filepath, format=None):
        if not format:
            format = os.path.splitext(filepath)[1][1:]
        with open(filepath, 'wb') as fobj:
            self.save(fobj, format)
    
    #==========================================================================
    # Helpers
    #==========================================================================
    
    def get_reverse_palette(self):
        if self.reverse_palette is None:
            self._fill_reverse_palette()
        return self.reverse_palette

    def _fill_reverse_palette(self):
        self.reverse_palette = {}
        if not self.palette:
            return
        for index, color in enumerate(self.palette):
            color_obj = Color.from_pixel(color)
            color_obj.to_hexcode()
            self.reverse_palette[color_obj] = index
            
    #==========================================================================
    # Geometry Operations 
    #==========================================================================

    def resize(self, width, height, resample_algorithm=nearest):
        pixels = resample_algorithm(self, width, height, self.pixelsize)
        return Image(
            width,
            height,
            pixels,
            self.mode,
            self.palette,
        )

    def get_color(self, x, y):
        line = self.pixels[y]
        if self.pixelsize == 1:
            pixel = line[x]
            if self.palette:
                return Color.from_pixel(self.palette[pixel])
            else:
                return Color.from_pixel([pixel])
        else:
            start = x * self.pixelsize
            return Color.from_pixel(line[start:start+self.pixelsize])
    
    def set_color(self, x, y, color):
        if color.alpha != 255:
            base = self.get_color(x, y)
            color = base.cover_with(color)
        if self.reverse_palette and self.pixelsize == 1:
            if color not in self.reverse_palette:
                raise InvalidColor(str(color))
            index = self.reverse_palette[color]
            self.pixels[y][x] = index
        else:
            start = x * self.pixelsize
            end = start + self.pixelsize
            pixel = color.to_pixel(self.pixelsize)
            self.pixels[y][start:end] = array.array('B', pixel)

    def flip_top_bottom(self):
        """
        Vertically flips the pixels of source into target 
        """
        return Image(
            self.width,
            self.height,
            [array.array(line.typecode, line) for line in reversed(self.pixels)],
            self.mode,
            self.palette,
        )
                    
    def flip_left_right(self):
        """
        Horizontally flips the pixels of source into target
        """
        if self.pixelsize == 1:
            flipper = reversed
        else:
            flipper = Fliprow(self.width * self.pixelsize, self.pixelsize).flip
        return Image(
            self.width,
            self.height,
            [flipper(line) for line in self.pixels],
            self.mode,
            self.palette,
        )
    
    def crop(self, width, height, padding_top, padding_left):
        linestart = padding_left * self.pixelsize
        lineend = linestart + (width * self.pixelsize)
        return Image(
            width,
            height,
            [line[linestart:lineend] for line in self.pixels[padding_top:padding_top + height]],
            self.mode,
            self.palette,
        )
    
    #==========================================================================
    # Manipulation
    #==========================================================================
    
    def draw(self, shape, color):
        for x, y, pixelcolor in shape.iter_pixels(color):
            self.set_color(x, y, pixelcolor)
