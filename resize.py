from notpil.image import Image

Image.open_from_path('testimage.png').resize(160, 240).save_to_path('resized_benchimage.png')
