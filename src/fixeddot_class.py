from dot_class import dot
from typing import Tuple


class fixeddot(dot):
    """
    A class that represents a fixed point (singleton).
    """

    def __init__(self, x: float, y: float, id: str):
        """Initialize a fixed point at (x, y) with a unique id."""
        super().__init__(x, y, id)

    def to_dict(self) -> dict:
        """Return a dictionary representation of the fixed point."""
        return {"x": self._x, "y": self._y, "id": self.id}

    @classmethod
    def create_instance(cls, **kwargs) -> "fixeddot":
        """Create a new instance of fixeddot."""
        return cls(**kwargs)

    @classmethod
    def overwrite_all_instances(cls, data_list):
        """Overwrite all instances of fixeddot with the data in data_list."""
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
        return f"Fixed Point at ({self._x}, {self._y}) with id = {self.id}"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":

    f1 = fixeddot(0, 0, "f1")
    f2 = fixeddot(1, 1, "f2")
    print(f1)
    print(f2)
    print(f1.to_dict())
    print(f2.to_dict())
    print(fixeddot.get_instances())
    fixeddot.clear_instances()
    print(fixeddot.get_instances())
