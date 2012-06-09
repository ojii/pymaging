# -*- coding: utf-8 -*-
# Copyright (c) 2012, Jonas Obrist
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Jonas Obrist nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JONAS OBRIST BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__all__ = ('nearest', 'bilinear')

from pymaging.affine import AffineTransform
from pymaging.colors import Color
from pymaging.utils import fdiv
import array
import math


class Resampler(object):
    def __init__(self):
        if self.__class__ is Resampler:
            raise NotImplementedError(
                "%r is abstract, instantiate a subclass instead" % Resampler
            )
        return super(Resampler, self).__init__()

    def affine(self, transform, resize_canvas=True):
        raise NotImplementedError

    def resize(self, source, width, height):
        transform = AffineTransform().scale(
            width / float(source.width),
            height / float(source.height)
        )
        return self.affine(source, transform)


class Nearest(Resampler):
    def affine(self, source, transform, resize_canvas=True):
        # TODO optimize this. It should be faster & possible to do a matrix mult
        # for each corner, and interpolate pixel locations from there.

        # get image dimensions
        xs = []
        ys = []
        for src_corner in (
            (0, 0),
            (0, source.height),
            (source.width, 0),
            (source.width, source.height),
        ):
            dest_corner = transform * src_corner
            xs.append(dest_corner[0])
            ys.append(dest_corner[1])

        if resize_canvas:
            width = int(math.ceil(max(xs)) - math.floor(min(xs)))
            height = int(math.ceil(max(ys)) - math.floor(min(ys)))
        else:
            width = source.width
            height = source.height

        pixels = []
        pixelsize = source.pixelsize

        # transparent or black background
        background = [0] * pixelsize

        # we want to go from dest coords to src coords:
        transform = transform.inverse()

        x_range = range(width)
        y_range = range(height)
        for y in y_range:
            y += 0.5  # use the center of each pixel
            line = array.array('B')  # initialize a new line

            for x in x_range:
                x += 0.5
                source_x, source_y = transform * (x, y)
                source_x = int(source_x)
                source_y = int(source_y)

                if source_x < 0 or source_y < 0 or \
                            source_x >= source.width or source_y >= source.height:
                    line.extend(background)
                else:
                    source_x_start = source_x * pixelsize
                    source_x_end = source_x_start + pixelsize
                    line.extend(source.pixels[source_y][source_x_start:source_x_end])
            pixels.append(line)
        return pixels

    def resize(self, source, width, height):
        pixels = []
        pixelsize = source.pixelsize

        pixelappend = pixels.append  # cache for cpython
        x_ratio = fdiv(source.width, width)  # get the x-axis ratio
        y_ratio = fdiv(source.height, height)  # get the y-axis ratio

        y_range = range(height)  # an iterator over the indices of all lines (y-axis)
        x_range = range(width)  # an iterator over the indices of all rows (x-axis)
        for y in y_range:
            y += 0.5  # use the center of each pixel
            source_y = int(y * y_ratio)  # get the source line
            line = array.array('B')  # initialize a new line
            lineextend = line.extend  # cache for cypthon
            for x in x_range:
                x += 0.5  # use the center of each pixel
                source_x = int(x * x_ratio)  # get the source row
                source_x_start = source_x * pixelsize
                source_x_end = source_x_start + pixelsize
                lineextend(source.pixels[source_y][source_x_start:source_x_end])
            pixelappend(line)
        return pixels


class Bilinear(Resampler):
    def affine(self, source, transform, resize_canvas=True):
        # TODO
        raise NotImplementedError

    def resize(self, source, width, height):
        pixels = []
        x_ratio = fdiv(source.width, width)  # get the x-axis ratio
        y_ratio = fdiv(source.height, height)  # get the y-axis ratio
        pixelsize = source.pixelsize

        if source.palette:
            raise NotImplementedError("Resampling of paletted images is not yet supported")

        if x_ratio < 1 and y_ratio < 1:
            if not (width % source.width) and not (height % source.height):
                # optimisation: if doing a perfect upscale,
                # can just use nearest neighbor (it's much faster)
                return nearest.resize(source, width, height)

        has_alpha = source.mode.alpha
        color_channels_range = range(pixelsize - 1 if has_alpha else pixelsize)

        y_range = range(height)  # an iterator over the indices of all lines (y-axis)
        x_range = range(width)  # an iterator over the indices of all rows (x-axis)
        for y in y_range:
            src_y = (y + 0.5) * y_ratio - 0.5  # use the center of each pixel
            src_y_i = int(src_y)

            weight_y0 = 1 - abs(src_y - src_y_i)

            line = array.array('B')  # initialize a new line
            for x in x_range:
                src_x = (x + 0.5) * x_ratio - 0.5
                src_x_i = int(src_x)

                weight_x0 = 1 - abs(src_x - src_x_i)

                channel_sums = [0.0] * pixelsize

                # populate <=4 nearest src_pixels, taking care not to go off
                # the edge of the image.
                src_pixels = [source.get_color(src_y_i, src_x_i), None, None, None]
                if src_x_i + 1 < source.width:
                    src_pixels[1] = source.get_color(src_y_i, src_x_i + 1)
                else:
                    weight_x0 = 1
                if src_y_i + 1 < source.height:
                    src_pixels[2] = source.get_color(src_y_i + 1, src_x_i)
                    if src_x_i + 1 < source.height:
                        src_pixels[3] = source.get_color(src_y_i + 1, src_x_i + 1)
                else:
                    weight_y0 = 1

                for i, src_pixel in enumerate(src_pixels):
                    if src_pixel is None:
                        continue
                    src_pixel = src_pixel.to_pixel(pixelsize)
                    weight_x = (1 - weight_x0) if (i % 2) else weight_x0
                    weight_y = (1 - weight_y0) if (i // 2) else weight_y0
                    alpha_weight = weight_x * weight_y
                    color_weight = alpha_weight
                    alpha = 255
                    if has_alpha:
                        alpha = src_pixel[-1]
                        if not alpha:
                            continue
                        color_weight *= (alpha / 255.0)
                    for channel_index, channel_value in zip(color_channels_range, src_pixel):
                        channel_sums[channel_index] += color_weight * channel_value

                    if has_alpha:
                        channel_sums[-1] += alpha_weight * alpha
                if has_alpha:
                    total_alpha_multiplier = channel_sums[-1] / 255.0
                    if total_alpha_multiplier:  # (avoid div/0)
                        for channel_index in color_channels_range:
                            channel_sums[channel_index] /= total_alpha_multiplier

                line.extend([int(round(s)) for s in channel_sums])
            pixels.append(line)
        return pixels


nearest = Nearest()
bilinear = Bilinear()
