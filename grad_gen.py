from PIL import Image, ImageFont
import math
import random
import numpy as np
from numpy.linalg import norm

def get_image_1(colors, image_size):
    base_color = tuple(colors[0] + [255])
    base_image = Image.new("RGBA", image_size, color=base_color)
    return base_image

def get_image_2(colors, image_size, orientation):
    colors = np.array(colors)
    imsw, imsh = image_size
    base_color = tuple(colors[0] + [255])
    base_image = Image.new("RGBA", image_size, color=base_color)
    if orientation is "vert":
        for i in range(imsh):
            color = (colors[0] * (imsh - i) + colors[1] * i) / imsh
            r, g, b = [int(val) for val in color]
            line = Image.new("RGBA", (imsw, 1), color=(r, g, b, 255))
            base_image.paste(line, box=(0, i, imsw, i + 1))
    if orientation is "hori":
        for i in range(imsw):
            color = (colors[0] * (imsw - i) + colors[1] * i) / imsw
            r, g, b = [int(val) for val in color]
            line = Image.new("RGBA", (1, imsh), color=(r, g, b, 255))
            base_image.paste(line, box=(i, 0, i + 1, imsh))
    return base_image

def get_image_3(colors, image_size):
    colors = np.array(colors)
    imsw, imsh = image_size
    down3 = ((imsw) ** 2 - (imsw/2) ** 2) ** 0.5

    base_color = tuple(colors[0] + [255])

    base_image = Image.new("RGBA", image_size, color=base_color)
    
    pixel = base_image.load()
    ones = np.ones(3)
    dist = np.zeros(3)
    avecs = np.zeros((3, 2))
    bvecs = np.zeros((3, 2))
    origins = [np.array([imsw/2, 0]), 
               np.array([0, down3]), 
               np.array([imsw, down3])]
    bvecs[0, :] = (origins[1] + origins[2]) / 2 - origins[0]
    bvecs[1, :] = (origins[2] + origins[0]) / 2 - origins[1]
    bvecs[2, :] = (origins[1] + origins[0]) / 2 - origins[2]
    bvecs[0] = bvecs[0] / norm(bvecs[0])
    bvecs[1] = bvecs[1] / norm(bvecs[1])
    bvecs[2] = bvecs[2] / norm(bvecs[2])

    for x in range(imsw):
        if x % 25 == 0:
            print(str(x // 25 + 1) + " percent done")
        for y in range(imsh):
            point = np.array([x, y])
            avecs[0, :] = origins[0] - point
            avecs[1, :] = origins[1] - point
            avecs[2, :] = origins[2] - point

            dist[0] = norm(avecs[0].dot(bvecs[0]))
            dist[1] = norm(avecs[1].dot(bvecs[1]))
            dist[2] = norm(avecs[2].dot(bvecs[2]))

            for i in range(3):
                if dist[i] < 0:
                    dist[i] = 0

            pix_col = (ones - (dist / down3)) @ colors[0:3]
            r, g, b = [int(pix) for pix in pix_col]
            pixel[x, y] = (r, g, b, 255)

    return base_image

def get_image_4(colors, image_size):
    colors = np.array(colors)
    imsw, imsh = image_size
    xdist = np.zeros((1, 2))

    base_color = tuple(colors[0] + [255])

    base_image = Image.new("RGBA", image_size, color=base_color)

    pixel = base_image.load()

    for x in range(imsw):
        if x % 25 == 0:
            print(str(x // 25 + 1) + " percent done")
        xdist[0, 0] = (imsw - x) / imsw
        xdist[0, 1] = (x) / imsw
        top = xdist @ colors[0:2]
        bottom = xdist @ colors[2:4]
        for y in range(imsh):
            color = top * (imsh - y) / imsh + bottom * y / imsh
            r, g, b = [int(val) for val in color[0]]
            pixel[x, y] = (r, g, b, 255)

    return base_image

def get_image(cols, num, image_size, orientation="vert"):
    if num is 1:
        return get_image_1(cols, image_size)
    elif num is 2:
        return get_image_2(cols, image_size, orientation)
    elif num is 3:
        return get_image_3(cols, image_size)
    elif num is 4:
        return get_image_4(cols, image_size)
    return get_image_1(cols, image_size)