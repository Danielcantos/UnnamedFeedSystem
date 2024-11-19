# AEther 23-24
# Creation: 16/02/2024
# Last edit: 19/11/2024
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
        '''
        Class codifying a set of curves mass flow - output pressure for a given input pressure.
        These are used to describe the behaviour of a pressure reducer.
        - Pin is the input pressure in Pa
        - mdot is an array of mass flows in kg/s
        - Pout is the corresponding array of output pressures in Pa
        '''
        self.Pin = Pin
        self.mdot = mdot
        self.Pout = Pout
        
class PressureReducer:
    def __init__(self, name: str, pressureData: list[PressureCurve]):
        '''
        Object modelling the behaviour of a pressure reducer from a set of output curves for a given input pressure.
        It accepts a list of pressure curves of any size.
        - name is the code identifying the piece
        - pressureDate is the list of PressureCurve objects
        '''
        self.name = name # Identifier on the PI&D
        self.pressureData = pressureData
        
    def addPressureCurve(self, pressureCurve: PressureCurve):
        '''
        Appends a new pressure curve to the pressureData list of the PressureReducer object
        - pressureCurve is the PressureCurve object to add
        '''
        self.pressureData.append(pressureCurve)
        
    def dP(self,node):
        '''
        Returns the loss of pressure on the component based on the behaviour of the pressure reducer prescribed by its curves.
        - node: point on the hydraulic chain in which the pressure reducer is located, and its associated data
        '''
        Pin = interpolatePressure(self,node)
        dP = Pin - node.P
        
        return dP

# Only the "reverse mode" is coded, that is, knowing the mass flow and the pressure at the output
def interpolatePressure(pressureReducer: PressureReducer, node):
    Pins = []
    Pouts = []
    mdot = node.mdot
    outputPressure = node.P
    
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
        return outputPressure
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
