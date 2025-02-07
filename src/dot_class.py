from typing import Tuple

class dot:
    """
    A class that represents a point in a 2D plane.
    """
    _instances = []  # Direkt in der Basisklasse definieren

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._instances = []  # Jede Unterklasse bekommt ihr eigenes _instances-Attribut

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.__class__._instances.append(self)

    def set_coordinates(self, x: float, y: float):
        self._x = x
        self._y = y

    def get_coordinates(self) -> Tuple[float, float]:
        return (float(self._x),float(self._y))
    
    def get_self(self):
        return self
    
    @classmethod
    def get_instances(cls):
        """Gibt alle Instanzen der jeweiligen Klasse zurück.
           Bei Unterklassen werden nur deren direkte Instanzen zurückgegeben."""
        return cls._instances

    @classmethod
    def get_all_instances(cls):
        """Gibt alle Instanzen zurück, die entweder von cls oder von einer Unterklasse von cls erstellt wurden."""
        all_instances = list(cls._instances)  # Kopie der direkten Instanzen
        for subcls in cls.__subclasses__():
            # Rekursiv alle Instanzen der Unterklassen hinzufügen
            all_instances.extend(subcls.get_all_instances())
        return all_instances
    
    def __str__(self):
        return f"({self._x}, {self._y})"
    
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    d = dot(1, 2)
    print("Direkte dot Instanzen:", dot.get_instances())
    print("Alle dot Instanzen:", dot.get_all_instances())
