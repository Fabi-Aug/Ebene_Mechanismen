from dot_class import dot

class connectionlinks:
    '''Class to represent a connection between two dots'''

    _instances = []

    def __init__(self, dot1: dot, dot2: dot):
        self.dot1 = dot1
        self.dot2 = dot2
        self.__class__._instances.append(self)

    def calc_length(self) -> float:
        x1,y1 = self.dot1.get_coordinates()
        x2,y2 = self.dot2.get_coordinates()
        length = ((x2-x1)**2 + (y2-y1)**2)**0.5	
        return length
    
    @classmethod
    def get_instances(cls):
        """Gibt alle erstellten Instanzen der Klasse zurück."""
        return cls._instances
    
    def __str__(self):
        return f"Link between {self.dot1} and {self.dot2} with length {self.calc_length()}"

    def __repr__(self):
        return self.__str__()
    
if __name__ == "__main__":
    d1 = dot(1,2)
    d2 = dot(3,4)
    c = connectionlinks(d1,d2)
    print(c)