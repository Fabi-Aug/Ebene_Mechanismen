from typing import Tuple
from dot_class import dot


class movabledot(dot):

    def __init__(self, x, y):
        super().__init__(x, y)
        
    def to_dict(self):
        return {
            #"__class__": self.__class__.__name__,
            "x": self._x,
            "y": self._y
            }

    @classmethod
    def create_instance(cls, **kwargs):
        # Einfaches Erstellen eines neuen Objekts (ohne Suche), weil die Liste zuvor geleert wurde.
        return cls(**kwargs)

    @classmethod
    def overwrite_all_instances(cls, data_list):
        # data_list ist eine Liste von Dictionaries, die aus der Datenbank geladen wurden.
        cls._instances.clear()  # Alle bisherigen Instanzen entfernen
        for data in data_list:
            cls.create_instance(**data)


    @classmethod
    def get_instances(cls):
        """Gibt alle erstellten Instanzen der Klasse zurück."""
        return cls._instances