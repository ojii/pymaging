#############
About formats
#############

Formats are classes that expose two staticmethods: ``open`` and ``save``.

``open`` takes a file-like object as argument and should either return ``None``
if the format does not accept this file, or an ``Image`` instance holding the
data. The image should be fully loaded, as the file object might be closed after
the call to ``open``.

``save`` takes an image instance and a file-like object as arguments and should
save the image instance to the file.
