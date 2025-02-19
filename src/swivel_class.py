from dot_class import dot
from math import cos, sin
from typing import Tuple
from singleton import singleton

@singleton
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
        instance = cls.get_instance()
        if instance is None:
            instance = cls(**kwargs)
            cls._instance = instance
        else:
            instance.__dict__.update(kwargs)
        return instance

    @classmethod
    def overwrite_all_instances(cls, data_list):
        """
        For a singleton, update the instance with the first record from the database.
        """
        cls._instance = None
        cls.clear_instances()
        if data_list:
            data = data_list[0]  # Expect only one swivel record
            return cls.create_instance(**data)
        return None

    @classmethod
    def clear_instances(cls):
        super().clear_instances()
        cls._instance = None
        if hasattr(cls, "_initialized"):
            del cls._initialized

    def __str__(self):
        return f"Swivel({self._x}, {self._y}, r={self._r}, phi={self._phi}, id={self.id})"

    def __repr__(self):
        return self.__str__()
