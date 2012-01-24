from notpil.api import open_image_from_path

open_image_from_path('testimage.png').flip_left_right().save_to_path('benchimage.png')

