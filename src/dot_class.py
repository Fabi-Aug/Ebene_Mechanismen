from typing import Tuple

class dot:
    """
    A base class that represents a point in a 2D plane.
    Each subclass has its own _instances list due to __init_subclass__.
    """
    _instances = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._instances = []  # Each subclass has its own instance list

    def __init__(self, x, y, id):
        self._x = x
        self._y = y
        self.id = id
        self.x_values = []
        self.y_values = []
        # Append to the subclass's _instances list
        self.__class__._instances.append(self)

    def set_coordinates(self, x: float, y: float):
        self._x = x
        self._y = y

    def get_coordinates(self) -> Tuple[float, float]:
        return (float(self._x), float(self._y))
    
    def get_self(self):
        return self

    @classmethod
    def get_instances(cls):
        """Return instances specific to this class (not including subclasses)."""
        return cls._instances

    @classmethod
    def get_all_instances(cls):
        """Return instances of cls and all its subclasses."""
        all_instances = list(cls._instances)
        for subcls in cls.__subclasses__():
            all_instances.extend(subcls.get_all_instances())
        return all_instances

    @classmethod
    def clear_instances(cls):
        """
        Clear the _instances list for this class.
        (Subclasses that store singletons may override this to reset them as well.)
        """
        cls._instances.clear()

    def __str__(self):
        return f"({self._x}, {self._y}, id={self.id})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    # Quick test
    d = dot(1, 2, "d")
    print("Direct dot instances:", dot.get_instances())
    print("All dot instances:", dot.get_all_instances())
    dot.clear_instances()
    print("After clearing:", dot.get_instances())
