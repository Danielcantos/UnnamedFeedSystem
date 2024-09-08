# AEther 23-24
# Creation: 16/02/2024
# Last edit: 20/07/2024
# It models pressure reducers that contain an incoming flow and deliver a set output pressure no matter it

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
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
    Pouts = []
    for pressureCurve in pressureReducer.pressureData:
        
        f_found = False # Flag marking if the objective could be interpolated in the present curve
        for i, valueMdot in enumerate(pressureCurve.mdot):
            if valueMdot < mdot:
                continue
            else: 
                PoutInterp = pressureCurve.Pout[i-1] + (pressureCurve.Pout[i] - pressureCurve.Pout[i-1])/(pressureCurve.mdot[i] - pressureCurve.mdot[i-1])*(mdot - pressureCurve.mdot[i-1])
                Pins.append(pressureCurve.Pin)
                Pouts.append(PoutInterp)
                f_found = True
                break
        
        if not f_found:
            print("No interpolation available with curve with Pin = " + str(pressureCurve.Pin) + " Pa")
                      
    # At this moment three scenarios might present themselves:
    # - No interpolation have been done --> program must give an error
    # - Only one curve is compatible --> linear approximation #NOTE: for now, this is CRAP
    # - 2+ curves are available --> normal procedure
    
    if not Pins:  # Empty list should be false
        print("No compatible pressure curve with the objective for this pressure reducer")
        return False
    elif len(Pins) == 1:
        # Test  
        c = Pins[0]/Pouts[0] # NOTE: this is evil
        return c*outputPressure
    else:
        
        for i, valuePout in enumerate(Pouts):
            if valuePout < outputPressure:
                continue
            else:
                PinInterp = Pins[i-1] + (Pins[i]-Pins[i-1])/(Pouts[i]-Pouts[i-1])*(outputPressure-Pouts[i-1])
                return PinInterp
