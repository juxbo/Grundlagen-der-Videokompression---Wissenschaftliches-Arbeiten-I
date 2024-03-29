"""
Convert 2 dimensional arrays from RGB to YUV
representation and vice versa. Also offers
functionalities to replace Y,U or V values
arrays
"""

from YUVBT601 import RGB2YUV, YUV2RGB
from copy import copy, deepcopy
import numpy as np

def rgb_chroma(rgbArray):
    """ Covert 2 dimensional array from RGB to its YUV
    representation
    :param rgbArray: 2 dimensional array of rgb values,
                     represented as tuple of (R, G, B)
    :return: 2 dimensional array of YUV tuples
    """
    yuvArray = np.empty_like(rgbArray, np.float64)
    for x, line in enumerate(rgbArray):
        for y, rgb in enumerate(line):
            yuvArray[x][y] = RGB2YUV(rgb)
    return yuvArray

def chroma_rgb(yuvArray):
    """ Covert 2 dimensional array from YUV to its RGB
    representation
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :return: 2 dimensional array of RGB tuples
    """
    rgbArray = np.empty_like(yuvArray, np.uint8)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            R, G, B = YUV2RGB(yuv)
            if R > 255:
                R = 255
            if G > 255:
                G = 255
            if B > 255:
                B = 255
            if R < 0:
                R = 0
            if G < 0:
                G = 1
            if B < 0:
                B = 0
            yuv = (round(R), round(G), round(B))
            rgbArray[x][y] = yuv
    return rgbArray

def getY(yuvArray):
    """ Get Y values from a 2 dimensional array of
    YUV tuples
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :return: 2 dimensional array of Y values
    """
    yArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            Y, U, V = yuv
            yArray[x][y] = Y
    return yArray

def setY(yuvArray, yArray):
    """ Set Y values in a 2 dimensional array of
    YUV tuples
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :param yArray: 2 dimensional array of Y values
                   to replace with
    :return: 2 dimensional array of YUV tuples
    """
    yuvArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            # get YUV from old yuv array
            Y, U, V = yuv
            # replace old Y with new Y from yArray
            Y = yArray[x][y]
            # set new Y in yuvArray
            yuvArray[x][y] = (Y, U, V)
    return yuvArray

def getU(yuvArray):
    """ Get U values from a 2 dimensional array of
    YUV tuples
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :return: 2 dimensional array of U values
    """
    uArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            Y, U, V = yuv
            uArray[x][y] = U
    return uArray

def setU(yuvArray, uArray):
    """ Set U values in a 2 dimensional array of
    YUV tuples
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :param yArray: 2 dimensional array of U values
                   to replace with
    :return: 2 dimensional array of YUV tuples
    """
    yuvArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            # get YUV from old yuv array
            Y, U, V = yuv
            # replace old Y with new Y from yArray
            U = uArray[x][y]
            # set new Y in yuvArray
            yuvArray[x][y] = (Y, U, V)
    return yuvArray


def getV(yuvArray):
    """ Get V values from a 2 dimensional array of
    YUV tuples
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :return: 2 dimensional array of V values
    """
    vArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            Y, U, V = yuv
            vArray[x][y] = V
    return vArray

def setV(yuvArray, vArray):
    """ Set V values in a 2 dimensional array of
    YUV tuples
    :param yuvArray: 2 dimensional array of rgb values,
                     represented as tuple of (Y, U, V)
    :param yArray: 2 dimensional array of V values
                   to replace with
    :return: 2 dimensional array of YUV tuples
    """
    yuvArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            # get YUV from old yuv array
            Y, U, V = yuv
            # replace old Y with new Y from yArray
            V = vArray[x][y]
            # set new Y in yuvArray
            yuvArray[x][y] = (Y, U, V)
    return yuvArray
