from typing import Tuple


class dot:
    """
    A class that represents a point in a 2D plane."""

    _instances = []

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.__class__._instances.append(self)

    def set_coordinates(self, x: float, y: float):
        self._x = x
        self._y = y

    def get_coordinates(self) -> Tuple[float, float]:
        return (self._x, self._y)
    
    @classmethod
    def get_instances(cls):
        """Gibt alle erstellten Instanzen der Klasse zurück."""
        return cls._instances
    
    def __str__(self):
        return f"({self._x}, {self._y})"
    
    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    d = dot(1, 2)
    print(d)
