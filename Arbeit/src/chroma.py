from copy import copy, deepcopy
from YUVBT601 import RGB2YUV, YUV2RGB
def rgb_chroma(rgbArray):
    yuvArray = deepcopy(rgbArray)
    for x, line in enumerate(rgbArray):
        for y, rgb in enumerate(line):
            yuvArray[x][y] = RGB2YUV(rgb)
    return yuvArray

def chroma_rgb(yuvArray):
    rgbArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            R, G, B = YUV2RGB(yuv)
            if R > 255:
                R = 255
            if G > 255:
                G = 255
            if B > 255:
                B = 255
            yuv = (round(R), round(G), round(B))
            rgbArray[x][y] = yuv
    return rgbArray

def getY(yuvArray):
    yArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            Y, U, V = yuv
            yArray[x][y] = Y
    return yArray

def setY(yuvArray, yArray):
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
