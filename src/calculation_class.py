from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
import math


class Calculation:
    '''
    A class that represents a calculation, ploting and saving of a 2D plane.'''
    def __init__(self):
        self._dots = dot.get_instances()
        self._connections = connectionlinks.get_instances()
        self._fixeddots = fixeddot.get_instance()
        self._swivels = swivel.get_instance()
        self._n = len(self._dots)
        self._m = len(self._connections)

        
    @staticmethod
    def check_dof(self):
        f = 2*self._n-2-2-self._m
        return f

    @staticmethod
    def calculate(self, phi):
        
        self._swivels.set_phi(phi)
        if self.check_dof(self) != 0:
            raise ValueError("The calculation is not possible, because the system is not statically determined.")
        x = np.array([dot.get_coordinates() for dot in self._dots]).reshape(-1,1)
        print(x)
        A = np.zeros((2*self._m, 2*self._n), dtype=int)
        
        for i in range(2*self._m):  
            A[i, i ] = 1  
            A[i, i + 2] = -1
        print(A)
        l = np.dot(A, x)
        print(l)
        L = np.array([np.linalg.norm([l[i+2,0],l[i,0]]) for i in range(self._m)]).reshape(-1,1)
        print(L)

        
        
    
    
    def save(self, path):
        pass

    def load(self, path):
        pass
    
    def plot(self):
        pass
    
    def __str__(self):
        return f"Calculation: dots:{self._dots}\nconnections:{self._connections}\nfixeddots:{self._fixeddots}\nswivels:{self._swivels}\n"

if __name__ == "__main__":  
    d0 = fixeddot(0,0)
    d1 = dot(10,35)
    
    c3 = connectionlinks(d0,d1)
    s1 = swivel(-30,0,11.18,1.107)
    c4 = connectionlinks(d1,s1)
    calc = Calculation()
    print(s1.get_circlepoint())
    print(s1.get_coordinates())
    print(calc)
    print(f"dof: {calc.check_dof(calc)}\n")
    print(f"calculation: {calc.calculate(calc,math.atan(10/5))}\n")
    print(f"calculation: {calc.calculate(calc,1.5)}\n")