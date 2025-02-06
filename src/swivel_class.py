from dot_class import dot
from math import cos, sin
from typing import Tuple
from singleton import singleton


@singleton
class swivel(dot):
    """
    A class that represents a swivel point in a 2D plane. It inherits from the dot class. Phi is the current angle in rad of the swivel point.
    """

    def __init__(self, x: float, y: float, r: float, phi: float):
        super().__init__(x, y)
        self._r = r
        self._phi = phi

    def set_phi(self, phi: float):
        self._phi = phi

    def get_phi(self) -> float:
        return self._phi

    def get_circlepoint(self) -> Tuple[float, float]:
        return (self._x + self._r * cos(self._phi), self._y + self._r * sin(self._phi))

    def set_coordinates(self, x, y):
        pass

    @classmethod
    def get_instances(cls):
        """Gibt alle erstellten Instanzen der Klasse zurück."""
        return cls.self

    def __str__(self):
        return f"({self._x}, {self._y}, {self._r}, {self._phi})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    s = swivel(1, 2, 3, 4)
    print(s)
    print(s.get_phi())
    s.set_phi(0)
    print(s.get_phi())
    print(s)
    print(s.get_circlepoint())
