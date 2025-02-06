from dot_class import dot
from typing import Tuple
from singleton import singleton


@singleton
class fixeddot(dot):
    """
    A class that represents a fixed point in a 2D plane. It inherits from the dot class.
    """

    _instances = None

    def __init__(self, x: float, y: float):
        if not fixeddot._instance:
            super().__init__(x, y)
            fixeddot._instances = self

    def set_coordinates(self, x, y):
        pass

    @classmethod
    def get_instance(cls):
        """Gibt die einzige Instanz der Klasse zurück."""
        return cls._instances

    def __str__(self):
        return f"({self._x}, {self._y})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    d = fixeddot(1, 2)
    e = fixeddot(3, 4)
    print(d)
    print(e)
    print(fixeddot.get_instance())