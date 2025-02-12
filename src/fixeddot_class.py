from dot_class import dot
from typing import Tuple
from singleton import singleton


@singleton
class fixeddot(dot):
    """
    A class that represents a fixed point in a 2D plane. It inherits from the dot class.
    """

    def __init__(self, x: float, y: float, id: str):
        # Initialisierung nur einmal durchführen
        if not hasattr(self, "_initialized"):
            super().__init__(x, y, id)
            self._initialized = True

    def set_coordinates(self, x, y):
        pass
    
    def to_dict(self):
        return {
            #"__class__": self.__class__.__name__,
            "x": self._x,
            "y": self._y,
            "id": self.id
            }
    
    @classmethod
    def create_instance(cls, **kwargs):
        instance = cls.get_instance()  # Annahme: get_instance() liefert die existierende Instanz oder None
        if instance is None:
            # Falls noch keine Instanz existiert, wird eine neue erstellt
            instance = cls(**kwargs)
            cls._instance = instance
        else:
            # Falls bereits eine Instanz existiert, aktualisieren wir ihre Attribute.
            # Hinweis: Falls du spezielle Logik (z.B. set_coordinates) hast, kannst du diese hier nutzen.
            instance.__dict__.update(kwargs)
        return instance


    def __str__(self):
        return f"({self._x}, {self._y})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    d = fixeddot(1, 2, "d")
    e = fixeddot(3, 4, "e")
    print("d:", d)
    print("e:", e)
    print("fixeddot.get_instance():", fixeddot.get_instance())
