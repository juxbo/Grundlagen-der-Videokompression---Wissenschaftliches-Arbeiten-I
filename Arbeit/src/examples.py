import numpy as np


orange = (255, 140, 0)
blue   = (0, 0, 255)
green  = (0, 255, 0)


def example1():
    # this matrix shall show the lost information
    # while subsampling on sharp colored edges
    example1 = np.full([16, 16, 3], orange, np.uint8)
    bluearray = np.full([16, 11, 3], blue, np.uint8)
    example1[0:16, 2:13] = bluearray
    return example1
