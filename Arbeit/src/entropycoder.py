""" Simplified Entropy Coding as used in JPEG """
import itertools
import numpy as np
import math
import huffman
import collections


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
        self.code = None
        self.addBits = None

    def length(self):
        """ Get count of bits needed to represent
        this descriptor """
        if self.code is None or self.addBits is None:
            sum = 0
            if self.timesZero > 0:
                3
            return sum + 1
        else:
            return len(self.code) + len(self.addBits)


class eob(descriptor):
    """ Descriptor that indicates End of block """
    def __init__(self):
        self.type = "eob"
        self.code = None
        self.value = "eob"

    def length(self):
        """ Get count of bits needed to represent
        this descriptor """
        if self.code is None:
            return 4
        else:
            return len(self.code)


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







def VLC_do(sequences, j):
    t = Huffman()
    if j.type == "eob":
        sequences.append("eob")
    else:
        value = j.value
        zeros = j.timesZero
        category = t.getCategoryByValue(int(value))
        sequences.append(str(zeros) + "/" + str(category))
    return sequences

def VLC(macroblocks):
    """ apply variable length encoding to list of macroblocks """
    t = Huffman()
    sequences = []
    # extract blocks from macroblocks to a flat list
    blocks = []
    for x in macroblocks:
        for y in x:
            for h in x:
                for j in (h.compressedU, h.compressedV, h.compressedY):
                    flatlist = np.array(j).flatten()
                    for b in flatlist:
                        if isinstance(b, list):
                            blocks.extend(b)
                        else:
                            blocks.append(b)
    # generate sequence to generate huffman codes
    for j in blocks:
        if j.type == "eob":
            sequences.append("eob")
        else:
            value = j.value
            zeros = j.timesZero
            category = t.getCategoryByValue(int(value))
            sequences.append(str(zeros) + "/" + str(category))
    # generate huffman table
    t.generateHuffmanTable(sequences)
    # apply codeword and additional bits to blocks
    # and count length
    size = 0
    for block in blocks:
        if j.type == "eob":
            j.code = t.getCodeByRC("eob")
        else:
            value = j.value
            zeros = j.timesZero
            category = t.getCategoryByValue(int(value))
            j.code = t.getCodeByRC(str(zeros) + "/" + str(category))
            j.addBits = t.getAdditionalBits(int(value))
        size += j.length()

    return size



class Huffman:
    """ Static class which hold the precoded huffman table """
    categories = []
    table = []
    inverse_table = []

    def __init__(self):
        self.categories = self.generateHuffmanCategory()

    def getCategoryByValue(self, value):
        if value == 0:
            raise Exception("0 is an invalid value")
        if value > 0:
            value -= 1
        return int(self.categories[1023 + value][2])

    def getAdditionalBits(self, value):
        if value == 0:
            raise Exception("0 is an invalid value")
        if value > 0:
            value -= 1
        return self.categories[1023 + value][1]

    def getCodeByRC(self, RC):
        return self.table[RC]

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

    def generateHuffmanTable(self, sequences = None):
        # generates huffman table
        # might changed to get direct input frm stream
        if sequences is  None:
            sequences = []
            for category in range(0,11):
                for run in range(0,65):
                    sequences.append(str(run) + "/" + str(category))
            sequences.append("eob")
        self.table = huffman.codebook(collections.Counter(sequences).items())
        self.inverse_table = inv_map = {v: k for k, v in self.table.items()}
