""" Simplified Entropy Coding as used in JPEG """
import itertools
import numpy as np
import math
class descriptor:
    def __init__(self):
        self.type = "descriptor"
    def length():
        raise NotImplementedError

class ac(descriptor):
    """ Descriptor for AC values """
    def __init__(self, value):
        self.type = "dc"
        self.value = 0


class Huffman:
    """ Static class which hold the precoded huffman table """
    table = []

    def getHuffman(self):
        """ :return: generated huffman table """
        if len(self.table) == 0:
            self.table = self.generateHuffman()
        return self.table

    def getAdditionalBits(self, value):
        self.getHuffman()
        if value == 0:
            raise Exception("0 is an invalid value")
        if value > 0:
            value -= 1
        return self.table[1023 + value]

    def generateHuffman(self):
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


