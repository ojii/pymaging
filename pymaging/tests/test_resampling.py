from pymaging.tests.test_basic import PymagingBaseTestCase, image_factory
from pymaging.affine import AffineTransform
from pymaging.colors import Color
from pymaging.webcolors import Red, Green, Blue
from pymaging.resample import bilinear


class NearestResamplingTests(PymagingBaseTestCase):
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

    def test_affine_rotate_nearest_90(self):
        img = image_factory([
            [Red, Blue],
            [Blue, Green],
        ])
        img = img.rotate(90)
        self.assertImage(img, [
            [Blue, Green],
            [Red, Blue],
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

    def test_resize_bilinear_down_simple_transparent(self):
        transparent = Color(255, 255, 255, 0)
        img = image_factory([
            [Red, Blue],
            [Blue, transparent],
        ])
        img = img.resize(1, 1, resample_algorithm=bilinear)

        #  - the alpha values get blended equally.
        #  - all non-alpha channels get multiplied by their alpha, so the
        #    transparent pixel does not contribute to the result.
        self.assertImage(img, [
            [Color(85, 0, 170, 191)]
        ])

    def test_resize_bilinear_down_simple_completely_transparent(self):
        transparent = Color(255, 255, 255, 0)
        img = image_factory([
            [transparent, transparent],
            [transparent, transparent],
        ])
        img = img.resize(1, 1, resample_algorithm=bilinear)

        # testing this because a naive implementation can cause div/0 error
        self.assertImage(img, [
            [Color(0, 0, 0, 0)]
        ])

    def test_resize_bilinear_down_proportional_transparent(self):
        transparent = Color(255, 255, 255, 0)
        img = image_factory([
            [Red, Red, transparent],
            [Red, Red, transparent],
            [transparent, transparent, transparent],
        ])
        img = img.resize(2, 2, resample_algorithm=bilinear)

        #  - the alpha values get blended equally.
        #  - all non-alpha channels get multiplied by their alpha, so the
        #    transparent pixel does not contribute to the result.
        self.assertImage(img, [
            [Red, Color(255, 0, 0, 64)],
            [Color(255, 0, 0, 64), Color(255, 0, 0, 16)],
        ])

    def test_resize_bilinear_no_change(self):
        img = image_factory([
            [Red, Blue],
            [Blue, Green],
        ])
        img = img.resize(2, 2, resample_algorithm=bilinear)
        self.assertImage(img, [
            [Red, Blue],
            [Blue, Green],
        ])

    def test_resize_bilinear_up_simple(self):
        img = image_factory([
            [Red, Blue],
            [Blue, Green],
        ])
        img = img.resize(4, 4, resample_algorithm=bilinear)
        self.assertImage(img, [
            [Red, Red, Blue, Blue],
            [Red, Red, Blue, Blue],
            [Blue, Blue, Green, Green],
            [Blue, Blue, Green, Green],
        ])

    def test_resize_bilinear_up_proportional(self):
        img = image_factory([
            [Red, Blue],
            [Blue, Green],
        ])
        img = img.resize(3, 3, resample_algorithm=bilinear)
        self.assertImage(img, [
            [(177, 4, 71, 255), (106, 11, 128, 255), (0, 21, 212, 255)],
            [(106, 11, 128, 255), (64, 32, 128, 255), (0, 64, 128, 255)],
            [(0, 21, 212, 255), (0, 64, 128, 255), (0, 128, 0, 255)],
        ])
