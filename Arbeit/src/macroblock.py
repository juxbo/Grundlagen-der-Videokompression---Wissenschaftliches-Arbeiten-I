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
        self.uncompressed = np.empty([2,2,8,8,3], np.float64) #deepcopy(self.blocks)

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

    def subsample(self, block):
        result = np.empty([4,4], np.float64)
        block = np.array(block)
        for x in range(0,4):
            for y in range(0,4):
                xmul = x*2
                ymul = y*2
                result[x][y] = np.average(block[xmul:xmul+2,ymul:ymul+2])
        return result

    def upsample(self, block):
        result = np.empty([16,16], np.float64)
        for x in range(0,8):
            for y in range(0,8):
                xmul = x*2
                ymul = y*2
                result[xmul:xmul+2,ymul:ymul+2].fill(block[x][y])
        return result

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

    def compressSU(self):
        # subsample blocks to one 8x8 block
        subsampledBlock = np.empty( [8, 8], np.float64)
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                uBlock = getU(block.tolist())
                uBlock = self.subsample(uBlock)
                subsampledBlock[x*4:x*4+4,y*4:y*4+4] = uBlock
        uDCT = dct(subsampledBlock, False)
        # Quantisierung
        # ...
        # RLE
        # ...
        self.compressedU = uDCT

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

    def compressSV(self):
        # subsample blocks to one 8x8 block
        subsampledBlock = np.empty( [8, 8], np.float64)
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                vBlock = getV(block.tolist())
                vBlock = self.subsample(vBlock)
                subsampledBlock[x*4:x*4+4,y*4:y*4+4] = vBlock
        vDCT = dct(subsampledBlock, False)
        # Quantisierung
        # ...
        # RLE
        # ...
        self.compressedV = vDCT

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

    def uncompressSU(self):
        if self.compressedU[0]:
            subsampledBlock = self.compressedU
            # DeRLE
            # DeQuantisierung
            subsampledBlock = idct(subsampledBlock, False)
            # upsample previously subsampled block
            uBlock = self.upsample(subsampledBlock)
            for x, vblocks in enumerate(self.uncompressed):
                for y, block in enumerate(vblocks):
                    # get block again
                    block = uBlock[x*8:x*8+8,y*8:y*8+8]
                    self.uncompressed[x][y] = setU(self.uncompressed[x][y], block)
        else:
            raise Exception("No compressed data there")

    def uncompressSV(self):
        if self.compressedU[0]:
            subsampledBlock = self.compressedV
            # DeRLE
            # DeQuantisierung
            subsampledBlock = idct(subsampledBlock, False)
            # upsample previously subsampled block
            vBlock = self.upsample(subsampledBlock)
            for x, vblocks in enumerate(self.uncompressed):
                for y, block in enumerate(vblocks):
                    # get block again
                    block = vBlock[x*8:x*8+8,y*8:y*8+8]
                    self.uncompressed[x][y] = setV(self.uncompressed[x][y], block)
        else:
            raise Exception("No compressed data there")

