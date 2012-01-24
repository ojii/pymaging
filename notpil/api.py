# -*- coding: utf-8 -*-
from notpil.formats import get_format_objects

def open_image(fileobj):
    """
    Returns a subclass of notpil.image.Image for the format of the fileobj
    passed in, if a format can be found.
    If not format could be found, False is returned.
    """
    for format in get_format_objects():
        image = format.open(fileobj)
        if image:
            return image
    return False

def open_image_from_path(filepath):
    with open(filepath, 'rb') as fobj:
        return open_image(fobj)
