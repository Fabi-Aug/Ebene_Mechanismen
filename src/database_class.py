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
        os.remove(full_path)
        cls.db = TinyDB(full_path)
        
        # Fixeddot speichern in eigener Tabelle "fixeddot"
        fixed_dot_table = cls.db.table("fixeddot")
        for fixed_dot in fixeddot.get_instances():
            fixed_dot_table.insert(fixed_dot.to_dict())
        
        # Movabledots speichern in eigener Tabelle "movabledot"
        movable_dot_table = cls.db.table("movabledot")
        for movable_dot in movabledot.get_instances():
            movable_dot_table.insert(movable_dot.to_dict())
        
        # Swivel speichern in eigener Tabelle "swivel"
        swivel_table = cls.db.table("swivel")
        for swivel_dot in swivel.get_instances():
            swivel_table.insert(swivel_dot.to_dict())
        
        # ConnectionLinks speichern in eigener Tabelle "connectionlinks", nur die IDs der Punkte
        connectionlinks_table = cls.db.table("connectionlinks")
        for connection in connectionlinks.get_instances():
            connectionlinks_table.insert(connection.to_dict())

    @classmethod
    def load_mechanism(cls, path="mechanism.json"):
        """
        Lädt einen Mechanismus und überschreibt alle Objekte für Klassen, die den Bulk-Update-Mechanismus unterstützen.
        """
        fixeddot.clear_instances()
        movabledot.clear_instances()
        swivel.clear_instances()
        connectionlinks.clear_instances()
        full_path = os.path.join("src", path)  # "src\" wird automatisch hinzugefügt
        cls.db = TinyDB(full_path)
        
        # Schritt 1: Dots laden
        dot_instances = {}  # Speichert die Instanzen der Dots nach ihrer ID
        # Fixeddots laden
        fixed_dot_table = cls.db.table("fixeddot")
        for dot_data in fixed_dot_table.all():
            dot_instances[dot_data["id"]] = fixeddot(**dot_data)
        
        # Movabledots laden
        movable_dot_table = cls.db.table("movabledot")
        for dot_data in movable_dot_table.all():
            dot_instances[dot_data["id"]] = movabledot(**dot_data)
        
        # Schritt 2: Swivels laden
        swivel_table = cls.db.table("swivel")
        for swivel_data in swivel_table.all():
            dot_instances[swivel_data["id"]] =swivel(**swivel_data)
            #swivel.create_instance(**swivel_data)

        # Schritt 3: ConnectionLinks laden und instanziieren
        connectionlinks_table = cls.db.table("connectionlinks")
        for link_data in connectionlinks_table.all():
            dot1 = dot_instances.get(link_data["dot1"]["id"])
            dot2 = dot_instances.get(link_data["dot2"]["id"])

            if dot1 and dot2:

                connectionlinks.create_instance(dot1=dot1, dot2=dot2)

        print("Mechanismus erfolgreich geladen!")

if __name__ == "__main__":
    # Beispielobjekte erstellen und speichern
    #d0 = fixeddot(0, 0, "d0")
    #d1 = movabledot(10, 35, "d1")
    #d2 = movabledot(5, 10, "d2")
    #s1 = swivel(-30, 0, (5**2 + 10**2)**0.5, math.atan(10/5), "s1")
    #c1 = connectionlinks(d0, d1)
    #c2 = connectionlinks(d1, d2)
    #c3 = connectionlinks(d2, s1)
    #c4 = connectionlinks(d2, d0)
    #Database.save_mechanism("mechanism.json")

    f=fixeddot(-28,-5,"f")
    a=movabledot(-16,23,"a")
    b=movabledot(-54,6.5,"b")
    c=movabledot(-44,-21.5,"c")
    d=movabledot(-21,-35,"d")
    e=movabledot(-35,-70,"e")
    s=swivel(0,0,10,0,"s")
    c1=connectionlinks(s,a)
    c2=connectionlinks(s,d)
    c3=connectionlinks(a,f)
    c4=connectionlinks(a,b)
    c5=connectionlinks(b,f)
    c6=connectionlinks(b,c)
    c7=connectionlinks(c,d)
    c8=connectionlinks(c,e)
    c9=connectionlinks(e,d)
    c10=connectionlinks(d,f)
    Database.save_mechanism("strandbeest.json")

    Database.load_mechanism("strandbeest.json")
    #print(swivel.get_instances())
    #print(fixeddot.get_instances())
    #print(movabledot.get_instances())
    print(connectionlinks.get_instances())
