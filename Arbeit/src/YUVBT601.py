"""
    Konvertierung von RGB zu YUV und umgekehrt.
    Implementiert nach https://www.fourcc.org/fccyvrgb.php
"""

import numpy as np


def RGB2YUV(RGB):
    """ takes rgb value as tuple like (r, g, b)
    returns tuple of (y, u, v)"""
    r, g, b = RGB
    Y = 0.299 * r + 0.587 * g + 0.144 * b
    U = (b - Y) * 0.565
    V = (r - Y) * 0.713
    return (Y, U, V)

def YUV2RGB(YUV):
    """ takes yuv value as a tuple like (y, u, v)
    returns tuple of (r, g, b) """
    Y, U, V = YUV
    r = Y + 1.403 * V
    g = Y - 0.344 * U - 0.714 * V
    b = Y + 1.770 * U
    return (r, g, b)

    

