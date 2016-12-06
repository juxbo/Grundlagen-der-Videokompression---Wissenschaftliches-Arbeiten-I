def dct(f):
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
            # save result in F
            F[u][v] = round((cu * cv * sum) / 4)
    return F
