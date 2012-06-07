from pymaging import Image
from pymaging.incubator.formats import register;register()

@profile
def run():
    Image.open_from_path('testimage.png').resize(160, 240).save_to_path('resized_benchimage.png')
run()
