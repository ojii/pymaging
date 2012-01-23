# -*- coding: utf-8 -*-
from notpil.incubator.formats.gif_raw import ImageLoaderGIF


def load_gif(fileobj):
    return ImageLoaderGIF().load(fileobj)
