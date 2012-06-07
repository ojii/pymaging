from pymaging.tests.test_basic import PymagingBaseTestCase, image_factory
from pymaging.colors import Color
from pymaging.webcolors import Red, Green, Blue
from pymaging.resample import bilinear


class ResizeNearestResamplingTests(PymagingBaseTestCase):
    def test_resize_nearest_down(self):
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

    def test_resize_nearest_down_transparent(self):
        transparent = Color(255, 255, 255, 0)
        img = image_factory([
            [Red, Green, Blue],
            [Green, Blue, Red],
            [Blue, Red, transparent],
        ])
        img = img.resize(2, 2)
        self.assertImage(img, [
            [Red, Blue],
            [Blue, transparent],
        ])

    def test_resize_nearest_up(self):
        img = image_factory([
            [Red, Blue],
            [Blue, Green],
        ])
        img = img.resize(4, 4)
        self.assertImage(img, [
            [Red, Red, Blue, Blue],
            [Red, Red, Blue, Blue],
            [Blue, Blue, Green, Green],
            [Blue, Blue, Green, Green],
        ])


class ResizeBilinearResamplingTests(PymagingBaseTestCase):
    def test_resize_bilinear_down_simple(self):
        img = image_factory([
            [Red, Blue],
            [Blue, Green],
        ])
        img = img.resize(1, 1, resample_algorithm=bilinear)
        self.assertImage(img, [
            # all the colors blended equally
            [Color(64, 32, 128, 255)]
        ])

    def test_resize_bilinear_down_proportional(self):
        img = image_factory([
            [Red, Red, Blue],
            [Red, Red, Blue],
            [Blue, Blue, Blue],
        ])
        img = img.resize(2, 2, resample_algorithm=bilinear)
        self.assertImage(img, [
            [Red, Color(64, 0, 191, 255)],
            [Color(64, 0, 191, 255), Color(16, 0, 239, 255)],
        ])

    # def test_resize_bilinear_down_transparent(self):
    #     img = image_factory([
    #         [Red, Blue],
    #         [Blue, Color(255, 255, 255, 0)],
    #     ])
    #     img = img.resize(1, 1, resample_algorithm=bilinear)
    #     self.assertImage(img, [
    #         # 3 colors blended equally,
    #         # but the transparent one should be ignored
    #         [Color(85, 0, 170, 255)]
    #     ])
