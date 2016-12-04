""" Simplified Entropy Coding as used in JPEG """
import itertools
import numpy as np
import math
class descriptor:
    def __init__(self):
        self.type = "descriptor"
    def length(self):
        raise NotImplementedError

class ac(descriptor):
    """ Descriptor for AC values """
    def __init__(self, value, timesZero):
        self.type = "ac"
        self.value = value
        self.timesZero = timesZero
    def length(self):
        sum = 0
        if self.timesZero > 0:
            3
        return sum + 1

class eob(descriptor):
    """ Descriptor that indicates End of block """
    def __init__(self):
        self.type = "eob"
    def length(self):
        return 4

def encode(dct):
    # RLE
    return RLEzigZag(dct)

def decode(rle):
    # DeRLE
    result = deRLEzigZag(rle, 8)
    return result

def RLEzigZag(dct):
    """ Zig Zag Run length encoding
    :param dct: (quantized) DCT -> 8x8 array
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
    result.append(eob())
    return result

def deRLEzigZag(rle, dim=8):
    """ Zig Zag Run length decoding
    param rle: Output from RLEzigZag """
    moves = zigZag(dim)
    moveIndex = 0
    result = np.zeros([dim,dim], np.float64)
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
    :return: list of tuples like (x, y) """

    moves = []
    # Zig
    for index in range(0,dim):
        if (index % 2) != 0:
            x = 0
            y = index
            even = False
        else:
            x = index
            y = 0
            even = True
        for run in range(0,index + 1):
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










class Huffman:
    """ Static class which hold the precoded huffman table """
    categories = []
    table = []

    def getHuffman(self):
        """ :return: generated huffman table """
        if len(self.categories) == 0:
            self.categories = self.generateHuffmanCategories()
        return self.categories

    def getAdditionalBits(self, value):
        self.getHuffman()
        if value == 0:
            raise Exception("0 is an invalid value")
        if value > 0:
            value -= 1
        return self.categories[1023 + value]

    def generateHuffmanCategory(self):
        """ generate predefined huffman table
        :return: array of [Value, Additional Bits, Category]"""
        table = []
        for category in range(1, 11):
            values = list(itertools.product([0, 1], repeat=category))
            # get positive start and end values
            start = int(math.pow(2, category-1))
            end = int(start + len(values)/2) - 1
            valuesPointer = 0
            # build negative list
            for i in range(-1 * end, -1 * start + 1):
                table.append([i, values[valuesPointer], category])
                valuesPointer += 1
            # build positive list
            for i in range(start, end + 1):
                table.append([i, values[valuesPointer], category])
                valuesPointer += 1
        table.sort()
        return table

    def generateCodeWords(self):
        raise NotImplementedError

    def generateHuffmanTable(self):
        raise NotImplementedError
