######
notpil
######

An alternative for the unmaintained PIL.


***********
Development
***********

An ``Image`` object (``notpil.image.Image``) has following required attributes:

* ``width``: Width of the image in pixels
* ``height``: Height of the image in pixels
* ``pixels``: A list of arrays (``array.array``). Each array in the list is a
              **line** in the image. Each array is the actual image data for
              that line in the image.
* ``mode``: The color mode (RGB/RGBA).
* ``palette``: The palette object (a list of colors represented as lists) or
               ``None`` if the image has no palette.
* ``pixelsize``: The size of a pixel in the array.


About pixelsize
===============

If ``pixelsize`` is ``1`` and the ``palette`` is set, the actual values stored
in ``pixels`` are actually indices into the ``palette``. So to get the actual
data (color) can be fetched using ``palette[pixelvalue]``. Otherwise you can
get the data (color) using ``pixels[y][x * pixelsize:(x * pixelsize) + pixelsize]``.

There is also the helper method ``Image.get_color`` to get a color at a x/y
position.


About ``incubator``
===================

The ``incubator`` submodule is there to hack around new format/feature support.

It's just there to make development easier, once something is reasonably stable
it should be moved out. In case of formats, they should be moved to their own
repos/packages. In case of features, move them to ``Image`` or other appropriate
places.


About formats
=============

Formats are classes that expose two staticmethods: ``open`` and ``save``.

``open`` takes a file-like object as argument and should either return ``None``
if the format does not accept this file, or an ``Image`` instance holding the
data. The image should be fully loaded, as the file object might be closed after
the call to ``open``.

``save`` takes an image instance and a file-like object as arguments and should
save the image instance to the file.


***********
Play around
***********

Requires ``distribute`` or ``setuptools`` to be installed.

Run this in your shell::

    git clone git@github.com:ojii/notpil.git
    cd notpil
    python


Do something like this in python::

    >>> from notpil.image import Image
    >>> img = Image.open_from_path('/path/to/your/image.png')
    >>> # do cool stuff with img
    >>> img.save_to_path('/foo/bar.png')


*********
Run Tests
*********

For now, use ``python -m unittest discover`` to run the tests.
