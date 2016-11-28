from pic import bild
from dct import dct, dct_inverse
from chroma import rgb_chroma, getY, chroma_rgb, setY
import scipy.misc
import numpy as np


def create_img(image):
    # declare picture size with RGB color
    width = 8
    height = 8
    channels = 3

    # create empty image
    img = np.zeros((height, width, channels), dtype=np.uint8)

    # fill image with picture array values
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            r, g, b = image[x][y][0], image[x][y][1], image[x][y][2]
            img[y][x][0] = r
            img[y][x][1] = g
            img[y][x][2] = b
    return img

# show original image
img = create_img(bild)
scipy.misc.imshow(img)

# chroma conversion
bildInYUV = rgb_chroma(bild)

# Extract luma
luma = getY(bildInYUV)

# do the dct on the Y only array
dimg = dct(luma)

# Here RLE and other fancy stuff might happen
# ...

# Inverse dct to get old Y value back
afterdct = dct_inverse(dimg)

# set Y in original YUV array again
afterdct = setY(bildInYUV, afterdct)
# convert to RGB again
afterdct = chroma_rgb(afterdct)
# create image
afterdct = create_img(afterdct)
# show image
scipy.misc.imshow(afterdct)


