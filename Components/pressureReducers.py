# AEther 23-24
# Creation: 16/02/2024
# Last edit: 16/04/2024
# It models pressure reducers that contain an incoming flow and deliver a set output pressure no matter it

# Native libraries
import numpy as np
import scipy
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
    def __init__(self, name: str, pressureData: list[PressureCurve]):
        self.name = name # Identifier on the PI&D
        self.pressureData = pressureData
        
    def addPressureCurve(self, pressureCurve: PressureCurve):
        self.pressureData.append(pressureCurve)

# Only the "reverse mode" is coded, that is, knowing the mass flow and the pressure at the output
def interpolatePressure(pressureReducer: PressureReducer, outputPressure: float, mdot: float):
    Pins = []
    mdots = []
    for pressureCurve in pressureReducer.pressureData:
        try:
            interpFunc = scipy.interpolate.interp1d(pressureCurve.Pout,pressureCurve.mdot)
            mdotTest = interpFunc(outputPressure) # NOTE: this will crash if the interpolation falls in a horizontal section of the curve
            Pins.append(pressureCurve.Pin)
            mdots.append(mdotTest)
        except:
            print("No interpolation available with curve with Pin = " + str(pressureCurve.Pin) + " Pa")
            # Just skip it
            
    # At this moment three scenarios might present themselves:
    # - No interpolation have been done --> program must give an error
    # - Only one curve is compatible --> linear approximation #NOTE: for now, this is CRAP
    # - 2+ curves are available --> normal procedure
    
    if not Pins:  # Empty list should be false
        print("No compatible pressure curve with the objective for this pressure reducer")
        return False
    elif len(Pins) == 1:
        # Test  
        c = 1.2  # NOTE: this is EVIL, it assumes linear proportionality between mass flow and input pressure input --> put a value based on reality
        return c*Pins[0]/mdots[0]*mdot
    else:
        interpFunc = scipy.interpolate.interp1d(mdots,Pins)
        return interpFunc(mdot)