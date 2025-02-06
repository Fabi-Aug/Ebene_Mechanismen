from dot_class import dot
from math import cos, sin
from typing import Tuple
from singleton import singleton

@singleton
class swivel(dot):
    """
    A class that represents a swivel point in a 2D plane. It inherits from the dot class.
    Phi is the current angle in rad of the swivel point.
    """
    def __init__(self, x_m: float, y_m: float, r: float, phi: float):
        # Da der Singleton-Dekorator __init__ mehrmals aufrufen kann,
        # initialisieren wir nur beim allerersten Aufruf.
        if not hasattr(self, '_initialized'):
            super().__init__(x_m + r * cos(phi), y_m + r * sin(phi))
            self._r = r
            self._phi = phi
            self._initialized = True

    def set_phi(self, phi: float):
        self._phi = phi

    def get_phi(self) -> float:
        return self._phi

    def get_circlepoint(self) -> Tuple[float, float]:
        return (self._x + self._r * cos(self._phi), self._y + self._r * sin(self._phi))

    def set_coordinates(self, x, y):
        # Diese Methode bleibt leer, da die Koordinaten nicht verändert werden sollen
        pass

    def __str__(self):
        return f"({self._x}, {self._y}, {self._r}, {self._phi})"

    def __repr__(self):
        return self.__str__()


# Testbereich
if __name__ == "__main__":
    s = swivel(1, 2, 3, 4)
    print("s:", s)
    print("phi:", s.get_phi())
    print("Circlepoint:", s.get_circlepoint())
    s.set_phi(0)
    print("phi (nach set_phi):", s.get_phi())
    print("s (nach set_phi):", s)
    print("Circlepoint:", s.get_circlepoint())
