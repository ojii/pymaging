########
Overview
########


.. _about-image-objects:

*******************
About Image objects
*******************

Constructing :class:`pymaging.image.Image` objects
==================================================

:class:`pymaging.image.Image` takes a pixel array, a mode and optionally a palette as arguments. The pixel array should
be constructed with :func:`pymaging.pixelarray.get_pixel_array`. Mode should be an instance of
:class:`pymaging.colors.ColorType`. The palette, if given, indicates that the image uses a palette to lookup colors.
This that each pixel in the pixel array is actually an index into the palette, which should be a list of
:class:`pymaging.colors.Color` instances.


************
Pixel arrays
************

Pixel arrays are the core data structure in which image data is represented in pymaging. Their base class is
:class:`pymaging.pixelarray.GenericPixelArray`, but in practice they use one of the specialized subclasses. In almost
all cases, you should use :func:`pymaging.pixelarray.get_pixel_array` to construct pixel arrays, instead of using the
classes directly.

:func:`pymaging.pixelarray.get_pixel_array` takes the image **data** (as an :class:`array.array`, more on this later),
the **width** (in pixels), **height** (in pixels) and the **pixel size** as arguments and returns a, if possible
specialized, pixel array.


Pixel size
==========

The **pixel size** indicates how many bytes form a single pixel. It also describes how data is stored in the array
passed into the pixel array. A pixel size of one indicates either an image with a palette (where the bytes in the image
data are indices into the palette) or a monochrome image. Pixel size 3 is probably the most common and usually indicates
RGB, whereas pixel size 4 indicates RGBA.

Given the **pixel size**, the **data** passed into the pixel array is translated into pixels at x/y coordinates through
the APIs on pixel array.

.. module:: pymaging.pixelarray

Important methods
=================

You should hardly ever manipulate the ``data`` attribute on pixel arrays directly, instead, you should use the provided
APIs that handle things like x/y translation for the given width, height and pixel size.

Pixel array methods usually operate **in place**, if you wish to have a copy of the data, use ``copy()``.

``get(x, y)``
-------------

Returns the **pixel** (a list of ints) at the given position.

``set(x, y, pixel)``
--------------------

Sets the given pixel (list of ints) to the given position.

``remove_lines``, ``remove_columns``, ``add_lines`` and ``add_columns``
-----------------------------------------------------------------------

Those four methods are closely related and are used to resize a pixel array (and thus the image canvas). They all take
two arguments: ``amount`` and ``offset``.

.. warning::

    There is an important performance caveat with those four methods. Manipulating columns (``add_columns`` and
    ``remove_columns``) is slower the more lines there are. Therefore the column manipulating methods should always be
    called **before add_lines** or **after remove_lines** to keep the amount of lines where columns are changed the
    lowest.
