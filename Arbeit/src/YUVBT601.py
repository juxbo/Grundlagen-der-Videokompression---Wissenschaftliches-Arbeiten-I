def RGB2YUV(RGB):
    """ Convert a RGB value to its YUV representation
    :param RGB: tuple of (r, g, b)
    :return: tuple of (y, u, v)
    """
    r, g, b = RGB
    Y = 0.299 * r + 0.587 * g + 0.144 * b
    U = (b - Y) * 0.493
    V = (r - Y) * 0.877
    return (Y, U, V)


def YUV2RGB(YUV):
    """ Convert a YUV value its to RGB representation
    :param RGB: tuple of (y, u, v)
    :return: tuple of (r, g, b)
    """
    Y, U, V = YUV
    b = Y + (U/0.493)
    r = Y + (V/0.877)
    g = 1.704 * Y - 0.509 * r - 0.194 * b
    return (r, g, b)
