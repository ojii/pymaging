from notpil.image import Image

Image.open_image_from_path('testimage.png').flip_left_right().save_to_path('benchimage.png')

