from pymaging.incubator.formats.jpeg import JPEG

with open('testdata/black-white-100.jpg', 'rb') as fobj:
    img = JPEG.open(fobj)
    img.save_to_path('jpegtest.png')
