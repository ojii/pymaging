# -*- coding: utf-8 -*-

class RGB(object):
    def __init__(self, data):
        self.palette = data or range(256) *  3
        self.colors = {}
        if 768 != len(self.palette):
            raise ValueError("Invalid palette size for RGB palette, expected size 768, got %s" % len(self.palette))
