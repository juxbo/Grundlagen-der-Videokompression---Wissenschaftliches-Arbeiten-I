from chroma import rgb_chroma, getY, chroma_rgb, setY, getU, setU, getV, setV
from copy import deepcopy
from dct import dct, idct
import numpy as np

class Macroblock:
    def __init__(self, macro):
        self.macro = macro
        self.blocks = [[[],[]],[[],[]]]
        self.extract_blocks(macro)
        self.compressedY = [[[],[]],[[],[]]]
        self.compressedU = [[[],[]],[[],[]]]
        self.compressedV = [[[],[]],[[],[]]]
        # initialize uncompressed, better might be just the generation
        # of the structure
        self.uncompressed = np.empty([2,2,8,8,3]) #deepcopy(self.blocks)

    def extract_blocks(self, macro):
        for a in range(0,2):
            for b in range(0,2):
                # extract all 8x8 blocks of this macroblock
                mula = a*8
                mulb = b*8
                block = macro[mula:mula+8,mulb:mulb+8]
                self.blocks[a][b] = block

    def get(self, x, y):
        """ returns the corresponding 8x8 block """
        return self.blocks[x][y]

    def getUncompressed(self):
        macroblock = np.empty([16,16,3])
        macroblock[0:8,0:8] = self.uncompressed[0][0]
        macroblock[0:8,8:16] = self.uncompressed[0][1]
        macroblock[8:16,0:8] = self.uncompressed[1][0]
        macroblock[8:16,8:16] = self.uncompressed[1][1]
        
        return macroblock

    def compress(self):
        self.compressY()
        self.compressU()
        self.compressV()

    def uncompress(self):
        self.uncompressY()
        self.uncompressU()
        self.uncompressV()

    def compressY(self):
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                yBlock = getY(block.tolist())
                yDCT = dct(yBlock, False)
                # Quantisierung
                # ...
                # RLE
                # ...
                self.compressedY[x][y] = yDCT

    def compressU(self):
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                uBlock = getU(block.tolist())
                uDCT = dct(uBlock, False)
                # Quantisierung
                # ...
                # RLE
                # ...
                self.compressedU[x][y] = uDCT

    def compressV(self):
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                vBlock = getV(block.tolist())
                vDCT = dct(vBlock, False)
                # Quantisierung
                # ...
                # RLE
                # ...
                self.compressedV[x][y] = vDCT

    def uncompressY(self):
        if self.compressedY[0][0]:
            for x, vblocks in enumerate(self.compressedY):
                for y, block in enumerate(vblocks):
                    # DeRLE
                    # DeQuantisierung
                    yBlock = idct(block, False)
                    self.uncompressed[x][y] = setY(self.uncompressed[x][y], yBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressU(self):
        if self.compressedU[0][0]:
            for x, vblocks in enumerate(self.compressedU):
                for y, block in enumerate(vblocks):
                    # DeRLE
                    # DeQuantisierung
                    uBlock = idct(block, False)
                    self.uncompressed[x][y] = setU(self.uncompressed[x][y], uBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressV(self):
        if self.compressedV[0][0]:
            for x, vblocks in enumerate(self.compressedV):
                for y, block in enumerate(vblocks):
                    # DeRLE
                    # DeQuantisierung
                    vBlock = idct(block, False)
                    self.uncompressed[x][y] = setV(self.uncompressed[x][y], vBlock)
        else:
            raise Exception("No compressed data there")

