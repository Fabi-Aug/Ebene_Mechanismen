from tinydb import TinyDB, Query
from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
import math
import os

class Database:
    def __init__(self, db_path : str):
        """Initialize the database with a given path."""
        full_path = os.path.join("src", db_path)  # "src\" automatically added
        self.db = TinyDB(full_path)

    @classmethod
    def save_mechanism(cls, path : str):
        """Save the mechanism to a JSON file."""
        full_path = os.path.join("src", path)  # "src\" automatically added
        with open(full_path, "w") as f:
            f.write("")
        cls.db = TinyDB(full_path)
        
        # Save fixed dots in their own table "fixeddot"
        fixed_dot_table = cls.db.table("fixeddot")
        for fixed_dot in fixeddot.get_instances():
            fixed_dot_table.insert(fixed_dot.to_dict())
        
        # Save movable dots in their own table "movabledot"
        movable_dot_table = cls.db.table("movabledot")
        for movable_dot in movabledot.get_instances():
            movable_dot_table.insert(movable_dot.to_dict())
        
        # Save swivels in their own table "swivel"
        swivel_table = cls.db.table("swivel")
        for swivel_dot in swivel.get_instances():
            swivel_table.insert(swivel_dot.to_dict())
        
        # Save connection links in their own table "connectionlinks", only the IDs of the dots
        connectionlinks_table = cls.db.table("connectionlinks")
        for connection in connectionlinks.get_instances():
            connectionlinks_table.insert(connection.to_dict())

    @classmethod
    def load_mechanism(cls, path: str):
        """
        Load a mechanism and overwrite all objects for classes that support the bulk update mechanism.
        """
        fixeddot.clear_instances()
        movabledot.clear_instances()
        swivel.clear_instances()
        connectionlinks.clear_instances()
        full_path = os.path.join("src", path)  # "src\" automatically added
        cls.db = TinyDB(full_path)
        
        dot_instances = {}  # Store the instances of the dots by their ID
        # Load fixed dots
        fixed_dot_table = cls.db.table("fixeddot")
        for dot_data in fixed_dot_table.all():
            dot_instances[dot_data["id"]] = fixeddot(**dot_data)
        
        # Load movable dots
        movable_dot_table = cls.db.table("movabledot")
        for dot_data in movable_dot_table.all():
            dot_instances[dot_data["id"]] = movabledot(**dot_data)
        
        # Load swivels
        swivel_table = cls.db.table("swivel")
        for swivel_data in swivel_table.all():
            dot_instances[swivel_data["id"]] = swivel(**swivel_data)

        # Load connection links and instantiate
        connectionlinks_table = cls.db.table("connectionlinks")
        for link_data in connectionlinks_table.all():
            dot1 = dot_instances.get(link_data["dot1"]["id"])
            dot2 = dot_instances.get(link_data["dot2"]["id"])

            if dot1 and dot2:
                connectionlinks.create_instance(dot1=dot1, dot2=dot2)

        print("Mechanism successfully loaded!")

if __name__ == "__main__":
    # Create and save example objects
    #d0 = fixeddot(0, 0, "d0")
    #d1 = movabledot(10, 35, "d1")
    #d2 = movabledot(5, 10, "d2")
    #s1 = swivel(-30, 0, (5**2 + 10**2)**0.5, math.atan(10/5), "s1")
    #c1 = connectionlinks(d0, d1)
    #c2 = connectionlinks(d1, d2)
    #c3 = connectionlinks(d2, s1)
    #c4 = connectionlinks(d2, d0)
    #Database.save_mechanism("mechanism.json")

    f = fixeddot(-28, -5, "f")
    a = movabledot(-16, 23, "a")
    b = movabledot(-54, 6.5, "b")
    c = movabledot(-44, -21.5, "c")
    d = movabledot(-21, -35, "d")
    e = movabledot(-35, -70, "e")
    s = swivel(0, 0, 10, 0, "s")
    c1 = connectionlinks(s, a)
    c2 = connectionlinks(s, d)
    c3 = connectionlinks(a, f)
    c4 = connectionlinks(a, b)
    c5 = connectionlinks(b, f)
    c6 = connectionlinks(b, c)
    c7 = connectionlinks(c, d)
    c8 = connectionlinks(c, e)
    c9 = connectionlinks(e, d)
    c10 = connectionlinks(d, f)
    Database.save_mechanism("strandbeest.json")
    Database.save_mechanism("flksf.json")

    Database.load_mechanism("strandbeest.json")
    #print(swivel.get_instances())
    #print(fixeddot.get_instances())
    #print(movabledot.get_instances())
    print(connectionlinks.get_instances())
