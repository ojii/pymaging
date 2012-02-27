# -*- coding: utf-8 -*-
"""
typedef struct
{
    WORD           idReserved;   // Reserved (must be 0)
    WORD           idType;       // Resource Type (1 for icons)
    WORD           idCount;      // How many images?
    ICONDIRENTRY   idEntries[1]; // An entry for each image (idCount of 'em)
} ICONDIR, *LPICONDIR;


typedef struct
{
    BYTE        bWidth;          // Width, in pixels, of the image
    BYTE        bHeight;         // Height, in pixels, of the image
    BYTE        bColorCount;     // Number of colors in image (0 if >=8bpp)
    BYTE        bReserved;       // Reserved ( must be 0)
    WORD        wPlanes;         // Color Planes
    WORD        wBitCount;       // Bits per pixel
    DWORD       dwBytesInRes;    // How many bytes in this resource?
    DWORD       dwImageOffset;   // Where in the file is this image?
} ICONDIRENTRY, *LPICONDIRENTRY;

typdef struct
{
   BITMAPINFOHEADER   icHeader;      // DIB header
   RGBQUAD         icColors[1];   // Color table
   BYTE            icXOR[1];      // DIB bits for XOR mask
   BYTE            icAND[1];      // DIB bits for AND mask
} ICONIMAGE, *LPICONIMAGE;

"""
from struct import Struct


class FileStruct(Struct):
    def unpack_from_file(self, fobj):
        return self.unpack(fobj.read(self.size))

ICONDIR = FileStruct('<HHH')


class InvalidHeaders(Exception): pass


class ICOReader(object):
    def __init__(self, fileobj):
        self.fileobj = fileobj
        self.read_headers()
    
    def read_headers(self):
        self.idreserved, self.idtype, self.idcount = ICONDIR.unpack_from_file(self.fileobj)
        if self.idreserved != 0:
            raise InvalidHeaders("idReserved must be 0") 
        if self.idtype != 1:
            raise InvalidHeaders("idType must be 1")
        if self.idcount < 1:
            raise InvalidHeaders("idCount must be at least 1 (no image found)")
    
    def get_image(self):
        pass


class ICO:
    @staticmethod
    def open(fileobj):
        try:
            reader = ICOReader(fileobj)
        except InvalidHeaders:
            return None
        return reader.get_image()
