import numpy as np

def RGB2YUV(RGB):
    """ takes rgb value as tuple like (r, g, b)
    returns tuple of (y, u, v)"""
    r, g, b = RGB
    Y = 0.299 * r + 0.587 * g + 0.144 * b
    U = (b - Y) * 0.493
    V = (r - Y) * 0.877
    return (Y, U, V)

def YUV2RGB(YUV):
    """ takes yuv value as a tuple like (y, u, v)
    returns tuple of (r, g, b) """
    Y, U, V = YUV
    r = Y + U/0.493
    b = Y + V/0.877
    g = (1/0.587) * Y - (0.299/0.587) * r - (0.144/0.587) * b
    return (r, g, b)

    

