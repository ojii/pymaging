# -*- coding: utf-8 -*-

class NotPILException(Exception): pass

class ImageModeError(NotPILException): pass
class ImageSizeMismatch(NotPILException): pass
