from picb import bild
from chroma import rgb_chroma, chroma_rgb
from macroblock import Macroblock
import scipy.misc
import numpy as np
from examples import example1

def create_img(image):
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
    # don't know why but now we need to correct wrong array
    img = np.rot90(np.fliplr(img))
    return img


def encode(bild, subsample=True):
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
            macroblock.compress(subsample, 1)
            compressedSize += macroblock.size()
            compressedMacroblocks[x][y] = macroblock

    print("Original Size: ", bildInYUV.size)
    print("Compressed Size: ", compressedSize)
    return compressedMacroblocks


def decode(compressedMacroblocks, subsample=True):
    height = len(compressedMacroblocks) * 16
    width = len(compressedMacroblocks[0]) * 16
    uncompressedImage = np.empty([height, width, 3])
    for x, row in enumerate(compressedMacroblocks):
        for y, macroblock in enumerate(row):
            macroblock.uncompress(subsample)
            xmul = x*16
            ymul = y*16
            uncompressedImage[xmul:xmul+16, ymul:ymul+16] = macroblock.getUncompressed()

    uncompressedImage = chroma_rgb(uncompressedImage)
    return uncompressedImage


if __name__ == "__main__":
    # show original image
    bild = scipy.misc.imread('./test_img/brook.jpg')
    # bild = scipy.misc.imread('./test_img/lena_small.jpg')
    # bild = example1()
    img = create_img(bild)
    scipy.misc.imshow(img)
    # do compression and decompression
    compressed = encode(bild)
    uncompressed = decode(compressed)
    # show uncompressed image
    scipy.misc.imshow(create_img(uncompressed))
