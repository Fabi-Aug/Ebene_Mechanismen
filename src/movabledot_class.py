from typing import Tuple
from dot_class import dot

class movabledot(dot):

    def __init__(self, x, y, id):
        super().__init__(x, y, id)
        
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
