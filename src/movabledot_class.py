from typing import Tuple
from dot_class import dot


class movabledot(dot):

    def __init__(self, x, y):
        super().__init__(x, y)
        

    @classmethod
    def get_instances(cls):
        """Gibt alle erstellten Instanzen der Klasse zurück."""
        return cls._instances