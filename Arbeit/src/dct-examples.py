import dct
import numpy as np
from encode_decode import create_img
import scipy.misc

def example1():
    # This 8x8 pixel matrix shows an easy compressable Block if we use dct
    # represents the dct matrix
    x = np.zeros([8,8])
    x[0][0] = 800
    x[0][1] = 200
    x[1][0] = 200

    return x

def showExample1():
    # load dct matrix
    m = example1()
    # do the idct
    m = dct.idct(m)
    # generate rgb picture
    for x, row in enumerate(m):
        for y, value in enumerate(row):
            m[x][y] = [value, value, value]
    # generate image and show it
    scipy.misc.imshow(create_img(m))

showExample1()
