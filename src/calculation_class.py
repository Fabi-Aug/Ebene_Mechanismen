from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt

class calculation:
    '''
    A class that represents a calculation, ploting and saving of a 2D plane.'''
    def __init__(self):
        self._dots = dot.get_instances()
        self._connections = connectionlinks.get_instnaces()
        self._fixeddots = fixeddot.get_instances()
        
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
