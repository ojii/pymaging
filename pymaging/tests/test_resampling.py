from pymaging.tests.test_basic import PymagingBaseTestCase, image_factory
from pymaging.webcolors import Red, Green, Blue


class ResizeCropTests(PymagingBaseTestCase):
    def test_resize_nearest_resampling(self):
        img = image_factory([
            [Red, Green, Blue],
            [Green, Blue, Red],
            [Blue, Red, Green],
        ])
        img = img.resize(2, 2)
        self.assertImage(img, [
            [Red, Blue],
            [Blue, Green],
        ])
