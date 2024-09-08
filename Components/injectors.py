# AEther 23-24
# Creation: 19/06/2024
# Last edit: 08/09/2024
# It defines an injector from the characteristic curve of the component

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import materials

# ----------------------------------------------------
# CLASS DEFINITIONS
# ----------------------------------------------------

class Injector:
    def __init__(self, name: str, linearCoefficient: float, exponentialCoefficient: float, material: materials.Material):
        self.name = name # Identifier on the PI&D
        self.linearCoefficient = linearCoefficient # Linear coefficient (a) of a mdot = a·dP^n expression, dP in bar
        self.exponentialCoefficient = exponentialCoefficient # Exponential coefficient (n) of a mdot = a·dP^n expression, dP in bar
        self.material = material # Specific object type
        

def dP(fluid:fluids.Liquid, injector:Injector, massFlow:float):
    dP = 1e5*(massFlow/injector.linearCoefficient)**(1/injector.exponentialCoefficient)
    return dP