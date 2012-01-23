# -*- coding: utf-8 -*-
import pkg_resources

FORMATS = [entry_point.load() for entry_point in pkg_resources.iter_entry_points('notpil.formats')]

def open(fileobj):
    """
    Returns a subclass of notpil.image.Image for the format of the fileobj
    passed in, if a format can be found.
    If not format could be found, False is returned.
    """
    for format in FORMATS:
        image = format(fileobj)
        if image:
            return image
    return False
