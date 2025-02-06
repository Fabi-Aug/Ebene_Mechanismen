from typing import Tuple


class dot:
    """
    A class that represents a point in a 2D plane."""

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def set_coordinates(self, x: float, y: float):
        self._x = x
        self._y = y

    def get_coordinates(self) -> Tuple[float, float]:
        return (self._x, self._y)
    
    def __str__(self):
        return f"({self._x}, {self._y})"
    
    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    d = dot(1, 2)
    print(d)
