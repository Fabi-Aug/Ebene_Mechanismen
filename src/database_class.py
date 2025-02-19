from tinydb import TinyDB, Query
from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
import math
import os

class Database:
    def __init__(self, db_path="mechanism.json"):
        full_path = os.path.join("src", db_path)  # "src\" wird automatisch hinzugefügt
        self.db = TinyDB(full_path)

    @classmethod
    def save_mechanism(cls, path="mechanism.json"):
        """Speichert einen Mechanismus in der Datenbank, jeweils in einer eigenen Tabelle pro Klasse."""
        full_path = os.path.join("src", path)  # "src\" wird automatisch hinzugefügt
        cls.db = TinyDB(full_path)
        # Fixeddot speichern in eigener Tabelle "fixeddot"
        cls.db.table("fixeddot").insert(fixeddot.get_instance().to_dict())
        
        # Movabledots speichern in eigener Tabelle "movabledot"
        movabledot_table = cls.db.table("movabledot")
        for movingdot in movabledot.get_instances():
            movabledot_table.insert(movingdot.to_dict())
        
        # Swivel speichern in eigener Tabelle "swivel"
        cls.db.table("swivel").insert(swivel.get_instance().to_dict())
        
        # ConnectionLinks speichern in eigener Tabelle "connectionlinks"
        connectionlinks_table = cls.db.table("connectionlinks")
        for connection in connectionlinks.get_instances():
            connectionlinks_table.insert(connection.to_dict())

    @classmethod
    def load_mechanism(self,path="mechanism.json"):
        """
        Lädt einen Mechanismus und überschreibt alle Objekte für Klassen, die den Bulk-Update-Mechanismus unterstützen.
        """
        full_path = os.path.join("src", path)  # "src\" wird automatisch hinzugefügt
        self.db = TinyDB(full_path)
        class_map={
                "fixeddot": fixeddot,
                "movabledot": movabledot,
                "swivel": swivel,
                "connectionlinks": connectionlinks
            }
        for class_name, cls in class_map.items():
            table = self.db.table(class_name)
            data = table.all()
            # Falls die Klasse den Bulk-Update-Mechanismus unterstützt, benutze diesen:
            if hasattr(cls, "overwrite_all_instances"):
                cls.overwrite_all_instances(data)
            else:
                # Für Singleton-Klassen oder ähnliche Fälle:
                for item in data:
                    cls.create_instance(**item)


if __name__ == "__main__":
    #Beispielobjekte erstellen
    #d0 = fixeddot(0, 0, "d0")
    #d1 = movabledot(10, 35, "d1")
    #d2 = movabledot(5, 10, "d2")
    #s1 = swivel(-30, 0, (5**2 + 10**2)**0.5, math.atan(10/5), "s1")
    #c1 = connectionlinks(d0, d1)
    #c2 = connectionlinks(d1, d2)
    #c3 = connectionlinks(d2, s1)
    #c4 = connectionlinks(d2, d0)
    #
    #
    #Database.save_mechanism("mechanism.json")

    Database.load_mechanism("strandbeest.json")
    print(swivel.get_instances())
    print(fixeddot.get_instances())
    print(movabledot.get_instances())
    print(connectionlinks.get_instances())
    

