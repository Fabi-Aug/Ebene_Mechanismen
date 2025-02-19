from dot_class import dot
from math import cos, sin
from typing import Tuple

class swivel(dot):
    """
    A class that represents a swivel point (singleton).
    """
    def __init__(self, x_m: float, y_m: float, r: float, phi: float, id: str):
        if not hasattr(self, "_initialized"):
            super().__init__(x_m + r*cos(phi), y_m + r*sin(phi), id)
            self.x_m = x_m
            self.y_m = y_m
            self._r = r
            self._phi = phi
            self._initialized = True

    def set_phi(self, phi: float):
        self._phi = phi
        self._x = self.x_m + self._r * cos(self._phi)
        self._y = self.y_m + self._r * sin(self._phi)

    def to_dict(self):
        return {
            "x_m": self.x_m,
            "y_m": self.y_m,
            "r": self._r,
            "phi": self._phi,
            "id": self.id
        }

    @classmethod
    def create_instance(cls, **kwargs):
        # Create a new instance (assumes that the list has been cleared beforehand)
        return cls(**kwargs)

    @classmethod
    def overwrite_all_instances(cls, data_list):
        # data_list is a list of dictionaries loaded from the database.
        cls._instances.clear()  # Remove all previous instances
        for data in data_list:
            cls.create_instance(**data)

    @classmethod
    def get_instances(cls):
        """Return all created instances of this class."""
        return cls._instances

    @classmethod
    def clear_instances(cls):
        """Clear all instances of movabledot."""
        cls._instances.clear()