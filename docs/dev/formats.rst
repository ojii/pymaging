#############
About formats
#############

To register a format, create an instance of :class:`pymaging.formats.Format`,
passing it a method to decode the image, a method to encode the image and a
list of extensions used for this format. Then register it in your packages
setup.py in the entry_points.

The decode method takes a file-like object as argument and should either
return ``None`` if the format does not accept this file, or an ``Image``
instance holding the data. The image should be fully loaded, as the file object
might be closed after the call to ``open``.

The encode method takes an image instance and a file-like object as arguments
and should save the image instance to the file.
