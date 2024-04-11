# AEther 23-24
# Creation: 16/02/2024
# Last edit: 05/04/2024
# It models pressure reducers that contain an incoming flow and deliver a set output pressure no matter it

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

# CLASS AND SUBCLASS DECLARATION

class PressureCurve:
    def __init__(self,Pin: float, mdot: np.array, Pout: np.array):
        self.Pin = Pin
        self.mdot = mdot
        self.Pout = Pout
        
class PressureReducer:
    def __init__(self, name: str, pressureData: list):
        self.name = name # Identifier on the PI&D
        self.pressureData = pressureData
        
    def addPressureCurve(self, pressureCurve: PressureCurve):
        self.pressureData.append(pressureCurve)

        
def interpolatePressure(gas: gases.Gas, pressure: float):
    # Not coded for now
    return 0