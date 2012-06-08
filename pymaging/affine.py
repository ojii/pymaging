from math import pi, cos, sin

_IDENTITY = (1, 0, 0, 0, 1, 0, 0, 0, 1)


class AffineTransform(object):
    """
    2-dimensional affine-transform implementation in pure python.

    Initialise with a tuple (a, b, c, d, e, f, g, h, i), representing
    the affine transform given by the following matrix:
        | a b c |
        | d e f |
        | g h i |
    """
    def __init__(self, matrix=_IDENTITY):
        if len(matrix) == 3:
            # accept 3x3 tuples
            matrix = matrix[0] + matrix[1] + matrix[2]
        if len(matrix) != 9:
            raise ValueError("AffineTransform expects a 9-tuple, or a 3x3 tuple")
        self.matrix = tuple(matrix)

    def __repr__(self):
        return '%s(\n  %g, %g, %g,\n  %g, %g, %g,\n  %g, %g, %g\n)' % (
            (self.__class__.__name__,) + self.matrix
        )

    def __eq__(self, other):
        if not hasattr(other, 'matrix'):
            return False
        return self.matrix == other.matrix

    def __mul__(self, other):
        """
        Multiply this affine transformation by something.
        Accepts a scalar (e.g. ``self * 3``) or another AffineTransform.
        """
        if not isinstance(other, AffineTransform):
            # accept any scalar arg we can convert to float
            try:
                s = float(other)
            except (ValueError, TypeError):
                # this will throw a TypeError (unsupported operand type)
                return super(AffineTransform, self).__mult__(other)
            # scalar multiplications are the same as scale matrix multiplications
            other = AffineTransform((
                s, 0, 0,
                0, s, 0,
                0, 0, s,
            ))

        sm = self.matrix
        om = other.matrix
        return AffineTransform((
            sm[0] * om[0] + sm[1] * om[3] + sm[2] * om[6],
            sm[0] * om[1] + sm[1] * om[4] + sm[2] * om[7],
            sm[0] * om[2] + sm[1] * om[5] + sm[2] * om[8],
            sm[3] * om[0] + sm[4] * om[3] + sm[5] * om[6],
            sm[3] * om[1] + sm[4] * om[4] + sm[5] * om[7],
            sm[3] * om[2] + sm[4] * om[5] + sm[5] * om[8],
            sm[6] * om[0] + sm[7] * om[3] + sm[8] * om[6],
            sm[6] * om[1] + sm[7] * om[4] + sm[8] * om[7],
            sm[6] * om[2] + sm[7] * om[5] + sm[8] * om[8],
        ))

    def __rmul__(self, other):
        if not isinstance(other, AffineTransform):
            # support commutative multiplying for scalars
            # (i.e. 3 * A == A * 3)
            return self.__mul__(other)
        # propagate up to object, which will call other.__mul__(self)
        return super(AffineTransform, self).__rmul__(other)

    def __truediv__(self, other):
        if isinstance(other, AffineTransform):
            return self * other.inverse()
        else:
            # scalar division
            return self * (1.0 / other)
    __div__ = __truediv__

    def _determinant(self):
        """
        Returns the determinant of this 3x3 matrix.
        """
        # http://en.wikipedia.org/wiki/Inverse_matrix#Inversion_of_3.C3.973_matrices
        a, b, c, d, e, f, g, h, k = self.matrix
        return (
            a * (e * k - f * h)
            - b * (k * d - f * g)
            + c * (d * h - e * g)
        )

    def inverse(self):
        """
        Returns an AffineTransform which represents this AffineTransform's inverse.
        """
        det = self._determinant()
        if det == 0:
            # this can happen for instance if you divide by a transform whose
            # matrix is filled with zeroes.
            raise ValueError("This AffineTransform doesn't have a valid inverse.")

        # http://en.wikipedia.org/wiki/Inverse_matrix#Inversion_of_3.C3.973_matrices
        a, b, c, d, e, f, g, h, k = self.matrix
        return (1.0 / det) * AffineTransform((
            e * k - f * h, c * h - b * k, b * f - c * e,
            f * g - d * k, a * k - c * g, c * d - a * f,
            d * h - e * g, g * b - a * h, a * e - b * d,
        ))

    def rotate(self, degrees, clockwise=False):
        """
        Returns an AffineTransform which is rotated by the given number
        of degrees. Anticlockwise unless clockwise=True is given.
        """
        degrees %= 360
        if clockwise:
            degrees = 360 - degrees
        theta = degrees * pi / 180.0
        return self * AffineTransform((
            cos(theta), -sin(theta), 0,
            sin(theta), cos(theta), 0,
            0, 0, 1,
        ))

    def scale(self, factor):
        return self * factor

    def translate(self, dx, dy):
        return self * AffineTransform((
            1, 0, dx,
            0, 1, dy,
            0, 0, 1,
        ))
