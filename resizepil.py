from PIL import Image

Image.open('testimage.png').resize((160, 240)).save('resize_benchimage.png', 'PNG')
