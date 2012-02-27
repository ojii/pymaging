# -*- coding: utf-8 -*-

class PymagingException(Exception): pass

class ImageModeError(PymagingException): pass
class ImageSizeMismatch(PymagingException): pass
class FormatNotSupported(PymagingException): pass
class InvalidColor(PymagingException): pass
