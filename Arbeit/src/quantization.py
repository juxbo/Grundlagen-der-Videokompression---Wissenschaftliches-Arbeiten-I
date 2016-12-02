""" MPEG-1 Intracoding Quantization """

import numpy as np

# Quantization matrix used for intracoding
intracoding = [[8, 16, 19, 22, 26, 27, 29, 34],
               [16, 16, 22, 24, 27, 29, 34, 37],
               [19, 22, 26, 27, 29, 34, 34, 38],
               [22, 22, 26, 27, 29, 34, 37, 40],
               [22, 26, 27, 29, 32, 35, 40, 48],
               [26, 27, 29, 32, 35, 40, 48, 58],
               [26, 27, 29, 34, 38, 46, 56, 69],
               [27, 29, 35, 38, 46, 56, 69, 83]]

def quantize(dct, quantizer, MQuant=1):
    """ quantizes a given matrix with its given qantizer
    :param dct: DCT matrix to quantize
    :param quantizer: quantization matrix to use
    :param MQuant: quantization scale factor (1-31)
    :return: quantized 2 dimensional array of input DCT
    """
    result = np.empty_like(dct)
    for x, row in enumerate(dct):
        for y, coefficient in enumerate(row):
            if x == 0 and y == 0:
                # apply fixed qantizer to DC value
                result[x][y] = int(coefficient / 8)
            else:
                # apply specified quantization formula to AC values
                result[x][y] = int( (8 * coefficient) / (MQuant * quantizer[x][y] ))
            # results should be clipped
    return result

def dequantize(dct, quantizer, MQuant=1):
    """ dequantizes a given matrix with its given qantizer
    :param idct: DCT matrix to dequantize
    :param quantizer: quantization matrix to use
    :param MQuant: quantization scale factor
    :return: dequantized 2 dimensional array of input DCT
    """
    result = np.empty_like(dct)
    for x, row in enumerate(dct):
        for y, coefficient in enumerate(row):
            if x == 0 and y == 0:
                result[x][y] = coefficient * 8
            else:
                result[x][y] = (coefficient * quantizer[x][y] * MQuant) / 8
    return result
