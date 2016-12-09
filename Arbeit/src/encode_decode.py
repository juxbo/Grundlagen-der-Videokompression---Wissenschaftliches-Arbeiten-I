from chroma import rgb_chroma, chroma_rgb
from examples import example1
from macroblock import Macroblock
import argparse
from picb import bild
import numpy as np
import scipy.misc


def create_img(image):
    """ Convert 2 dimensional array of rgb tuples
    into an array that is convertable to a picture
    with scipy
    :param image: 2 dimensional array of rgb tuples
    """
    # declare picture size with RGB color
    width = len(image[0])
    height = len(image)
    channels = 3

    # create empty image
    img = np.zeros((width, height, channels), dtype=np.uint8)

    # fill image with picture array values
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            r, g, b = image[x][y][0], image[x][y][1], image[x][y][2]
            img[y][x][0] = r
            img[y][x][1] = g
            img[y][x][2] = b
    return img


def encode(bild, subsample=True, quantize=True, mquant=1):
    """ Encode an image
    :param subsample: whether subsampling should be applied or not
    :param quantize: whether quantization should be applied or not
    :param mquant: set quantization scaling factor
    :return: 2 dimensional array of macroblocks
    """
    # Variable that holds the compressed size at the end
    compressedSize = 0
    # chroma conversion
    bildInYUV = rgb_chroma(bild)

    # load matrix into numpy array for better extraction
    # of blocks and macroblocks
    bildInYUV = np.array(bildInYUV)

    height = len(bild)
    width = len(bild[0])
    compressedMacroblocks = np.empty([int(height/16), int(width/16)]).tolist()

    for x in range(0, int(height/16)):
        for y in range(0, int(width/16)):
            # Extract each Macroblock
            # A macroblock consists of 4 * 8x8 blocks
            xmul = x*16
            ymul = y*16
            thisMacroblock = bildInYUV[xmul:xmul+16, ymul:ymul+16]
            macroblock = Macroblock(thisMacroblock)
            macroblock.compress(subsample, quantize, mquant)
            compressedSize += macroblock.size()
            compressedMacroblocks[x][y] = macroblock

    # For calculation of original size we assumed, that each RGB
    # value is represented as an 8 bit integer
    # For calculation of the compressed size we assumed that each
    # value encoded by RLE needs 9 bits as we have additional overhead
    # from special characters like eob
    print("Original Size: ", ((bildInYUV.size * 8) / 1024) / 8, " Kilobyte")
    print("Compressed Size: ", ((compressedSize * 9) / 1024) / 8, " Kilobyte")
    return compressedMacroblocks


def decode(compressedMacroblocks, upsample=True, dequantize=True):
    """ Decode an encoded image
    :param upsample: whether uplsampling should be applied or not
    :param upsample: whether dequantization should be applied or not
    :return: 2 dimenional array of rgb tuples
    """
    height = len(compressedMacroblocks) * 16
    width = len(compressedMacroblocks[0]) * 16
    uncompressedImage = np.empty([height, width, 3])
    for x, row in enumerate(compressedMacroblocks):
        for y, macroblock in enumerate(row):
            macroblock.uncompress(upsample, dequantize)
            xmul = x*16
            ymul = y*16
            uncompressedImage[xmul:xmul+16, ymul:ymul+16] = macroblock.getUncompressed()

    uncompressedImage = chroma_rgb(uncompressedImage)
    return uncompressedImage


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compress images.')
    parser.add_argument('-s', '--subsample', dest='subsample', action='store_true', help='Enable subsampling')
    parser.add_argument('-q', '--quantize', dest='quantize', action='store_true', help='Enable Quantization')
    parser.add_argument('-m', '--mquant', dest='mquant', type=int, default='1', help='Set quantization scaling factor. Default: 1')
    args = parser.parse_args()

    # Reference Image
    bild = scipy.misc.imread('./test_img/brook.jpg')
    # Image showing chroma subsampling artefacts
    # bild = example1()
    # Mirror and rotate image
    bild = np.rot90(np.fliplr(bild))
    img = create_img(bild)
    # show original image
    scipy.misc.imshow(img)
    # do compression and decompression
    compressed = encode(bild, args.subsample, args.quantize, args.mquant)
    uncompressed = decode(compressed, args.subsample, args.quantize)
    # show uncompressed image
    scipy.misc.imshow(create_img(uncompressed))
