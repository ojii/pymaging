# -*- coding: utf-8 -*-
from notpil.incubator.formats.gif_raw import ImageLoaderGIF


class GIF:
    @staticmethod
    def open(fileobj):
        return ImageLoaderGIF().load(fileobj)
        
    @staticmethod
    def save(image, fileobj):
        raise NotImplementedError()
