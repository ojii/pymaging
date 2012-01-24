######
notpil
######

An alternative for the unmaintained PIL.


***********
Development
***********

Pixels are stored as flat array (``array.array``). This is mostly for
performance, but also because it seems to be the preferred format for existing
pure Python image decoders/encoders.

This is why ``Image`` has a ``pixelsize`` attribute. That attribute specifies
how "long" a pixel is. 
