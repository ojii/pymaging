######
notpil
######

An alternative for the unmaintained PIL.


***********
Development
***********

Pixels are stored as a list of arrays (``array.array``). Actual pixels can be
retrieved by reading ``Image.pixelsize`` ints from the array.


***********
Play around
***********

    git clone git@github.com:ojii/notpil.git
    cd notpil
    python

    >>> from notpil.image import Image
    >>> img = Image.open_from_path('/path/to/your/image.png')
    >>> # do cool stuff with img
    >>> img.save_to_path('/foo/bar.png')
