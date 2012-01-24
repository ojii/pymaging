from PIL import Image

Image.open('testimage.png').transpose(Image.FLIP_LEFT_RIGHT).save('benchimage.png', 'PNG')