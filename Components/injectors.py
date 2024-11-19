# AEther 23-24
# Creation: 19/06/2024
# Last edit: 19/11/2024
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
        '''
        Object used to describe curved an injector characterized by its curve.
        - name is the code identifying the piece
        - linearCoefficient is the "a" coefficient of the mdot = a·dP^n expression, for dP in bar
        - exponentialCoefficient is the "n" coefficient of the mdot = a·dP^n expression, for dP in bar
        - material is a Material object
        '''
        self.name = name # Identifier on the PI&D
        self.linearCoefficient = linearCoefficient # Linear coefficient (a) of a mdot = a·dP^n expression, dP in bar
        self.exponentialCoefficient = exponentialCoefficient # Exponential coefficient (n) of a mdot = a·dP^n expression, dP in bar
        self.material = material # Specific object type
        
    def dP(self, node):
        '''
        Returns the loss of pressure in Pa based on the mdot = a·dP^n that characterized the injector.
        If unavailable it can be manually extracted from curve fitting on provider data.
        - 
        '''
        if type(node.fluid) is fluids.Liquid: # It's a liquid
            massFlow = node.mdot
            dP = 1e5*(massFlow/self.linearCoefficient)**(1/self.exponentialCoefficient)
        else: # It's a gas
            print("Why are you injecting a gas?")
            dP = 0
            
        return dP
