#####
Image
#####

An ``Image`` object (``pymaging.image.Image``) has following required attributes:

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
position, this should only be used for very high level operation.
