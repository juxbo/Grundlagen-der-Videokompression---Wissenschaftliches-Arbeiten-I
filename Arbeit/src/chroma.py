from copy import copy, deepcopy

def rgb_chroma(rgbArray):
    yuvArray = deepcopy(rgbArray)
    for x, line in enumerate(rgbArray):
        for y, rgb in enumerate(line):
            r, g, b = rgb
            Y =  0.299 * r + 0.587 * g + 0.114 * b
            U = -0.299 * r - 0.587 * g + 0.886 * b
            V =  0.701 * r - 0.587 * g - 0.144 * b
            yuvArray[x][y] = (Y, U, V)
    return yuvArray

def chroma_rgb(yuvArray):
    rgbArray = deepcopy(yuvArray)
    for x, line in enumerate(yuvArray):
        for y, yuv in enumerate(line):
            Y, U, V = yuv
            r = Y + V
            g = Y - 0.509 * V - 0.194 * U
            b = Y + U
            rgbArray[x][y] = (round(r), round(g), round(b))
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
