from pymaging.incubator.formats.png_reader import Reader


with open('testimage.png', 'rb') as fobj:
    reader = Reader(fobj)
    reader.get_image()
