from dot_class import dot
from typing import Tuple
from singleton import singleton

@singleton
class fixeddot(dot):
    """
    A class that represents a fixed point (singleton).
    """
    def __init__(self, x: float, y: float, id: str):
        if not hasattr(self, "_initialized"):
            super().__init__(x, y, id)
            self._initialized = True

    def to_dict(self):
        return {
            "x": self._x,
            "y": self._y,
            "id": self.id
        }
    
    @classmethod
    def create_instance(cls, **kwargs):
        instance = cls.get_instance()  # Using the singleton getter
        if instance is None:
            instance = cls(**kwargs)
            cls._instance = instance
        else:
            # Update existing instance
            instance.__dict__.update(kwargs)
        return instance

    @classmethod
    def overwrite_all_instances(cls, data_list):
        """
        For a singleton, we assume there's only one record.
        Clear any existing instance and create a new one with the data.
        """
        cls._instance = None  # Reset the singleton
        cls.clear_instances()  # Clear the base _instances list
        if data_list:
            data = data_list[0]  # Expect only one fixed dot record
            return cls.create_instance(**data)
        return None

    @classmethod
    def clear_instances(cls):
        super().clear_instances()
        cls._instance = None
        if hasattr(cls, "_initialized"):
            del cls._initialized

    def __str__(self):
        return f"Fixed({self._x}, {self._y}, id={self.id})"

    def __repr__(self):
        return self.__str__()
