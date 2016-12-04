from chroma import rgb_chroma, getY, chroma_rgb, setY, getU, setU, getV, setV
from copy import deepcopy
from dct import dct, idct
import entropycoder as ec
import quantization
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
        self.mquant=1

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

    def size(self):
        """ returns a count of containing
        elements in compressed form """
        size = 0
        for y in self.compressedY:
            for z in y:
                for i in z:
                    size +=i.length()
        for x in (self.compressedU, self.compressedV):
            for i in x:
                size +=i.length()
        return size

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

    def setMQuant(self, mquant):
        if mquant > 31 or mquant <= 0:
            raise Exception("MQuant needs to be in range of 1-31")
        else:
            self.mquant = mquant

    def compress(self, do_subsample=True, mquant=1, quantize=True):
        self.setMQuant(mquant)
        if do_subsample:
            self.compressY(quantize)
            self.compressSU(quantize)
            self.compressSV(quantize)
        else:
            self.compressY(quantize)
            self.compressU(quantize)
            self.compressV(quantize)

    def uncompress(self, was_subsampled=True, was_quantized=True):
        if was_subsampled:
            self.uncompressY(was_quantized)
            self.uncompressSU(was_quantized)
            self.uncompressSV(was_quantized)
        else:
            self.uncompressY(was_quantized)
            self.uncompressU(was_quantized)
            self.uncompressV(was_quantized)

    def compressY(self, quantize=True):
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                yBlock = getY(block.tolist())
                # DCT
                yDCT = dct(yBlock, False)
                # Quantisierung
                if quantize:
                    yDCT = quantization.quantize(yDCT, quantization.intracoding, self.mquant)
                # RLE
                yDCT = ec.encode(yDCT)
                # ...
                self.compressedY[x][y] = yDCT

    def compressSU(self, quantize=True):
        # subsample blocks to one 8x8 block
        subsampledBlock = np.empty( [8, 8], np.float64)
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                uBlock = getU(block.tolist())
                uBlock = self.subsample(uBlock)
                subsampledBlock[x*4:x*4+4,y*4:y*4+4] = uBlock
        uDCT = dct(subsampledBlock, False)
        # Quantisierung
        if quantize:
            uDCT = quantization.quantize(uDCT, quantization.intracoding, self.mquant)
        # ...
        # RLE
        uDCT = ec.encode(uDCT)
        # ...
        self.compressedU = uDCT

    def compressU(self, quantize=True):
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                uBlock = getU(block.tolist())
                uDCT = dct(uBlock, False)
                # Quantisierung
                if quantize:
                    uDCT = quantization.quantize(uDCT, quantization.intracoding, self.mquant)
                # ...
                # RLE
                uDCT = ec.encode(uDCT)
                # ...
                self.compressedU[x][y] = uDCT

    def compressV(self, quantize=True):
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                vBlock = getV(block.tolist())
                vDCT = dct(vBlock, False)
                # Quantisierung
                if quantize:
                    vDCT = quantization.quantize(vDCT, quantization.intracoding, self.mquant)
                # ...
                # RLE
                vDCT = ec.encode(vDCT)
                # ...
                self.compressedV[x][y] = vDCT

    def compressSV(self, quantize=True):
        # subsample blocks to one 8x8 block
        subsampledBlock = np.empty( [8, 8], np.float64)
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                vBlock = getV(block.tolist())
                vBlock = self.subsample(vBlock)
                subsampledBlock[x*4:x*4+4,y*4:y*4+4] = vBlock
        vDCT = dct(subsampledBlock, False)
        # Quantisierung
        if quantize:
            vDCT = quantization.quantize(vDCT, quantization.intracoding, self.mquant)
        # ...
        # RLE
        vDCT = ec.encode(vDCT)
        # ...
        self.compressedV = vDCT

    def uncompressY(self, dequantize=True):
        if self.compressedY[0]:
            for x, vblocks in enumerate(self.compressedY):
                for y, block in enumerate(vblocks):
                    yBlock = block
                    # DeRLE
                    yBlock = ec.decode(yBlock)
                    # DeQuantisierung
                    if dequantize:
                        yBlock = quantization.dequantize(yBlock, quantization.intracoding, self.mquant)
                    yBlock = idct(yBlock, False)
                    self.uncompressed[x][y] = setY(self.uncompressed[x][y], yBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressU(self, dequantize= True):
        if self.compressedU[0][0]:
            for x, vblocks in enumerate(self.compressedU):
                for y, block in enumerate(vblocks):
                    uBlock = block
                    # DeRLE
                    uBlock  = ec.decode(uBlock)
                    # DeQuantization
                    if dequantize:
                        uBlock = quantization.dequantize(uBlock, quantization.intracoding, self.mquant)
                    # inverse dct
                    uBlock = idct(uBlock, False)
                    self.uncompressed[x][y] = setU(self.uncompressed[x][y], uBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressV(self, dequantize=True):
        if self.compressedV[0][0]:
            for x, vblocks in enumerate(self.compressedV):
                for y, block in enumerate(vblocks):
                    vBlock = block
                    # DeRLE
                    vBlock = ec.decode(vBlock)
                    # DeQuantisierung
                    if dequantize:
                        vBlock = quantization.dequantize(vBlock, quantization.intracoding, self.mquant)
                    vBlock = idct(vBlock, False)
                    self.uncompressed[x][y] = setV(self.uncompressed[x][y], vBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressSU(self, dequantize=True):
        subsampledBlock = self.compressedU
        # DeRLE
        subsampledBlock = ec.decode(subsampledBlock)
        # DeQuantisierung
        subsampledBlock = quantization.dequantize(subsampledBlock, quantization.intracoding, self.mquant)
        # Inverse DCT
        if dequantize:
            subsampledBlock = idct(subsampledBlock, False)
        # upsample previously subsampled block
        uBlock = self.upsample(subsampledBlock)
        for x, vblocks in enumerate(self.uncompressed):
            for y, block in enumerate(vblocks):
                # get block again
                block = uBlock[x*8:x*8+8,y*8:y*8+8]
                self.uncompressed[x][y] = setU(self.uncompressed[x][y], block)

    def uncompressSV(self, dequantize=True):
        subsampledBlock = self.compressedV
        # DeRLE
        subsampledBlock = ec.decode(subsampledBlock)
        # DeQuantisierung
        if dequantize:
            subsampledBlock = quantization.dequantize(subsampledBlock, quantization.intracoding, self.mquant)
        # Inverse DCT
        subsampledBlock = idct(subsampledBlock, False)
        # upsample previously subsampled block
        vBlock = self.upsample(subsampledBlock)
        for x, vblocks in enumerate(self.uncompressed):
            for y, block in enumerate(vblocks):
                # get block again
                block = vBlock[x*8:x*8+8,y*8:y*8+8]
                self.uncompressed[x][y] = setV(self.uncompressed[x][y], block)

