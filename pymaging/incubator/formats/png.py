# -*- coding: utf-8 -*-
from pymaging.colors import RGBA
from pymaging.incubator.formats.png_reader import Reader
from pymaging.incubator.formats.png_raw import Writer, FormatError


class PNG:
    @staticmethod
    def open(fileobj):
        reader = Reader(fileobj=fileobj)
        try:
            return reader.get_image()
        except FormatError:
            fileobj.seek(0)
            return None

    @staticmethod
    def save(image, fileobj):
        writer = Writer(
            width=image.width,
            height=image.height,
            alpha=image.mode is RGBA,
            palette=image.palette,
        )
        writer.write(fileobj, image.pixels)
