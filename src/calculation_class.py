from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt

class Calculation:
    '''
    A class that represents a calculation, ploting and saving of a 2D plane.'''
    def __init__(self):
        self._dots = dot.get_instances()
        self._connections = connectionlinks.get_instances()
        self._fixeddots = fixeddot.get_instance()
        self._swivels = swivel.get_instance()

    @classmethod
    def calculate_(self):
        pass
    
    @classmethod
    def save(self, path):
        pass

    @classmethod
    def load(self, path):
        pass
    
    @classmethod
    def plot(self):
        pass
    
    def __str__(self):
        return f"Calculation: {self._dots}, {self._connections}, {self._fixeddots}, {self._swivels}"

if __name__ == "__main__":  
    d1 = dot(1,2)
    d2 = dot(3,4)
    d3 = fixeddot(5,6)
    c1 = connectionlinks(d1,d2)
    c2 = connectionlinks(d2,d3)
    c3 = connectionlinks(d3,d1)
    s1 = swivel(1,2,1,0)
    Calculation()
    print(Calculation())