# -*- coding: utf-8 -*-
from array import array
import itertools
import struct

try:  # see :pyver:old
    array.tostring
except:
    def tostring(row):
        l = len(row)
        return struct.pack('%dB' % l, *row)
else:
    def tostring(row):
        """Convert row of bytes to string.  Expects `row` to be an
        ``array``.
        """
        return row.tostring()


# Conditionally convert to bytes.  Works on Python 2 and Python 3.
try:
    bytes('', 'ascii')
    def strtobytes(x): return bytes(x, 'iso8859-1')
    def bytestostr(x): return str(x, 'iso8859-1')
except:
    strtobytes = str
    bytestostr = str
    
try:
    itertools.count(1,2)
    icount = itertools.count
except TypeError:
    def icount(start, step):
        counter = itertools.count(start)
        while True:
            thing = counter.next()
            if (thing - start) % step == 0:
                yield thing

def irange(start, stop, step):
    """
    like range, but returns an iterator
    """
    return itertools.islice(icount(start, step), (stop-start+step-1)//step)