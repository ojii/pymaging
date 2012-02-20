# -*- coding: utf-8 -*-
from notpil.utils import fdiv


class Pixel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def iter_pixels(self):
        yield self.x, self.y


class Line(object):
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
    
    def iter_pixels(self):
        """
        Use Bresenham Line Algorithm:
        
        function line(x0, x1, y0, y1)
            boolean steep := abs(y1 - y0) > abs(x1 - x0)
            if steep then
                swap(x0, y0)
                swap(x1, y1)
            if x0 > x1 then
                swap(x0, x1)
                swap(y0, y1)
            int deltax := x1 - x0
            int deltay := abs(y1 - y0)
            real error := 0
            real deltaerr := deltay / deltax
            int ystep
            int y := y0
            if y0 < y1 then ystep := 1 else ystep := -1
            for x from x0 to x1
                if steep then plot(y,x) else plot(x,y)
                error := error + deltaerr
                if error ≥ 0.5 then
                    y := y + ystep
                    error := error - 1.0
        """
        steep = abs(self.end_y - self.start_y) > abs(self.end_x - self.start_x)
        if steep:
            x0, y0 = self.start_y, self.start_x
            x1, y1 = self.end_y, self.end_x
        else:
            x0, y0 = self.start_x, self.start_y
            x1, y1 = self.end_x, self.end_y
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        delta_x = x1 - x0
        delta_y = abs(y1 - y0)
        error = 0.0
        delta_error = fdiv(delta_y, delta_x)
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        
        y = y0
        
        for x in range(x0, x1):
            if steep:
                yield y, x
            else:
                yield x, y
            error += delta_error
            if error >= 0.5:
                y = y + ystep
                error = error - 1.0
