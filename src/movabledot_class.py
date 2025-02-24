from typing import Tuple
from dot_class import dot


class movabledot(dot):

    def __init__(self, x, y, id):
        """Initialize a new movable dot at position (x, y) with a unique id."""
        super().__init__(x, y, id)

    def to_dict(self) -> dict:
        """Return a dictionary representation of the movable dot."""
        return {"x": self._x, "y": self._y, "id": self.id}

    @classmethod
    def create_instance(cls, **kwargs) -> "movabledot":
        """Create a new instance of the class."""
        return cls(**kwargs)

    @classmethod
    def overwrite_all_instances(cls, data_list):
        """Overwrite all instances of the class with the data in data"""
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
        return f"Movable Point at ({self._x:.2f}, {self._y:.2f}) with id = {self.id})"


if __name__ == "__main__":
    
    m = movabledot(1, 2, 1)
    print(m)
    print(m.to_dict())
    print(m.get_instances())
    m.clear_instances()
    print(m.get_instances())
