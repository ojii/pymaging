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

from pymaging.utils import fdiv
import array


def nearest(source, width, height):
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


def bilinear(source, width, height):
    pixels = []
    x_ratio = fdiv(source.width, width)  # get the x-axis ratio
    y_ratio = fdiv(source.height, height)  # get the y-axis ratio
    pixelsize = source.pixelsize

    if x_ratio < 1 and y_ratio < 1:
        if not (width % source.width) and not (height % source.height):
            # optimisation: if doing a perfect upscale,
            # can just use nearest neighbor (it's much faster)
            return nearest(source, width, height, pixelsize)

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
                weight = weight_x * weight_y
                for channel_index, channel_value in enumerate(src_pixel):
                    channel_sums[channel_index] += weight * channel_value

            line.extend([int(round(s)) for s in channel_sums])
        pixels.append(line)
    return pixels
