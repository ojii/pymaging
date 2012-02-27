# -*- coding: utf-8 -*-
from pymaging.colors import RGBA, RGB
from pymaging.image import Image
from pymaging.incubator.formats.png_raw import Writer, Reader, FormatError, group
import array


class PNG:
    @staticmethod
    def open(fileobj):
        reader = Reader(file=fileobj)
        try:
            width, height, pixels, metadata = reader.read()
        except FormatError:
            fileobj.seek(0)
            return None
        if reader.plte:
            palette = group(array.array('B', reader.plte), 3)
        else:
            palette = None
        # TODO: Should we really `list` pixels here?
        return Image(width, height, list(pixels), RGBA if metadata.get('alpha', False) else RGB, palette)

    @staticmethod
    def save(image, fileobj):
        writer = Writer(
            width=image.width,
            height=image.height,
            alpha=image.mode is RGBA,
            palette=image.palette,
        )
        writer.write(fileobj, image.pixels)
