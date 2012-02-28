from pymaging.colors import RGBA, RGB
from pymaging.image import Image
from pymaging.incubator.formats.png_raw import Reader, group
import array


with open('testimage.png', 'rb') as fobj:
    reader = Reader(fileobj=fobj)
    width, height, pixels, metadata = reader.read()
    if reader.plte:
        palette = group(array.array('B', reader.plte), 3)
    else:
        palette = None
    Image(width, height, list(pixels), RGBA if metadata.get('alpha', False) else RGB, palette)
