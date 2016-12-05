from chroma import getY, setY, getU, setU, getV, setV
from dct import dct, idct
import entropycoder as ec
import numpy as np
import quantization


class Macroblock:
    """ Class that defines a macroblock """
    def __init__(self, macro):
        """ :param macro: 16x16 array that is stored
                          in this macroblock"""
        self.macro = macro
        self.blocks = [[[], []], [[], []]]
        self.extract_blocks(macro)
        self.compressedY = [[[], []], [[], []]]
        self.compressedU = [[[], []], [[], []]]
        self.compressedV = [[[], []], [[], []]]
        # initialize uncompressed, better might be just the generation
        # of the structure
        self.uncompressed = np.empty([2, 2, 8, 8, 3], np.float64)
        self.mquant = None

    def extract_blocks(self, macro):
        """ extracts 8x8 blocks from a 16x16 array
        and applies them to blocks member
        :param macro: 16x16 array that represents the
                      macroblock"""
        for a in range(0, 2):
            for b in range(0, 2):
                # extract all 8x8 blocks of this macroblock
                mula = a*8
                mulb = b*8
                block = macro[mula:mula+8, mulb:mulb+8]
                self.blocks[a][b] = block

    def get(self, x, y):
        """ returns the corresponding 8x8 block
        :param x: X coordinate in this macroblock
        :param y: Y coordinate in this macroblock
        """
        return self.blocks[x][y]

    def subsample(self, block):
        """ perform chroma subsampling
        :param block: 8x8 array of values
        :returns: 4x4 array of values
        """
        result = np.empty([4, 4], np.float64)
        block = np.array(block)
        for x in range(0, 4):
            for y in range(0, 4):
                xmul = x*2
                ymul = y*2
                result[x][y] = np.average(block[xmul:xmul+2, ymul:ymul+2])
        return result

    def upsample(self, block):
        """ reverse chroma subsampling
        :param block: 8x8 array of values
        :return: 16x16 array of values
        """
        result = np.empty([16, 16], np.float64)
        for x in range(0, 8):
            for y in range(0, 8):
                xmul = x*2
                ymul = y*2
                result[xmul:xmul+2, ymul:ymul+2].fill(block[x][y])
        return result

    def size(self):
        """ Get size of this macroblock
        :return: integer
        """
        size = 0
        
        for j in (self.compressedU, self.compressedV, self.compressedY):
            flatlist = np.array(j).flatten()
            for b in flatlist:
                if isinstance(b, list):
                    for r in b:
                        size += r.length()
                else:
                    size += b.length()
        return size

    def getUncompressed(self):
        """ Get uncompressed macroblock
        :return: 16x16 array of tuples (Y, U, V)
        """
        macroblock = np.empty([16, 16, 3])
        macroblock[0:8, 0:8] = self.uncompressed[0][0]
        macroblock[0:8, 8:16] = self.uncompressed[0][1]
        macroblock[8:16, 0:8] = self.uncompressed[1][0]
        macroblock[8:16, 8:16] = self.uncompressed[1][1]
        return macroblock

    def setMQuant(self, mquant):
        """ Set quantization factor
        :param mquant: quantization factor in range from 1-31
        """
        if mquant > 31 or mquant <= 0:
            raise Exception("MQuant needs to be in range of 1-31")
        else:
            self.mquant = mquant

    def compress(self, do_subsample=True, quantize=True, mquant=1):
        """ compress this macroblock
        :param do_subsample: whether to do chroma subsampling
        :param mquant: specify mquant value
        :quantize: whether or not to quantize dct values
        """
        if quantize:
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
        """ compress this macroblock
        :param was_subsampled: if block was subsampled
        :param was_quantized: if block was quantized
        """
        if was_subsampled:
            self.uncompressY(was_quantized)
            self.uncompressSU(was_quantized)
            self.uncompressSV(was_quantized)
        else:
            self.uncompressY(was_quantized)
            self.uncompressU(was_quantized)
            self.uncompressV(was_quantized)

    def compressY(self, quantize=True):
        """ Compress Y values
        :param quantize: whether to quantize this block or not
        """
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                yBlock = getY(block.tolist())
                # DCT
                yDCT = dct(yBlock, True)
                # Quantisierung
                if quantize and self.mquant is not None:
                    yDCT = quantization.quantize(yDCT, quantization.intracoding, self.mquant)
                # RLE
                yDCT = ec.encode(yDCT)
                # ...
                self.compressedY[x][y] = yDCT

    def compressSU(self, quantize=True):
        """ Compress U values with subsampling
        :param quantize: whether to quantize this block or not
        """
        # subsample blocks to one 8x8 block
        subsampledBlock = np.empty( [8, 8], np.float64)
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                uBlock = getU(block.tolist())
                uBlock = self.subsample(uBlock)
                subsampledBlock[x*4:x*4+4, y*4:y*4+4] = uBlock
        uDCT = dct(subsampledBlock, True)
        # Quantisierung
        if quantize and self.mquant is not None:
            uDCT = quantization.quantize(uDCT, quantization.intracoding, self.mquant)
        # ...
        # RLE
        uDCT = ec.encode(uDCT)
        # ...
        self.compressedU = uDCT

    def compressU(self, quantize=True):
        """ Compress U values without subsampling
        :param quantize: whether to quantize this block or not
        """
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                uBlock = getU(block.tolist())
                uDCT = dct(uBlock, True)
                # Quantisierung
                if quantize and self.mquant is not None:
                    uDCT = quantization.quantize(uDCT, quantization.intracoding, self.mquant)
                # ...
                # RLE
                uDCT = ec.encode(uDCT)
                # ...
                self.compressedU[x][y] = uDCT

    def compressV(self, quantize=True):
        """ Compress V values without subsampling
        :param quantize: whether to quantize this block or not
        """
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                vBlock = getV(block.tolist())
                vDCT = dct(vBlock, True)
                # Quantisierung
                if quantize and self.mquant is not None:
                    vDCT = quantization.quantize(vDCT, quantization.intracoding, self.mquant)
                # ...
                # RLE
                vDCT = ec.encode(vDCT)
                # ...
                self.compressedV[x][y] = vDCT

    def compressSV(self, quantize=True):
        """ Compress V values with subsampling
        :param quantize: whether to quantize this block or not
        """
        # subsample blocks to one 8x8 block
        subsampledBlock = np.empty( [8, 8], np.float64)
        for x, vblocks in enumerate(self.blocks):
            for y, block in enumerate(vblocks):
                vBlock = getV(block.tolist())
                vBlock = self.subsample(vBlock)
                subsampledBlock[x*4:x*4+4, y*4:y*4+4] = vBlock
        vDCT = dct(subsampledBlock, True)
        # Quantisierung
        if quantize and self.mquant is not None:
            vDCT = quantization.quantize(vDCT, quantization.intracoding, self.mquant)
        # ...
        # RLE
        vDCT = ec.encode(vDCT)
        # ...
        self.compressedV = vDCT

    def uncompressY(self, dequantize=True):
        """ Uncompress Y values
        :param dequantize: whether to dequantize this block or not
        """
        if self.compressedY[0]:
            for x, vblocks in enumerate(self.compressedY):
                for y, block in enumerate(vblocks):
                    yBlock = block
                    # DeRLE
                    yBlock = ec.decode(yBlock)
                    # DeQuantisierung
                    if dequantize and self.mquant is not None:
                        yBlock = quantization.dequantize(yBlock, quantization.intracoding, self.mquant)
                    yBlock = idct(yBlock, True)
                    self.uncompressed[x][y] = setY(self.uncompressed[x][y], yBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressU(self, dequantize=True):
        """ Uncompress U values without upsampling
        :param dequantize: whether to dequantize this block or not
        """
        if self.compressedU[0][0]:
            for x, vblocks in enumerate(self.compressedU):
                for y, block in enumerate(vblocks):
                    uBlock = block
                    # DeRLE
                    uBlock = ec.decode(uBlock)
                    # DeQuantization
                    if dequantize and self.mquant is not None:
                        uBlock = quantization.dequantize(uBlock, quantization.intracoding, self.mquant)
                    # inverse dct
                    uBlock = idct(uBlock, True)
                    self.uncompressed[x][y] = setU(self.uncompressed[x][y], uBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressV(self, dequantize=True):
        """ Uncompress V values without upsampling
        :param dequantize: whether to dequantize this block or not
        """
        if self.compressedV[0][0]:
            for x, vblocks in enumerate(self.compressedV):
                for y, block in enumerate(vblocks):
                    vBlock = block
                    # DeRLE
                    vBlock = ec.decode(vBlock)
                    # DeQuantisierung
                    if dequantize and self.mquant is not None:
                        vBlock = quantization.dequantize(vBlock, quantization.intracoding, self.mquant)
                    vBlock = idct(vBlock, True)
                    self.uncompressed[x][y] = setV(self.uncompressed[x][y], vBlock)
        else:
            raise Exception("No compressed data there")

    def uncompressSU(self, dequantize=True):
        """ Uncompress U values with upsampling
        :param dequantize: whether to dequantize this block or not
        """
        subsampledBlock = self.compressedU
        # DeRLE
        subsampledBlock = ec.decode(subsampledBlock)
        # DeQuantisierung
        if dequantize and self.mquant is not None:
            subsampledBlock = quantization.dequantize(subsampledBlock, quantization.intracoding, self.mquant)
        # Inverse DCT
        subsampledBlock = idct(subsampledBlock, True)
        # upsample previously subsampled block
        uBlock = self.upsample(subsampledBlock)
        for x, vblocks in enumerate(self.uncompressed):
            for y, block in enumerate(vblocks):
                # get block again
                block = uBlock[x*8:x*8+8, y*8:y*8+8]
                self.uncompressed[x][y] = setU(self.uncompressed[x][y], block)

    def uncompressSV(self, dequantize=True):
        """ Uncompress V values with upsampling
        :param dequantize: whether to dequantize this block or not
        """
        subsampledBlock = self.compressedV
        # DeRLE
        subsampledBlock = ec.decode(subsampledBlock)
        # DeQuantisierung
        if dequantize and self.mquant is not None:
            subsampledBlock = quantization.dequantize(subsampledBlock, quantization.intracoding, self.mquant)
        # Inverse DCT
        subsampledBlock = idct(subsampledBlock, True)
        # upsample previously subsampled block
        vBlock = self.upsample(subsampledBlock)
        for x, vblocks in enumerate(self.uncompressed):
            for y, block in enumerate(vblocks):
                # get block again
                block = vBlock[x*8:x*8+8, y*8:y*8+8]
                self.uncompressed[x][y] = setV(self.uncompressed[x][y], block)
