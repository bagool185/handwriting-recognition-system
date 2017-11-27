class InvalidImageSize(Exception):
    """ Exception to be raised when the entered image size is invalid. """
    pass


class InvalidK(Exception):
    """ Exception to be raised when k is out of the recommended range
        1 <= k <= 15, or if it is not an integer
     """
    pass


class InvalidN(Exception):
    """ Exception to be raised when n is out of the boundaries
        1 <= n <= 10000
    """
    pass