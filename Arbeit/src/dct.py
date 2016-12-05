import math

# Testvectors

# https://vsr.informatik.tu-chemnitz.de/~jan/MPEG/HTML/mpeg_tech.html
a = [[120, 108, 90, 75, 69, 73, 82, 89],
     [127, 115, 97, 81, 75, 79, 88, 95],
     [134, 122, 105, 89, 83, 87, 96, 103],
     [137, 125, 107, 92, 86, 90, 99, 106],
     [131, 119, 101, 86, 80, 83, 93, 100],
     [117, 105, 87, 72, 65, 69, 78, 85],
     [100, 88, 70, 55, 49, 53, 62, 69],
     [89, 77, 59, 44, 38, 42, 51, 58]]

# ???
b = [[140, 124, 124, 132, 130, 139, 102, 88],
     [140, 123, 126, 132, 134, 134, 88, 117],
     [143, 126, 126, 133, 134, 138, 81, 82],
     [148, 126, 128, 136, 137, 134, 79, 130],
     [147, 128, 126, 137, 138, 145, 132, 144],
     [147, 131, 123, 138, 137, 140, 145, 137],
     [142, 135, 122, 137, 140, 138, 143, 112],
     [140, 138, 125, 137, 140, 140, 148, 143]]

# http://keyj.emphy.de/files/projects/videocomp.pdf
c = [[139,144,149,153,155,155,155,155],
     [144,151,153,156,159,156,156,155],
     [150,155,160,163,158,156,156,156],
     [159,161,162,160,160,159,159,159],
     [159,160,161,161,160,155,155,155],
     [161,161,161,161,160,157,157,157],
     [162,162,161,163,162,157,157,157],
     [162,162,161,161,163,158,158,158]]


def dct(f, toint=True):
    """ Do a dct on a given 8x8 array
    :param f: 8x8 array to perform the dct on
    :param toint: round resulting values to integers
    :return: 8x8 array of dct coefficients
    """
    # initialize resulting DCT array
    F = [8*[0], 8*[0], 8*[0], 8*[0], 8*[0], 8*[0], 8*[0], 8*[0]]
    # Go through f and calculate DC/AC for each value
    for u in range(0, 8):
        for v in range(0, 8):
            if u == 0:
                cu = 1/math.sqrt(2)
            else:  # u > 0:
                cu = 1
            if v == 0:
                cv = 1/math.sqrt(2)
            else:  # v > 0:
                cv = 1

            sum = 0
            for x in range(0, 8):
                for y in range(0, 8):
                    sum += f[x][y] * math.cos((((2 * x) + 1) * u * math.pi ) / 16) * math.cos((((2 * y) + 1) * v * math.pi) / 16)
            # save the AC/DC to the corresponding cell in output array
            if toint:
                F[u][v] = round((cu * cv * sum) / 4)
            else:
                F[u][v] = (cu * cv * sum) / 4
    return F


def idct(F, toint=True):
    """ Do an inverse dct on a given 8x8 array
    :param f: 8x8 array to perform the idct on
    :param toint: round resulting values to integers
    :return: 8x8 array of values
    """
    # initialize resulting DCT array
    f = [8*[0], 8*[0], 8*[0], 8*[0], 8*[0], 8*[0], 8*[0], 8*[0]]
    # Go through f and calculate DC/AC for each value
    for x in range(0, 8):
        for y in range(0, 8):

            sum = 0
            for u in range(0, 8):
                for v in range(0, 8):
                    if u == 0:
                        cu = 1/math.sqrt(2)
                    else:  # u > 0:
                        cu = 1
                    if v == 0:
                        cv = 1/math.sqrt(2)
                    else:  # v > 0:
                        cv = 1

                    sum += (cu/2) * (cv/2) * F[u][v] * math.cos((((2 * x) + 1) * u * math.pi ) / 16) * math.cos((((2 * y) + 1) * v * math.pi) / 16)
            # save the AC/DC to the corresponding cell in output array
            if toint:
                f[x][y] = round(sum)
            else:
                f[x][y] = sum
    return f
