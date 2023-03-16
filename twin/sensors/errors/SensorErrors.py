class RGBValueSizeError(Exception):
    """Raised when shape of RGB array is incorrect"""

    def __init__(self, shape, typ):
        self.message = f"Shape of input RGB + intensity array must be a 1 x 4 numpy array\n Current shape is {shape} with type {typ}"
