from picb import bild
from chroma import rgb_chroma, getY, chroma_rgb, setY
from macroblock import Macroblock
import scipy.misc
import numpy as np


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
    # chroma conversion
    bildInYUV = rgb_chroma(bild)

    # load matrix into numpy array for better extraction
    # of blocks and macroblocks
    bildInYUV = np.array(bildInYUV)

    height = len(bild)
    width = len(bild[0])
    compressedMacroblocks = np.empty([int(height/16), int(width/16)]).tolist()

    for x in range(0,int(height/16)):
        for y in range(0,int(width/16)):
            # Extract each Macroblock
            # A macroblock consists of 4 * 8x8 blocks
            xmul = x*16
            ymul = y*16
            thisMacroblock = bildInYUV[xmul:xmul+16,ymul:ymul+16]
            macroblock = Macroblock(thisMacroblock)
            macroblock.compress(subsample)
            compressedMacroblocks[x][y] = macroblock

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
            uncompressedImage[xmul:xmul+16,ymul:ymul+16] = macroblock.getUncompressed()
   
    uncompressedImage = chroma_rgb(uncompressedImage)
    return uncompressedImage

    
    # # Inverse dct to get old Y value back
    # afterdct = dct_inverse(dimg)

    # # set Y in original YUV array again
    # afterdct = setY(bildInYUV, afterdct)
    # # convert to RGB again
    # afterdct = chroma_rgb(afterdct)
    # # create image
    # afterdct = create_img(afterdct)
    # # show image
    # scipy.misc.imshow(afterdct)

if __name__ == "__main__":
    # show original image
    bild = scipy.misc.imread('./test_img/lena_square.jpg')
    img = create_img(bild)
    scipy.misc.imshow(img)
    # do compression and decompression
    compressed = encode(bild)
    uncompressed = decode(compressed)
    # show uncompressed image
    scipy.misc.imshow(create_img(uncompressed))
