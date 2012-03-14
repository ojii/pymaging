# -*- coding: utf-8 -*-
from pymaging.colors import RGB
from pymaging.exceptions import FormatNotSupported
from pymaging.image import Image
from pymaging.incubator.formats.jpeg_raw import TonyJpegDecoder
import array


class JPEG:
    @staticmethod
    def open(fileobj):
        decoder = TonyJpegDecoder()
        jpegsrc = fileobj.read()
        try:
            bmpout = decoder.DecompressImage(jpegsrc)
        except:
            fileobj.seek(0)
            raise
        """
        bmpout is in bgr format, bottom to top. it has padding stuff.
        """
        pixels = []
        for reverse_y in range(0, decoder.Height):
            y = decoder.Height - reverse_y - 1
            pixels.append(array.array('B', bmpout[:3 * decoder.Width]))
            del bmpout[:3 * decoder.Width]
            del bmpout[:2] # kill padding
        return Image(decoder.Width, decoder.Height, list(reversed(pixels)), RGB)

    @staticmethod
    def save(image, fileobj):
        raise FormatNotSupported('jpeg')
    
#import TonyJpegDecoder
#try:
#  import psyco
#except ImportError:
#  psyco = None
#import sys
#
## convert from BGR to RGB
#def bgr2rgb(bmpstr):
#  return "".join([bmpstr[i*3+2]+bmpstr[i*3+1]+bmpstr[i*3] for i in range(len(bmpstr)/3)])
#
#def padrgb(bmpstr):
#  return "".join([bmpstr[i*3:i*3+3] + chr(0) for i in range(len(bmpstr)/3)])
#
#def avg(chrs):
#  if chrs:
#    return chr(int(sum(map(ord, chrs))/len(chrs)))
#  else:
#    return ""
#
#def thumbnail(bmpstr, width, height, scale, n):
#  """experimental simple thumbnail creator"""
#  tpoints = ""
#  for y in range(height/scale):
#    for x in range(width/scale):
#      points = []
#      for xs in range(scale):
#        for ys in range(scale):
#          xi = x*scale + xs
#          yi = y*scale + ys
#          if xi >= width or yi >= height: continue
#          i = xi + yi * width
#          point = bmpstr[i*n:(i+1)*n]
#          points.append(point)
#      newpoint = [avg([point[c] for point in points if point]) for c in range(n)]
#      newpoint = "".join(newpoint)
#      tpoints += newpoint
#  return tpoints, width/scale, height/scale
#
#if psyco:
#  psyco.full()
#inputfile = open(sys.argv[1], 'rb')
#jpgsrc = inputfile.read()
#inputfile.close()
#decoder = TonyJpegDecoder.TonyJpegDecoder()
#bmpout = decoder.DecompressImage(jpgsrc)
#bmpstr = "".join(map(chr, bmpout))
#bmpstr2 = bgr2rgb(bmpstr)
#if True:
#  # this bit uses PIL to save the buffer to a .bmp file
#  import Image
#  image = Image.frombuffer("RGB", (decoder.Width, decoder.Height), bmpstr2)
#  image.save(sys.argv[2])
#elif True:
#  # this uses my simple BmpFormat wrapper to do the same thing, and tries to create a thumbnail too
#  import BmpFormat
#  # bmpstr2a = padrgb(bmpstr2)
#  bmp = BmpFormat.BMPFile(decoder.Width, decoder.Height, bmpstr)
#  bmpfile = sys.argv[2]
#  open(bmpfile, "wb").write(str(bmp))
#  tstr, width, height = thumbnail(bmpstr, decoder.Width, decoder.Height, 2, 3)
#  tbmp = BmpFormat.BMPFile(width, height, tstr)
#  tbmpfile = sys.argv[2].replace(".", "t.")
#  open(tbmpfile, "wb").write(str(tbmp))
