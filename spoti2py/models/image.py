class Image:
    """Image model"""

    def __init__(self, height, url, width):
        self.height = height
        self.url = url
        self.width = width

    def __str__(self) -> str:
        return f"{self.height} x {self.width}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.height} x {self.width})"
