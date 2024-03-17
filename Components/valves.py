# AEther 23-24
# Creation: 15/02/2024
# Last edit: 14/03/2024
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
class Ball_valve:
        def __init__(self,name:str,state: bool,type: str,actuation:str,delta:float,fluid_velocity:float): 
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = ball # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.delta = delta #valve opening angle
                self.fluid_velocity = velocity #velocity of the incoming fluid
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False
            
            
class Check_valve:
        def __init__(self,name:str,state: bool,type: str,actuation:str,delta:float,diameter:float,fluid_velocity:float): 
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = check # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.fluid_velocity = velocity #velocity of the incoming fluid
                self.diameter = diameter #diameter of the valve
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False


class Butterfly_valve:
        def __init__(self,name:str,state: bool,type: str,actuation:str,delta:float,diameter:float,fluid_velocity:float): 
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = butterfly # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.delta = delta #valve opening angle
                self.fluid_velocity = velocity #velocity of the incoming fluid
                self.diameter = diameter #diameter of the valve
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False


class Gate_valve:
        def __init__(self,name:str,state: bool,type: str,actuation:str,opening:float,diameter:float,fluid_velocity:float): 
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = gate # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.height_open = height_open #valve opening height
                self.fluid_velocity = velocity #velocity of the incoming fluid
                   
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False


class Globe_valve:
        def __init__(self,name:str,state: bool,type: str,actuation:str,delta:float,diameter:float,fluid_velocity:float): 
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = globe # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                self.fluid_velocity = velocity #velocity of the incoming fluid
                self.diameter = diameter #diameter of the valve
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False


# Pressure drop in valves

def dp_ball_valve(valve:Ball_valve, fluid: fluids.Fluid):
    
    xi = 0.0946*exp(0.1106*h/self.diameter)
    dp = 1/2*fluid.density*valve.fluid_velocity**2*xi
    
    return dp
    

def dp_ball_valve(valve:Butterfly_valve, fluid: fluids.Fluid):
    
    Re = *fluid.density*valve.fluid_velocity*valve.diameter/fluid.viscosity
    xi = 1/Re + 1 - 50/Re*0.3166*exp(0.0958*self.delta)
    dp = 1/2*fluid.density*valve.liquid_velocity**2*xi
    
    return dp


def dp_gate_valve(valve = Gate_valve, fluid: fluids.Fluid):
    
    xi = 116.34*exp(-7.98*valve.height_open/valve.diameter)
    dp = 1/2*fluid.density*valve.fluid_velocity**2*xi
    
    return dp


def dp_globe_valve(valve = Globe_valve, fluid: fluids.Fluid):
    
    xi = 1.0973*valve.diameter**(-0.5955)
    dp = 1/2*fluid.density*valve.fluid_velocity**2*xi
    
    return dp


def dp_check_valve(valve = Check_valve, fluid: fluids.Fluid):
    
    xi = 1.07 + 5.16*valve.diameter - 6.71*valve.diameter**2 + 4.93*valve.diameter**3
    dp = 1/2*fluid.density*valve.fluid_velocity**2*xi
    
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

