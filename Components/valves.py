# AEther 23-24
# Creation: 15/02/2024
# Last edit: 25/04/2024
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
        def __init__(self,name:str,state:bool,type:str,actuation:str,diameter:float): 
                self.name = name # Identifier on the PI&D
                self.type = type
                self.state = state # Closed (0) or Opened (1)
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.diameter = diameter # Valve diameter
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False
            
            
class CheckValve:
        def __init__(self,name:str,state: bool,type: str,actuation:str,diameter:float): 
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.diameter = diameter #diameter of the valve
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False


# Pressure drop in valves

def dPBallValve(fluid:fluids.Fluid, valve:Valve, delta:float,velocity:float):
    # delta: opening angle of the ball valve
    xi = 0.0946*np.exp(0.1106*delta)
    dP = 1/2 * fluid.density * velocity**2 * xi
    
    return dP
    

def dPButterflyValve(fluid:fluids.Fluid,valve:Valve,delta:float,velocity:float):
    
    Re = fluid.density*velocity*valve.diameter/fluid.viscosity
    xi = 1/Re + 1 - 50/Re * 0.3166 * np.exp(0.0958 * delta)
    dP = 1/2 * fluid.density * velocity**2 * xi
    
    return dP


def dPGateValve(fluid:fluids.Fluid,valve:Valve,height:float,velocity:float):  #change Fluid by N2 or H2O2
    
    xi = 116.34 * np.exp(-7.98 * height / valve.diameter)
    dp = 1/2 * fluid.density * velocity**2 * xi
    
    return dp


def dPGlobeValve(fluid:fluids.Fluid,valve:Valve,velocity:float):
    
    xi = 1.0973 * valve.diameter**(-0.5955)
    dp = 1/2 * fluid.density * velocity**2 * xi
    
    return dp


def dPCheckValve(fluid:fluids.Fluid,valve:Valve,velocity:float):
    
    xi = 1.07 + 5.16 * valve.diameter - 6.71 * valve.diameter**2 + 4.93 * valve.diameter**3
    dp = 1/2 * fluid.density * velocity**2 * xi
    
    return dp

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

