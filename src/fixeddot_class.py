from dot_class import dot
from typing import Tuple


class fixeddot(dot):
    """
    A class that represents a fixed point (singleton).
    """
    def __init__(self, x: float, y: float, id: str):
        #if not hasattr(self, "_initialized"):
            super().__init__(x, y, id)
            #self._initialized = True

    def to_dict(self):
        return {
            "x": self._x,
            "y": self._y,
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

    def __str__(self):
        return f"Fixed Point at ({self._x}, {self._y}) with id = {self.id}"

    def __repr__(self):
        return self.__str__()
