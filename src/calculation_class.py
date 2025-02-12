from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as opt
import math


class Calculation:
    '''
    A class that represents a calculation, plotting and saving of a 2D plane.'''
    def __init__(self):
        self._dots = dot.get_all_instances()
        self.movabledots = movabledot.get_instances()
        self._connections = connectionlinks.get_instances()
        self._fixeddots = fixeddot.get_instance()
        self._swivels = swivel.get_instance()
        self._n = len(self._dots)
        self._m = len(self._connections)
 
    
    def check_dof(self):
        f = 2*self._n-2-2-self._m
        return f

    def calculate(self, phi, phi2,params):
        
        self._swivels.set_phi(phi)
        if self.check_dof() != 0:
            raise ValueError("The calculation is not possible, because the system is not statically determined.")
        
        l_c = np.zeros((0, 1))  
        for connection in self._connections:
            l_c = np.vstack((l_c, [[connection.calc_length()]])) 

        for i, movable in enumerate(self.movabledots):
            x, y = params[2*i:2*i+2]
            movable.set_coordinates(x, y)


        self._swivels.set_phi(phi2)
        l_n = np.zeros((0, 1))  
        for connection in self._connections:
            l_n = np.vstack((l_n, [[connection.calc_length()]])) 

        e = (l_n - l_c).flatten()
        return e
    
    def optimizer(self,phi,phi2):
        def objective(params):
            return self.calculate(phi,phi2,params)

        md = []
        for movable in self.movabledots:
            md.extend(movable.get_coordinates())

        result = opt.least_squares(objective, md)
        #print(result)
        return result.x

    def trajectory(self):
        pass



    def save_csv(self, path, dot: movabledot):
        df = pd.DataFrame({"x": dot.x_values, "y": dot.y_values})
        df.to_csv(path, index=False)



        



    def load(self, path):
        pass
    
    def plot(self):
        pass
    
    def __str__(self):
        return f"Calculation: dots:{self._dots}\nconnections:{self._connections}\nfixeddots:{self._fixeddots}\nswivels:{self._swivels}\n"

if __name__ == "__main__":  
    d0 = fixeddot(0,0)
    d1 = movabledot(10,35)
    d2 = movabledot(5,10)
    s1 = swivel(-30,0,(5**2+10**2)**0.5,math.atan(10/5))

    c1 = connectionlinks(d0, d1)
    c2 = connectionlinks(d1, d2)
    c3 = connectionlinks(d2, s1)
    c4 = connectionlinks(d2, d0)
    calc = Calculation()
    #print(c4.calc_length())
    #print(c3.calc_length())

    angles = np.linspace(0, 2 * math.pi, 360)  # 1000 Werte zwischen 0 und 2π

    calc.save_csv("C:/Schule_24-25/Python_Schule/AbschlussProjekt/Ebene_Mechanismen/src/test.csv", d2)


    # Plot für X- und Y-Werte
    #plt.figure(figsize=(8, 6))
    #plt.plot( x_values,y_values, color="blue")
    #plt.xlim(-40, 20)
    #plt.ylim(-10, 40)
    #plt.show()


