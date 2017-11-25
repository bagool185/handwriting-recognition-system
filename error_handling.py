class InvalidImageSize(Exception):
    """ Exception to be raised when the entered image size is invalid. """
    pass


class InvalidK(Exception):
    """ Exception to be raised when k is out of the recommended range
        1 <= k <= 15
     """
    pass

