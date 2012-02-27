# -*- coding: utf-8 -*-
from copy import deepcopy
from pymaging.exceptions import (ImageModeError, ImageSizeMismatch, 
    PymagingException)
from pymaging.incubator.constants import IMAGE_TYPE_UINT8, IMAGE_TYPE_SPECIAL
from pymaging.incubator.storage import copy_info
import math
#
#/* Undef if you don't need resampling filters */
##define WITH_FILTERS
#
##define COORD(v) ((v) < 0.0 ? -1 : ((int)(v)))
COORD = lambda v: -1 if v < 0 else int(v)
##define FLOOR(v) ((v) < 0.0 ? ((int)floor(v)) : ((int)(v)))
FLOOR = lambda v: int(math.floor(v)) if v < 0 else int(v)
#
#/* -------------------------------------------------------------------- */
#/* Transpose operations                            */
#
#Imaging
#ImagingFlipLeftRight(Imaging imOut, Imaging imIn)
#{
def flip_left_right(imageout, imagein):
#    ImagingSectionCookie cookie;
#    int x, y, xr;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
    if imageout.mode != imagein.mode:
        raise ImageModeError()
#    if (imIn->xsize != imOut->xsize || imIn->ysize != imOut->ysize)
#    return (Imaging) ImagingError_Mismatch();
    if imagein.width != imageout.width or imagein.height != imageout.height:
        raise ImageSizeMismatch()
#
#    ImagingCopyInfo(imOut, imIn);
    copy_info(imageout, imagein)
#
##define    FLIP_HORIZ(image)\
    def FLIP_HORIZ(attr):
#    for (y = 0; y < imIn->ysize; y++) {\
        for y in range(0, imagein.height):
#    xr = imIn->xsize-1;\
            xr = imagein.width - 1
#    for (x = 0; x < imIn->xsize; x++, xr--)\
            for x in range(0, imagein.width):
#        imOut->image[y][x] = imIn->image[y][xr];\
                getattr(imageout, attr)[y][x] = getattr(imagein, attr)[y][xr]
                xr -= 1
#    }
#
#    ImagingSectionEnter(&cookie); NOOP!
#
#    if (imIn->image8)
    if imagein.image8:
#    FLIP_HORIZ(image8)
        FLIP_HORIZ('image8')
#    else
    else:
#    FLIP_HORIZ(image32)
        FLIP_HORIZ('image32')
#
#    ImagingSectionLeave(&cookie); NOOP!
#
    return imageout
#    return imOut;
#}
#
#
#Imaging
#ImagingFlipTopBottom(Imaging imOut, Imaging imIn)
#{
def flip_top_bottom(imageout, imagein):
#    ImagingSectionCookie cookie;
#    int y, yr;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
    if imageout.mode != imagein.mode:
        raise ImageModeError()
#    if (imIn->xsize != imOut->xsize || imIn->ysize != imOut->ysize)
#    return (Imaging) ImagingError_Mismatch();
    if imagein.width != imageout.width or imagein.height != imageout.height:
        raise ImageSizeMismatch()
#
#    ImagingCopyInfo(imOut, imIn);
    copy_info(imageout, imagein)
#
#    ImagingSectionEnter(&cookie); NOOP!
#
#    yr = imIn->ysize-1;
    yr = imagein.height - 1
#    for (y = 0; y < imIn->ysize; y++, yr--)
    for y in range(0, imagein.height):
#    memcpy(imOut->image[yr], imIn->image[y], imIn->linesize);
        imageout.pixels[yr] = deepcopy(imagein.pixels[y])
        yr -= 1
#
#    ImagingSectionLeave(&cookie); NOOP!
#
#    return imOut;
    return imageout
#}
#
#
#Imaging
#ImagingRotate90(Imaging imOut, Imaging imIn)
#{
def rotate_90(imageout, imagein):
#    ImagingSectionCookie cookie;
#    int x, y, xr;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
    if imageout.mode != imagein.mode:
        raise ImageModeError()
#    if (imIn->xsize != imOut->ysize || imIn->ysize != imOut->xsize)
#    return (Imaging) ImagingError_Mismatch();
    if imagein.width != imageout.width or imagein.height != imageout.height:
        raise ImageSizeMismatch()
#
#    ImagingCopyInfo(imOut, imIn);
    copy_info(imageout, imagein)
#
##define    ROTATE_90(image)\
    def ROTATE_90(attr):
#    for (y = 0; y < imIn->ysize; y++) {\
        for y in range(0, imagein.height):
#    xr = imIn->xsize-1;\
            xr = imagein.width - 1
#    for (x = 0; x < imIn->xsize; x++, xr--)\
            for x in range(0, imagein.width):
#        imOut->image[xr][y] = imIn->image[y][x];\
                getattr(imageout, attr)[xr][y] = getattr(imagein, attr)[y][x]
                xr -= 1
#    }
#
#    ImagingSectionEnter(&cookie); NOOP!
#
#    if (imIn->image8)
    if imagein.image8:
#    ROTATE_90(image8)
        ROTATE_90('image8')
#    else
    else:
#    ROTATE_90(image32)
        ROTATE_90('image32')
#
#    ImagingSectionLeave(&cookie); NOOP!
#
#    return imOut;
    return imageout
#}
#
#
#Imaging
#ImagingRotate180(Imaging imOut, Imaging imIn)
#{
def rotate_180(imageout, imagein):
#    ImagingSectionCookie cookie;
#    int x, y, xr, yr;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
    if imageout.mode != imagein.mode:
        raise ImageModeError()
#    if (imIn->xsize != imOut->xsize || imIn->ysize != imOut->ysize)
#    return (Imaging) ImagingError_Mismatch();
    if imagein.width != imageout.width or imagein.height != imageout.height:
        raise ImageSizeMismatch()
#
#    ImagingCopyInfo(imOut, imIn);
    copy_info(imageout, imagein)
#
#    yr = imIn->ysize-1;
    yr = imagein.height - 1
#
##define    ROTATE_180(image)\
    def ROTATE_180(attr):
#    for (y = 0; y < imIn->ysize; y++, yr--) {\
        for y in range(0, imagein.height):
#    xr = imIn->xsize-1;\
            xr = imagein.width - 1
#    for (x = 0; x < imIn->xsize; x++, xr--)\
            for x in range(0, imagein.width):
                getattr(imageout, attr)[y][x] = getattr(imagein)[yr][x]
                xr -=1
            yr -= 1
#        imOut->image[y][x] = imIn->image[yr][xr];\
#    }
#
#    ImagingSectionEnter(&cookie); NOOP!
#
#    if (imIn->image8)
    if imagein.image8:
#    ROTATE_180(image8)
        ROTATE_180('image8')
#    else
    else:
        ROTATE_180('image32')
#    ROTATE_180(image32)
#
#    ImagingSectionLeave(&cookie); NOOP!
#
#    return imOut;
    return imageout
#}
#
#
#Imaging
#ImagingRotate270(Imaging imOut, Imaging imIn)
#{
def rotate_270(imageout, imagein):
#    ImagingSectionCookie cookie;
#    int x, y, yr;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
    if imageout.mode != imagein.mode:
        raise ImageModeError()
#    if (imIn->xsize != imOut->ysize || imIn->ysize != imOut->xsize)
#    return (Imaging) ImagingError_Mismatch();
    if imagein.width != imageout.width or imagein.height != imageout.height:
        raise ImageSizeMismatch()
#
#    ImagingCopyInfo(imOut, imIn);
    copy_info(imageout, imagein)
#
#    yr = imIn->ysize - 1;
    yr = imagein.height - 1
#
##define    ROTATE_270(image)\
    def ROTATE_270(attr):
#    for (y = 0; y < imIn->ysize; y++, yr--)\
        for y in range(0, imagein.height):
#    for (x = 0; x < imIn->xsize; x++)\
            for x in range(0, imagein.width):
#        imOut->image[x][y] = imIn->image[yr][x];
                getattr(imageout, attr)[x][y] = getattr(imagein, attr)[yr][x]
                yr -= 1
#
#    ImagingSectionEnter(&cookie); NOOP!
#
#    if (imIn->image8)
    if imagein.image8:
#    ROTATE_270(image8
        ROTATE_270('image8')
#    else
    else:
#    ROTATE_270(image32)
        ROTATE_270('image32')
#
#    ImagingSectionLeave(&cookie);NOOP!
#
#    return imOut;
    return imageout
#}
#
#
#/* -------------------------------------------------------------------- */
#/* Transforms                                */
#
#/* transform primitives (ImagingTransformMap) */
#
#static int
#affine_transform(double* xin, double* yin, int x, int y, void* data)
#{
def affine_transform(x, y, data):
    """
    WARNING: Instead of manipulating 'xin' and 'yin', it RETURNS 'xin' and 'yin'
    """
#    /* full moon tonight.  your compiler will generate bogus code
#       for simple expressions, unless you reorganize the code, or
#       install Service Pack 3 */
#
#    double* a = (double*) data;
#    double a0 = a[0]; double a1 = a[1]; double a2 = a[2];
#    double a3 = a[3]; double a4 = a[4]; double a5 = a[5];
#
#    xin[0] = a0 + a1*x + a2*y;
#    yin[0] = a3 + a4*x + a5*y;
    xin = data[0] + (data[1] * x) + (data[2] * y)
    yin = data[3] + (data[4] * x) + (data[5] * y)
    return xin, yin
#
#    return 1;
#}
#
#static int
#perspective_transform(double* xin, double* yin, int x, int y, void* data)
#{
def perspective_transform(x, y, data):
    """
    WARNING: Instead of manipulating 'xin' and 'yin', it RETURNS 'xin' and 'yin'
    """
#    double* a = (double*) data;
#    double a0 = a[0]; double a1 = a[1]; double a2 = a[2];
#    double a3 = a[3]; double a4 = a[4]; double a5 = a[5];
#    double a6 = a[6]; double a7 = a[7];
#
#    xin[0] = (a0 + a1*x + a2*y) / (a6*x + a7*y + 1);
#    yin[0] = (a3 + a4*x + a5*y) / (a6*x + a7*y + 1);
    xleft, yleft = affine_transform(x, y, data)
    right = ((data[6] * x) + (data[7] * y) + 1)
    xin = xleft / right 
    yin = yleft / right
    return xin, yin
#
#    return 1;
#}
#
##if 0
#static int
#quadratic_transform(double* xin, double* yin, int x, int y, void* data)
#{
def quadratic_transform(x, y, data):
    """
    WARNING: Instead of manipulating 'xin' and 'yin', it RETURNS 'xin' and 'yin'
    """
#    double* a = (double*) data;
#
#    double a0 = a[0]; double a1 = a[1]; double a2 = a[2]; double a3 = a[3];
#    double a4 = a[4]; double a5 = a[5]; double a6 = a[6]; double a7 = a[7];
#    double a8 = a[8]; double a9 = a[9]; double a10 = a[10]; double a11 = a[11];
#
#    xin[0] = a0 + a1*x + a2*y + a3*x*x + a4*x*y + a5*y*y;
#    yin[0] = a6 + a7*x + a8*y + a9*x*x + a10*x*y + a11*y*y;
    xin = data[0] + (data[1] * x) + (data[2] * y) + (data[3] * x * x) + (data[4] * x * y) + (data[5] * y * y)
    yin = data[6] + (data[7] * x) + (data[8] * y) + (data[9] * x * x) + (data[10] * x * y) + (data[11] * y * y)
    return xin, yin 
#
#    return 1;
#}
##endif
#
#static int
#quad_transform(double* xin, double* yin, int x, int y, void* data)
#{
def quad_transform(x, y, data):
    """
    WARNING: Instead of manipulating 'xin' and 'yin', it RETURNS 'xin' and 'yin'
    """
#    /* quad warp: map quadrilateral to rectangle */
#
#    double* a = (double*) data;
#    double a0 = a[0]; double a1 = a[1]; double a2 = a[2]; double a3 = a[3];
#    double a4 = a[4]; double a5 = a[5]; double a6 = a[6]; double a7 = a[7];
#
#    xin[0] = a0 + a1*x + a2*y + a3*x*y;
#    yin[0] = a4 + a5*x + a6*y + a7*x*y;
    xin = data[0] + (data[1] * x) + (data[2] * y) + (data[3] * x * y)
    yin = data[4] + (data[5] * x) + (data[6] * y) + (data[7] * x * y)
    return xin, yin
#
#    return 1;
#}
#
#/* transform filters (ImagingTransformFilter) */
#
##ifdef WITH_FILTERS
#
#static int
#nearest_filter8(void* out, Imaging im, double xin, double yin, void* data)
#{
def nearest_filter8(image, xin, yin, data):
    """
    WARNING: Returns 'out' instead of transforming it.
    """
#    int x = COORD(xin);
#    int y = COORD(yin);
    x = COORD(xin)
    y = COORD(yin)
#    if (x < 0 || x >= im->xsize || y < 0 || y >= im->ysize)
    if (x < 0 or x >= image.width or y < 0 or y >= image.height):
#        return 0;
        return False
#    ((UINT8*)out)[0] = im->image8[y][x];
    return image.image8[y][x]
#    return 1;
#}
#
#static int
#nearest_filter16(void* out, Imaging im, double xin, double yin, void* data)
#{
def nearest_filter16(image, xin, yin, data):
    """
    WARNING: Returns 'out' instead of transforming it.
    """
#    int x = COORD(xin);
#    int y = COORD(yin);
    x = COORD(xin)
    y = COORD(yin)
#    if (x < 0 || x >= im->xsize || y < 0 || y >= im->ysize)
    if (x < 0 or x >= image.width or y < 0 or y >= image.height):
#        return 0;
        return False
#    ((INT16*)out)[0] = ((INT16*)(im->image8[y]))[x];
    return image.image8[y][x]
#    return 1;
#}
#
#static int
#nearest_filter32(void* out, Imaging im, double xin, double yin, void* data)
#{
def nearest_filter32(image, xin, yin, data):
    """
    WARNING: Returns 'out' instead of transforming it.
    """
#    int x = COORD(xin);
#    int y = COORD(yin);
    x = COORD(xin)
    y = COORD(yin)
#    if (x < 0 || x >= im->xsize || y < 0 || y >= im->ysize)
    if (x < 0 or x >= image.width or y < 0 or y >= image.height):
#        return 0;
        return False
#    ((INT32*)out)[0] = im->image32[y][x];
    return image.image8[y][x]
#    return 1;
#}
#
##define XCLIP(im, x) ( ((x) < 0) ? 0 : ((x) < im->xsize) ? (x) : im->xsize-1 )
##define YCLIP(im, y) ( ((y) < 0) ? 0 : ((y) < im->ysize) ? (y) : im->ysize-1 )
XCLIP = lambda image, x: 0 if x < 0 else x if x < image.width else image.width - 1
YCLIP = lambda image, y: 0 if y < 0 else y if y < image.height else image.height - 1
#
BILINEAR = lambda a, b, d: a + (b - a) * d


class BilinearFilter(object):
    def __init__(self, image, xin, yin, data, attr):
        if xin < 0 or xin > image.width or yin < 0 or yin >= image.height:
            raise NotPILException()
        self.image = image
        self.imagedata = getattr(self.image, attr)
        self.xin = xin
        self.yin = yin
        self.data = data
    
    def head(self):
        self.xin -= 0.5
        self.yin -= 0.5
        self.x = FLOOR(self.xin)
        self.y = FLOOR(self.yin)
        self.dx = self.xin - self.x
        self.dy = self.yin - self.y
    
    def body(self, offset, step):
        indata = self.imagedata[YCLIP(self.image, self.y)] + offset
        x0 = XCLIP(self.image, self.x)  * step
        x1 = XCLIP(self.image, self.x + 1) * step
        v1 = BILINEAR(indata[x0], indata[x1], self.dx)
        if self.y + 1 >= 0 and self.y + 1 < self.image.height:
            indata = self.imagedata[self.y + 1] + offset
            v2 = BILINEAR(indata[x0], indata[x1], self.dx)
        else:
            v2 = v1
        return BILINEAR(v1, v2, self.dy)
    
    def run(self, offset, step, converter):
        self.head()
        return converter(self.body(offset, step))

##define BILINEAR(v, a, b, d)\
#    (v = (a) + ( (b) - (a) ) * (d))
#
##define BILINEAR_HEAD(type)\
#    int x, y;\
#    int x0, x1;\
#    double v1, v2;\
#    double dx, dy;\
#    type* in;\
#    if (xin < 0.0 || xin >= im->xsize || yin < 0.0 || yin >= im->ysize)\
#        return 0;\
#    xin -= 0.5;\
#    yin -= 0.5;\
#    x = FLOOR(xin);\
#    y = FLOOR(yin);\
#    dx = xin - x;\
#    dy = yin - y;
#
##define BILINEAR_BODY(type, image, step, offset) {\
#    in = (type*) ((image)[YCLIP(im, y)] + offset);\
#    x0 = XCLIP(im, x+0)*step;\
#    x1 = XCLIP(im, x+1)*step;\
#    BILINEAR(v1, in[x0], in[x1], dx);\
#    if (y+1 >= 0 && y+1 < im->ysize) {\
#        in = (type*) ((image)[y+1] + offset);\
#        BILINEAR(v2, in[x0], in[x1], dx);\
#    } else\
#        v2 = v1;\
#    BILINEAR(v1, v1, v2, dy);\
#}
#
#static int
#bilinear_filter8(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BILINEAR_HEAD(UINT8);
#    BILINEAR_BODY(UINT8, im->image8, 1, 0);
#    ((UINT8*)out)[0] = (UINT8) v1;
#    return 1;
#}

def bilinear_filter8(image, xin, yin, data):
    """
    WARNING: Returns 'out' ('v1') instead of manipulating it
    """
    return BilinearFilter(image, xin, yin, data, 'image8').run(1, 0, int)
#
#static int
#bilinear_filter32I(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BILINEAR_HEAD(INT32);
#    BILINEAR_BODY(INT32, im->image32, 1, 0);
#    ((INT32*)out)[0] = (INT32) v1;
#    return 1;
#}

def bilinear_filter32I(image, xin, yin, data):
    """
    WARNING: Returns 'out' ('v1') instead of manipulating it
    """
    return BilinearFilter(image, xin, yin, data, 'image32').run(1, 0, int)
#
#static int
#bilinear_filter32F(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BILINEAR_HEAD(FLOAT32);
#    BILINEAR_BODY(FLOAT32, im->image32, 1, 0);
#    ((FLOAT32*)out)[0] = (FLOAT32) v1;
#    return 1;
#}

def bilinear_filter32F(image, xin, yin, data):
    """
    WARNING: Returns 'out' ('v1') instead of manipulating it
    """
    return BilinearFilter(image, xin, yin, data, 'image32').run(1, 0, float)
#
#static int
#bilinear_filter32LA(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BILINEAR_HEAD(UINT8);
#    BILINEAR_BODY(UINT8, im->image, 4, 0);
#    ((UINT8*)out)[0] = (UINT8) v1;
#    ((UINT8*)out)[1] = (UINT8) v1;
#    ((UINT8*)out)[2] = (UINT8) v1;
#    BILINEAR_BODY(UINT8, im->image, 4, 3);
#    ((UINT8*)out)[3] = (UINT8) v1;
#    return 1;
#}

def bilinear_filter32LA(image, xin, yin, data):
    """
    WARNING: Returns 'out' ('v1') instead of manipulating it
    """
    bf = BilinearFilter(image, xin, yin, data, 'image')
    bf.head()
    v1 = bf.body(4, 0)
    v2 = bf.body(4, 3)
    return (v1, v1, v1, v2)
#
#static int
#bilinear_filter32RGB(void* out, Imaging im, double xin, double yin, void* data)
#{
#    int b;
#    BILINEAR_HEAD(UINT8);
#    for (b = 0; b < im->bands; b++) {
#        BILINEAR_BODY(UINT8, im->image, 4, b);
#        ((UINT8*)out)[b] = (UINT8) v1;
#    }
#    return 1;
#}
def bilinear_filter32RGB(image, xin, yin, data):
    bf = BilinearFilter(image, xin, yin, data, 'image')
    bf.head()
    output = []
    for b in range(0, image.bands):
        output.append(int(bf.body(4, b)))
    return output
#
##define BICUBIC(v, v1, v2, v3, v4, d) {\
#    double p1 = v2;\
#    double p2 = -v1 + v3;\
#    double p3 = 2*(v1 - v2) + v3 - v4;\
#    double p4 = -v1 + v2 - v3 + v4;\
#    v = p1 + (d)*(p2 + (d)*(p3 + (d)*p4));\
#}
#
##define BICUBIC_HEAD(type)\
#    int x = FLOOR(xin);\
#    int y = FLOOR(yin);\
#    int x0, x1, x2, x3;\
#    double v1, v2, v3, v4;\
#    double dx, dy;\
#    type* in;\
#    if (xin < 0.0 || xin >= im->xsize || yin < 0.0 || yin >= im->ysize)\
#        return 0;\
#    xin -= 0.5;\
#    yin -= 0.5;\
#    x = FLOOR(xin);\
#    y = FLOOR(yin);\
#    dx = xin - x;\
#    dy = yin - y;\
#    x--; y--;
#
##define BICUBIC_BODY(type, image, step, offset) {\
#    in = (type*) ((image)[YCLIP(im, y)] + offset);\
#    x0 = XCLIP(im, x+0)*step;\
#    x1 = XCLIP(im, x+1)*step;\
#    x2 = XCLIP(im, x+2)*step;\
#    x3 = XCLIP(im, x+3)*step;\
#    BICUBIC(v1, in[x0], in[x1], in[x2], in[x3], dx);\
#    if (y+1 >= 0 && y+1 < im->ysize) {\
#        in = (type*) ((image)[y+1] + offset);\
#        BICUBIC(v2, in[x0], in[x1], in[x2], in[x3], dx);\
#    } else\
#        v2 = v1;\
#    if (y+2 >= 0 && y+2 < im->ysize) {\
#        in = (type*) ((image)[y+2] + offset);\
#        BICUBIC(v3, in[x0], in[x1], in[x2], in[x3], dx);\
#    } else\
#        v3 = v2;\
#    if (y+3 >= 0 && y+3 < im->ysize) {\
#        in = (type*) ((image)[y+3] + offset);\
#        BICUBIC(v4, in[x0], in[x1], in[x2], in[x3], dx);\
#    } else\
#        v4 = v3;\
#    BICUBIC(v1, v1, v2, v3, v4, dy);\
#}
#
#
#static int
#bicubic_filter8(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BICUBIC_HEAD(UINT8);
#    BICUBIC_BODY(UINT8, im->image8, 1, 0);
#    if (v1 <= 0.0)
#        ((UINT8*)out)[0] = 0;
#    else if (v1 >= 255.0)
#        ((UINT8*)out)[0] = 255;
#    else
#        ((UINT8*)out)[0] = (UINT8) v1;
#    return 1;
#}
#
#static int
#bicubic_filter32I(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BICUBIC_HEAD(INT32);
#    BICUBIC_BODY(INT32, im->image32, 1, 0);
#    ((INT32*)out)[0] = (INT32) v1;
#    return 1;
#}
#
#static int
#bicubic_filter32F(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BICUBIC_HEAD(FLOAT32);
#    BICUBIC_BODY(FLOAT32, im->image32, 1, 0);
#    ((FLOAT32*)out)[0] = (FLOAT32) v1;
#    return 1;
#}
#
#static int
#bicubic_filter32LA(void* out, Imaging im, double xin, double yin, void* data)
#{
#    BICUBIC_HEAD(UINT8);
#    BICUBIC_BODY(UINT8, im->image, 4, 0);
#    if (v1 <= 0.0) {
#        ((UINT8*)out)[0] = 0;
#        ((UINT8*)out)[1] = 0;
#        ((UINT8*)out)[2] = 0;
#    } else if (v1 >= 255.0) {
#        ((UINT8*)out)[0] = 255;
#        ((UINT8*)out)[1] = 255;
#        ((UINT8*)out)[2] = 255;
#    } else {
#        ((UINT8*)out)[0] = (UINT8) v1;
#        ((UINT8*)out)[1] = (UINT8) v1;
#        ((UINT8*)out)[2] = (UINT8) v1;
#    }
#    BICUBIC_BODY(UINT8, im->image, 4, 3);
#    if (v1 <= 0.0)
#        ((UINT8*)out)[3] = 0;
#    else if (v1 >= 255.0)
#        ((UINT8*)out)[3] = 255;
#    else
#        ((UINT8*)out)[3] = (UINT8) v1;
#    return 1;
#}
#
#static int
#bicubic_filter32RGB(void* out, Imaging im, double xin, double yin, void* data)
#{
#    int b;
#    BICUBIC_HEAD(UINT8);
#    for (b = 0; b < im->bands; b++) {
#        BICUBIC_BODY(UINT8, im->image, 4, b);
#        if (v1 <= 0.0)
#            ((UINT8*)out)[b] = 0;
#        else if (v1 >= 255.0)
#            ((UINT8*)out)[b] = 255;
#        else
#            ((UINT8*)out)[b] = (UINT8) v1;
#    }
#    return 1;
#}
#
#static ImagingTransformFilter
#getfilter(Imaging im, int filterid)
#{
#    switch (filterid) {
#    case IMAGING_TRANSFORM_NEAREST:

def nearest_filter(image, xin, yin, data):
#        if (im->image8)
#            switch (im->type) {
#            case IMAGING_TYPE_UINT8:
#                return (ImagingTransformFilter) nearest_filter8;
#            case IMAGING_TYPE_SPECIAL:
#                switch (im->pixelsize) {
#                case 1:
#                    return (ImagingTransformFilter) nearest_filter8;
#                case 2:
#                    return (ImagingTransformFilter) nearest_filter16;
#                case 4:
#                    return (ImagingTransformFilter) nearest_filter32;
#                }
#            }
#        else
#            return (ImagingTransformFilter) nearest_filter32;
#        break;
    if image.image8:
        if image.type == IMAGE_TYPE_UINT8:
            return nearest_filter8(image, xin, yin, data)
        elif image.type == IMAGE_TYPE_SPECIAL:
            if image.pixelsize == 1:
                return nearest_filter8(image, xin, yin, data)
            elif image.pixelsize == 2:
                return nearest_filter16(image, xin, yin, data)
            elif image.pixelsize == 4:
                return nearest_filter32(image, xin, yin, data)
    else:
        return nearest_filter32(image, xin, yin, data)
#    case IMAGING_TRANSFORM_BILINEAR:
#        if (im->image8)
#            return (ImagingTransformFilter) bilinear_filter8;
#        else if (im->image32) {
#            switch (im->type) {
#            case IMAGING_TYPE_UINT8:
#                if (im->bands == 2)
#                    return (ImagingTransformFilter) bilinear_filter32LA;
#                else
#                    return (ImagingTransformFilter) bilinear_filter32RGB;
#            case IMAGING_TYPE_INT32:
#                return (ImagingTransformFilter) bilinear_filter32I;
#            case IMAGING_TYPE_FLOAT32:
#                return (ImagingTransformFilter) bilinear_filter32F;
#            }
#        }
#        break;
#    case IMAGING_TRANSFORM_BICUBIC:
#        if (im->image8)
#            return (ImagingTransformFilter) bicubic_filter8;
#        else if (im->image32) {
#            switch (im->type) {
#            case IMAGING_TYPE_UINT8:
#                if (im->bands == 2)
#                    return (ImagingTransformFilter) bicubic_filter32LA;
#                else
#                    return (ImagingTransformFilter) bicubic_filter32RGB;
#            case IMAGING_TYPE_INT32:
#                return (ImagingTransformFilter) bicubic_filter32I;
#            case IMAGING_TYPE_FLOAT32:
#                return (ImagingTransformFilter) bicubic_filter32F;
#            }
#        }
#        break;
#    }
#    /* no such filter */
#    return NULL;
#}
#
##else
##define getfilter(im, id) NULL
##endif
#
#/* transformation engines */
#
#Imaging
#ImagingTransform(
#    Imaging imOut, Imaging imIn, int x0, int y0, int x1, int y1, 
#    ImagingTransformMap transform, void* transform_data,
#    ImagingTransformFilter filter, void* filter_data,
#    int fill)
#{
def transform(imageout, imagein, x0, y0, x1, y1, transform_map, transform_data, transform_filter, filter_data, fill):
#    /* slow generic transformation.  use ImagingTransformAffine or
#       ImagingScaleAffine where possible. */
#
#    ImagingSectionCookie cookie;
#    int x, y;
#    char *out;
#    double xx, yy;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
    if imageout.mode != imagein.mode:
        raise ImageModeError()
#
#    ImagingCopyInfo(imOut, imIn);
    copy_info(imageout, imagein)
#
#    ImagingSectionEnter(&cookie); NOOP!
#
#    if (x0 < 0)
    if x0 < 0:
#        x0 = 0;
        x0 = 0
#    if (y0 < 0)
    if y0 < 0:
#        y0 = 0;
        y0 = 0
#    if (x1 > imOut->xsize)
    if x1 > imageout.width:
#        x1 = imOut->xsize;
        x1 = imageout.width
#    if (y1 > imOut->ysize)
    if y1 > imageout.height:
#        y1 = imOut->ysize;
        y1 = imageout.height
#
#    for (y = y0; y < y1; y++) {
    for y in range(y0, y1):
#    out = imOut->image[y] + x0*imOut->pixelsize;
        out = imageout.image[y] + (x0 * imageout.pixelsize)
#    for (x = x0; x < x1; x++) {
        for x in range(x0, x1):
#        if (!transform(&xx, &yy, x-x0, y-y0, transform_data) ||
            transformed_out = transform_map(x-x0, y-y0, transform_data)
            if transformed_out:
                out = transformed_out
            filtered_out = transform_filter(imagein, filter_data)
            if filtered_out:
                out = filtered_out
#                !filter(out, imIn, xx, yy, filter_data)) {
            if (transformed_out or filtered_out) and fill:
                pass #memset?!
#                if (fill)
#                    memset(out, 0, imOut->pixelsize);
#            }
            out += imageout.pixelsize
#            out += imOut->pixelsize;
#    }
#    }
#
#    ImagingSectionLeave(&cookie);
#
    return imageout
#    return imOut;
#}
#
#static Imaging
#ImagingScaleAffine(Imaging imOut, Imaging imIn,
#                   int x0, int y0, int x1, int y1,
#                   double a[6], int fill)
#{
#    /* scale, nearest neighbour resampling */
#
#    ImagingSectionCookie cookie;
#    int x, y;
#    int xin;
#    double xo, yo;
#    int xmin, xmax;
#    int *xintab;
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
#
#    ImagingCopyInfo(imOut, imIn);
#
#    if (x0 < 0)
#        x0 = 0;
#    if (y0 < 0)
#        y0 = 0;
#    if (x1 > imOut->xsize)
#        x1 = imOut->xsize;
#    if (y1 > imOut->ysize)
#        y1 = imOut->ysize;
#
#    xintab = (int*) malloc(imOut->xsize * sizeof(int));
#    if (!xintab) {
#    ImagingDelete(imOut);
#    return (Imaging) ImagingError_MemoryError();
#    }
#
#    xo = a[0];
#    yo = a[3];
#
#    xmin = x1;
#    xmax = x0;
#
#    /* Pretabulate horizontal pixel positions */
#    for (x = x0; x < x1; x++) {
#    xin = COORD(xo);
#    if (xin >= 0 && xin < (int) imIn->xsize) {
#        xmax = x+1;
#        if (x < xmin)
#        xmin = x;
#        xintab[x] = xin;
#    }
#    xo += a[1];
#    }
#
##define    AFFINE_SCALE(pixel, image)\
#    for (y = y0; y < y1; y++) {\
#    int yi = COORD(yo);\
#    pixel *in, *out;\
#    out = imOut->image[y];\
#        if (fill && x1 > x0)\
#            memset(out+x0, 0, (x1-x0)*sizeof(pixel));\
#    if (yi >= 0 && yi < imIn->ysize) {\
#        in = imIn->image[yi];\
#        for (x = xmin; x < xmax; x++)\
#        out[x] = in[xintab[x]];\
#    }\
#    yo += a[5];\
#    }
#
#    ImagingSectionEnter(&cookie);
#
#    if (imIn->image8) {
#        AFFINE_SCALE(UINT8, image8);
#    } else {
#        AFFINE_SCALE(INT32, image32);
#    }
#
#    ImagingSectionLeave(&cookie);
#
#    free(xintab);
#
#    return imOut;
#}
#
#static inline int
#check_fixed(double a[6], int x, int y)
#{
#    return (fabs(a[0] + x*a[1] + y*a[2]) < 32768.0 &&
#            fabs(a[3] + x*a[4] + y*a[5]) < 32768.0);
#}
#
#static inline Imaging
#affine_fixed(Imaging imOut, Imaging imIn,
#             int x0, int y0, int x1, int y1,
#             double a[6], int filterid, int fill)
#{
#    /* affine transform, nearest neighbour resampling, fixed point
#       arithmetics */
#
#    int x, y;
#    int xin, yin;
#    int xsize, ysize;
#    int xx, yy;
#    int a0, a1, a2, a3, a4, a5;
#
#    ImagingCopyInfo(imOut, imIn);
#
#    xsize = (int) imIn->xsize;
#    ysize = (int) imIn->ysize;
#
#/* use 16.16 fixed point arithmetics */
##define FIX(v) FLOOR((v)*65536.0 + 0.5)
#
#    a0 = FIX(a[0]); a1 = FIX(a[1]); a2 = FIX(a[2]);
#    a3 = FIX(a[3]); a4 = FIX(a[4]); a5 = FIX(a[5]);
#
##define    AFFINE_TRANSFORM_FIXED(pixel, image)\
#    for (y = y0; y < y1; y++) {\
#    pixel *out;\
#    xx = a0;\
#    yy = a3;\
#    out = imOut->image[y];\
#        if (fill && x1 > x0)\
#            memset(out+x0, 0, (x1-x0)*sizeof(pixel));\
#        for (x = x0; x < x1; x++, out++) {\
#        xin = xx >> 16;\
#        if (xin >= 0 && xin < xsize) {\
#            yin = yy >> 16;\
#        if (yin >= 0 && yin < ysize)\
#                    *out = imIn->image[yin][xin];\
#            }\
#        xx += a1;\
#        yy += a4;\
#    }\
#    a0 += a2;\
#    a3 += a5;\
#    }
#
#    if (imIn->image8)
#    AFFINE_TRANSFORM_FIXED(UINT8, image8)
#    else
#    AFFINE_TRANSFORM_FIXED(INT32, image32)
#
#    return imOut;
#}
#
#Imaging
#ImagingTransformAffine(Imaging imOut, Imaging imIn,
#                       int x0, int y0, int x1, int y1,
#                       double a[6], int filterid, int fill)
#{
#    /* affine transform, nearest neighbour resampling, floating point
#       arithmetics*/
def transform_affine(imageout, imagein, x0, y0, x1, y1, a, resize_filter, fill):
#
#    ImagingSectionCookie cookie;
#    int x, y;
#    int xin, yin;
#    int xsize, ysize;
#    double xx, yy;
#    double xo, yo;
#
#    if (filterid || imIn->type == IMAGING_TYPE_SPECIAL) {
    if resize_filter: # for now, always True
#        /* Filtered transform */
#        ImagingTransformFilter filter = getfilter(imIn, filterid);
#        if (!filter)
#            return (Imaging) ImagingError_ValueError("unknown filter");
        return transform(imageout, imagein, x0, y0, x1, y1, affine_transform, a, resize_filter, None, fill)
#        return ImagingTransform(
#            imOut, imIn,
#            x0, y0, x1, y1,
#            affine_transform, a,
#            filter, NULL, fill);
#    }
#
#    if (a[2] == 0 && a[4] == 0)
#    /* Scaling */
#    return ImagingScaleAffine(imOut, imIn, x0, y0, x1, y1, a, fill);
#
#    if (!imOut || !imIn || strcmp(imIn->mode, imOut->mode) != 0)
#    return (Imaging) ImagingError_ModeError();
#
#    if (x0 < 0)
#        x0 = 0;
#    if (y0 < 0)
#        y0 = 0;
#    if (x1 > imOut->xsize)
#        x1 = imOut->xsize;
#    if (y1 > imOut->ysize)
#        y1 = imOut->ysize;
#
#    ImagingCopyInfo(imOut, imIn);
#
#    /* translate all four corners to check if they are within the
#       range that can be represented by the fixed point arithmetics */
#
#    if (check_fixed(a, 0, 0) && check_fixed(a, x1-x0, y1-y0) &&
#        check_fixed(a, 0, y1-y0) && check_fixed(a, x1-x0, 0))
#        return affine_fixed(imOut, imIn, x0, y0, x1, y1, a, filterid, fill);
#
#    /* FIXME: cannot really think of any reasonable case when the
#       following code is used.  maybe we should fall back on the slow
#       generic transform engine in this case? */
#
#    xsize = (int) imIn->xsize;
#    ysize = (int) imIn->ysize;
#
#    xo = a[0];
#    yo = a[3];
#
##define    AFFINE_TRANSFORM(pixel, image)\
#    for (y = y0; y < y1; y++) {\
#    pixel *out;\
#    xx = xo;\
#    yy = yo;\
#    out = imOut->image[y];\
#        if (fill && x1 > x0)\
#            memset(out+x0, 0, (x1-x0)*sizeof(pixel));\
#        for (x = x0; x < x1; x++, out++) {\
#        xin = COORD(xx);\
#        if (xin >= 0 && xin < xsize) {\
#            yin = COORD(yy);\
#        if (yin >= 0 && yin < ysize)\
#                    *out = imIn->image[yin][xin];\
#            }\
#        xx += a[1];\
#        yy += a[4];\
#    }\
#    xo += a[2];\
#    yo += a[5];\
#    }
#
#    ImagingSectionEnter(&cookie);
#
#    if (imIn->image8)
#    AFFINE_TRANSFORM(UINT8, image8)
#    else
#    AFFINE_TRANSFORM(INT32, image32)
#
#    ImagingSectionLeave(&cookie);
#
#    return imOut;
#}
#
#Imaging
#ImagingTransformPerspective(Imaging imOut, Imaging imIn,
#                            int x0, int y0, int x1, int y1,
#                            double a[8], int filterid, int fill)
#{
#    ImagingTransformFilter filter = getfilter(imIn, filterid);
#    if (!filter)
#        return (Imaging) ImagingError_ValueError("bad filter number");
#
#    return ImagingTransform(
#        imOut, imIn,
#        x0, y0, x1, y1,
#        perspective_transform, a,
#        filter, NULL,
#        fill);
#}
#
#Imaging
#ImagingTransformQuad(Imaging imOut, Imaging imIn,
#                     int x0, int y0, int x1, int y1,
#                     double a[8], int filterid, int fill)
#{
#    ImagingTransformFilter filter = getfilter(imIn, filterid);
#    if (!filter)
#        return (Imaging) ImagingError_ValueError("bad filter number");
#
#    return ImagingTransform(
#        imOut, imIn,
#        x0, y0, x1, y1,
#        quad_transform, a,
#        filter, NULL,
#        fill);
#}
#
#/* -------------------------------------------------------------------- */
#/* Convenience functions */
#
#Imaging
#ImagingResize(Imaging imOut, Imaging imIn, int filterid)
#{
def resize(imageout, imagein, resize_filter):
#    double a[6];
    a = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#
#    if (imOut->xsize == imIn->xsize && imOut->ysize == imIn->ysize)
    if imageout.width == imagein.width and imageout.height == imagein.height:
#    return ImagingCopy2(imOut, imIn);
        imageout.pixels = deepcopy(imagein.pixels)
        return imageout
#
#    memset(a, 0, sizeof a);
#    a[1] = (double) imIn->xsize / imOut->xsize;
    a[1] = float(imagein.width) / float(imageout.width)
#    a[5] = (double) imIn->ysize / imOut->ysize;
    a[5] = float(imagein.height) / float(imageout.height)
#
#    if (!filterid && imIn->type != IMAGING_TYPE_SPECIAL)
#        return ImagingScaleAffine(
#            imOut, imIn,
#            0, 0, imOut->xsize, imOut->ysize,
#            a, 1);
#
    return transform_affine(imageout, imagein, 0, 0, imageout.width, imageout.height, a, resize_filter, True)
#    return ImagingTransformAffine(
#        imOut, imIn,
#        0, 0, imOut->xsize, imOut->ysize,
#        a, filterid, 1);
#}
#
#Imaging
#ImagingRotate(Imaging imOut, Imaging imIn, double theta, int filterid)
#{
#    int xsize, ysize;
#    double sintheta, costheta;
#    double a[6];
#
#    /* Setup an affine transform to rotate around the image center */
#    theta = -theta * M_PI / 180.0;
#    sintheta = sin(theta);
#    costheta = cos(theta);
#
#    xsize = imOut->xsize;
#    ysize = imOut->ysize;
#
#    a[0] = -costheta * xsize/2 - sintheta * ysize/2 + xsize/2;
#    a[1] = costheta;
#    a[2] = sintheta;
#    a[3] = sintheta * xsize/2 - costheta * ysize/2 + ysize/2;
#    a[4] = -sintheta;
#    a[5] = costheta;
#
#    return ImagingTransformAffine(
#        imOut, imIn,
#        0, 0, imOut->xsize, imOut->ysize,
#        a, filterid, 1);
#}
