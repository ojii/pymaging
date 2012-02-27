# -*- coding: utf-8 -*-
import array
from collections import deque

class Fliprow(object):
    def __init__(self, rowlength, pixelsize):
        self.indices = deque()
        indicesappend = self.indices.append
        tmp = deque()
        append = tmp.append
        pop = tmp.pop
        for i in range(rowlength - 1, -1, -1):
            append(i)
            if not i % pixelsize:
                while tmp:
                    indicesappend(pop())
    
    def flip(self, row):
        return array.array('B', (row[i] for i in self.indices))
