""" Simplified Entropy Coding as used in JPEG """
import numpy as np
import math


class descriptor:
    """ base descriptor class """
    def __init__(self):
        self.type = "descriptor"

    def length(self):
        raise NotImplementedError


class ac(descriptor):
    """ Descriptor for AC values """
    def __init__(self, value, timesZero):
        """
        :param value: value to save in descriptor
        :param timesZero: count of leading zeros
        """
        self.type = "ac"
        self.value = value
        self.timesZero = timesZero

    def length(self):
        """ Get count of values in this descriptor """
        sum = 0
        if self.timesZero > 1:
            sum += 2
        elif self.timesZero > 0:
            sum += 1
        return sum + 1


class eob(descriptor):
    """ Descriptor that indicates End of block """
    def __init__(self):
        self.type = "eob"
        self.value = "eob"

    def length(self):
        """ Get count of values in this descriptor """
        return 1


def encode(dct):
    """ Apply RLE
    :param dct: 8x8 array
    :return: list of rle descriptors
    """
    # RLE
    return RLEzigZag(dct)


def decode(rle):
    """ Reverse RLE
    :param rle: list of rle descriptors
    :return: 8x8 array of restored values
    """
    # DeRLE
    result = deRLEzigZag(rle, 8)
    return result


def RLEzigZag(dct):
    """ Zig Zag Run length encoding
    :param dct: 8x8 array
    :return: list of rle descriptors
    """
    moves = zigZag(len(dct))
    result = []
    values = []
    for move in moves:
        x, y = move
        value = dct[x][y]
        if value != 0:
            result.append(ac(value, len(values)))
            values = []
        else:
            values.append(value)
    if len(values) > 0:
        result.append(eob())
    return result


def deRLEzigZag(rle, dim=8):
    """ Zig Zag Run length decoding
    :param rle: list of rle descriptors
    :return: 8x8 array of restored values
    """
    moves = zigZag(dim)
    moveIndex = 0
    result = np.zeros([dim, dim], np.float64)
    for value in rle:
        if value.type == "eob":
            break
        elif value.type == "ac":
            for i in range(0, value.timesZero):
                x, y = moves[moveIndex]
                moveIndex += 1
                result[x][y] = 0
            x, y = moves[moveIndex]
            moveIndex += 1
            result[x][y] = value.value
        else:
            raise Exception("Unknown type encoded in RLE list: " + str(value.type))
    return result


def zigZag(dim):
    """ Calculate zig zag moves for a matrix of given dimension
    :param dim: dimension of the matrix
    :return: list of tuples like (x, y)
    """

    moves = []
    # Zig
    for index in range(0, dim):
        if (index % 2) != 0:
            x = 0
            y = index
            even = False
        else:
            x = index
            y = 0
            even = True
        for run in range(0, index + 1):
            moves.append((x, y))
            if not even:
                x += 1
                y -= 1
            else:
                x -= 1
                y += 1
            if x >= dim or x < 0 or y >= dim or y < 0:
                break
    # Zag
    for index in range(1, dim):
        if (index % 2) != 0:
            x = dim - 1
            y = index
            even = False
        else:
            x = index
            y = dim - 1
            even = True
        for run in range(0, dim + 1):
            moves.append((x, y))
            if not even:
                x -= 1
                y += 1
            else:
                x += 1
                y -= 1
            if x >= dim or x < 0 or y >= dim or y < 0:
                break
    return moves
