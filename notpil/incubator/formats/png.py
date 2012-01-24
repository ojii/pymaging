# -*- coding: utf-8 -*-
from notpil.colors import RGBA
from notpil.incubator.formats.png_raw import Writer
from itertools import chain

def flat_pixels_iter(pixels):
    for row in pixels:
        yield chain(*row)

class PNG:
    @staticmethod
    def open(fileobj):
        raise NotImplementedError()
    
    @staticmethod
    def save(image, fileobj):
        writer = Writer(
            width=image.width,
            height=image.height,
            alpha=image.mode is RGBA
        )
        writer.write_packed(fileobj, flat_pixels_iter(image.pixels))
