from dot_class import dot
from typing import Tuple
from singleton import singleton


@singleton
class fixeddot(dot):
    """
    A class that represents a fixed point in a 2D plane. It inherits from the dot class.
    """

    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def set_coordinates(self, x, y):
        pass

    def __str__(self):
        return f"({self._x}, {self._y})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    d = fixeddot(1, 2)
    e = fixeddot(3, 4)
    print(d)
    print(e)
