from dot_class import dot
from math import cos, sin
from typing import Tuple


class swivel(dot):
    """
    A class that represents a swivel point (singleton).
    """

    def __init__(self, x_m: float, y_m: float, r: float, phi: float, id: str):
        """Create a new Swivel point at (x_m, y_m) with radius r and angle phi."""
        super().__init__(x_m + r * cos(phi), y_m + r * sin(phi), id)
        self.x_m = x_m
        self.y_m = y_m
        self._r = r
        self._phi = phi

    def set_phi(self, phi: float):
        """Set the angle of the swivel point."""
        self._phi = phi
        self._x = self.x_m + self._r * cos(self._phi)
        self._y = self.y_m + self._r * sin(self._phi)

    def to_dict(self) -> dict:
        """Return a dictionary representation of the swivel point."""
        return {
            "x_m": self.x_m,
            "y_m": self.y_m,
            "r": self._r,
            "phi": self._phi,
            "id": self.id,
        }

    @classmethod
    def create_instance(cls, **kwargs) -> "swivel":
        """Create a new instance of the swivel point."""
        return cls(**kwargs)

    @classmethod
    def overwrite_all_instances(cls, data_list):
        """Overwrite all instances of the swivel point with the data in data_list."""
        cls._instances.clear()  # Remove all previous instances
        for data in data_list:
            cls.create_instance(**data)

    @classmethod
    def get_instances(cls) -> list:
        """Return all created instances of this class."""
        return cls._instances

    @classmethod
    def clear_instances(cls):
        """Clear all instances of movabledot."""
        cls._instances.clear()

    def __str__(self):
        return f"Swivel point at ({self.x_m}, {self.y_m}) with radius {self._r}, angle {self._phi:.2f} and id = {self.id}"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    s = swivel(0, 0, 1, 0, "s1")
    print(s)
    s.set_phi(180)
    print(s)
    print(s.to_dict())
    print(swivel.get_instances())
    swivel.clear_instances()
    print(swivel.get_instances())
