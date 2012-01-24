# -*- coding: utf-8 -*-
from itertools import chain
from notpil.colors import RGBA, RGB
from notpil.image import Image
from notpil.incubator.formats.png_raw import Writer, Reader, FormatError

def flat_pixels_iter(pixels):
    for row in pixels:
        yield chain(*row)

class PNG:
    @staticmethod
    def open(fileobj):
        reader = Reader(file=fileobj)
        try:
            width, height, pixels, metadata = reader.read()
        except FormatError:
            fileobj.seek(0)
            return None
        # TODO: Should we really `list` pixels here?
        return Image(width, height, list(pixels), RGBA if metadata.get('alpha', False) else RGB)

    @staticmethod
    def save(image, fileobj):
        writer = Writer(
            width=image.width,
            height=image.height,
            alpha=image.mode is RGBA
        )
        writer.write(fileobj, image.pixels)
