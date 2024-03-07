# AEther 23-24
# Creation: 15/02/2024
# Last edit: 16/02/2024
# It models valves no matter type, elements that can be closed or opened and 
# through which a small amount of pressure is lost

# - Valve.py 
# - INPUT:
# -- Pin, coefficient
# -- Pin, geometry, type
# - OUTPUT:
# -- dP

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

# CLASS AND SUBCLASS DECLARATION
class Valve:
        def __init__(self,name:str,state: bool,type: str,actuation:str):
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = type # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False
            
            
class checkValve:
    def __init__(self,name:str):
        # Placeholder --> NOTE: can we assume it's going to be only a diode with no dP?
          self.name = name # Identifier on the PI&D


# Zapata functions

def dPZapataLiquid(fluid: fluids.Fluid, valve: Valve, massFlow: float):
    # Equation presented by Zapata in his S3 project report
    # NOTE: we assume all inputs are in SI
    # - Ql is the mass flow needs to be in m3/h
    # - SG is the ration between density of the liquid and that of water
    # - Kf is the flow factor

    rho = fluid.density # Assumed incompressible
    SG = fluid.density/1000 # Divided by water density
    Ql = massFlow/rho*3600 # in m3/h
    
    try:
        Kf = valve.fluidFactor
    except:
        Kf = 1  
        
    dP = 1E5*SG*(Ql/Kf)**2
    return dP
    
    
def dPZapataGas(fluid: gases.Gas, valve: Valve, massFlow: float, temperature: float, pressure: float):
    # Equation presented by Zapata in his S3 project report
    # NOTE: we assume all inputs are in SI
    # - Qg is the mass flow needs to be in L/min
    # - SG is the ration between density of the liquid and that of air
    # - Kf is the flow factor
    
    rho = pressure/(fluid.gasConstant*temperature)
    rhoAir = pressure/(287*temperature)
    SG = rho/rhoAir
    Qg = massFlow/rho*1000*60
    
    try:
        Kf = valve.fluidFactor
    except:
        Kf = 1   
        
    dP = 1E5*SG*temperature/(8062**2*pressure)*(Qg/Kf)**2
    return dP
    
    