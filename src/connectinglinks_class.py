from dot_class import dot
from fixeddot_class import fixeddot
from movabledot_class import movabledot

class connectionlinks:
    """Class to represent a connection between two dots."""
    _instances = []

    def __init__(self, dot1: dot, dot2: dot):
        """Initializes a connection between two dots."""
        self.dot1 = dot1
        self.dot2 = dot2
        self.__class__._instances.append(self)

    def calc_length(self) -> float:
        """Calculates the length of the connection."""
        x1, y1 = self.dot1.get_coordinates()
        x2, y2 = self.dot2.get_coordinates()
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    @classmethod
    def get_instances(cls):
        """Returns all instances of connectionlinks."""
        return cls._instances

    @classmethod
    def create_instance(cls, dot1: dot, dot2: dot):
        """Creates a new instance of connectionlinks."""
        return cls(dot1, dot2)

    @classmethod
    def overwrite_all_instances(cls, data_list, dot_instances):
        """Overwrites all instances of connectionlinks with the given data."""
        cls._instances.clear()
        for data in data_list:
            # Get the dot instances
            dot1 = cls.get_dot_by_id(data["dot1"]["id"], dot_instances)
            dot2 = cls.get_dot_by_id(data["dot2"]["id"], dot_instances)
            if dot1 and dot2:
                cls.create_instance(dot1, dot2)

    @classmethod
    def get_dot_by_id(cls, dot_id, dot_instances):
        """Returns the dot with the given ID."""
        return dot_instances.get(dot_id)

    @classmethod
    def clear_instances(cls):
        """Clears all instances of connectionlinks"""
        cls._instances.clear()

    def to_dict(self):
        """Returns the connection as a dictionary."""
        return {
            "dot1": self.dot1.to_dict(),
            "dot2": self.dot2.to_dict()
        }

    def __str__(self):
        return f"Link between ({self.dot1} and {self.dot2})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    d0 = fixeddot(0, 0, "F0")
    c = connectionlinks(d0, d0)
    print("connectionlinks:", connectionlinks.get_instances())
    connectionlinks.clear_instances()
    print("After clearing:", connectionlinks.get_instances())
