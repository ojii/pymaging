# -*- coding: utf-8 -*-
from pymaging.incubator.formats.gif_raw import ImageLoaderGIF


class GIF:
    @staticmethod
    def open(fileobj):
        return None
        # need to make it return an array!
        return ImageLoaderGIF().load(fileobj)
        
    @staticmethod
    def save(image, fileobj):
        raise NotImplementedError()
