# AEther 23-24
# Creation: 15/02/2024
# Last edit: 19/11/2024
# It models valves no matter type, elements that can be closed or opened and 
# through which a small amount of pressure is lost

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import materials


# CLASS AND SUBCLASS DECLARATION
class Valve:
        def __init__(self,name:str,state:bool,type:str,actuation:str,diameter:float,coefficient:float): 
            '''
            Object used to describe two-way valves of any type (so not including check valves).
            - name is the code identifying the piece
            - state is a boolean defining closed (False) and opened (True) states. NOTE: unused as of 19/11/2024
            - type is a string defining the internal mechanism of the valve (ball, solenoid...)
            - actuation is a string defining the activation mechanism of the valve (manual, electrical, pneumatic...) NOTE: unused as of 19/11/2024
            - material is a Material object
            - diameter is the internal diameter of the valve in m (thread standard can be used)
            - coefficient is the pressure loss coefficient of the valve
            '''
            self.name = name # Identifier on the PI&D
            self.type = type
            self.state = state # Closed (0) or Opened (1)
            self.actuation = actuation # Manual, electrical or pneumatic
            self.diameter = diameter # Valve diameter
            self.coefficient = coefficient # The valve's Cv, -1 if there's no coefficient
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False
            
        def dP(self,node): # Node is not defined here, but in main
            '''
            Returns the correct loss of pressure in Pa based on the type of valve and the fluid.
            - node: point on the hydraulic chain in which the valve is located and associated data.
            '''
            dP = 0
            if type(node.fluid) is fluids.Gas:
                 dP = dPKvGas(node.fluid,self,node) # Will work with or without defines loss
            elif type(node.fluid) is fluids.Liquid: # It's a liquid
                S = np.pi/4*self.diameter**2
                v  = node.mdot/(S*node.fluid.density) # Continuity
                if self.coefficient > 0: # There is a defined coefficient
                        dP = dPKvLiquid(node.fluid,self,node)
                else:
                    match self.type.lower():
                        case "ball":
                            dP = dPBallValve(node.fluid,self,0.0,v)
                        case "butterfly":
                            dP = dPButterflyValve(node.fluid,self,0.0,v)
                        case "gate": 
                            # NOTE: as of 2024 it only admets fully opened as the diameter is passed as height
                            dP = dPGateValve(node.fluid,self,self.diameter,v)
                        case "globe":
                            dP = dPGlobeValve(node.fluid,self,v)
                        case _:
                            # Assume a valve coefficient of 1, which is a lot
                            self.coefficient = 1
                            dP = dPKvLiquid(node.fluid,self,node)
            else:
                print("Is not gas or liquid. Are you trying to push a solid through the valve?")
            
            return dP
            
class CheckValve:
        def __init__(self,name:str,state:bool,type:str,actuation:str,diameter:float): 
            '''
            Object used to describe one-way valves.
            - name is the code identifying the piece
            - state is a boolean defining closed (False) and opened (True) states. NOTE: unused as of 19/11/2024
            - type is a string defining the internal mechanism of the valve (ball, solenoid...)
            - actuation is a string defining the activation mechanism of the valve (manual, electrical, pneumatic...) NOTE: unused as of 19/11/2024
            - material is a Material object
            - diameter is the internal diameter of the valve in m
            '''
            self.name = name # Identifier on the PI&D
            self.state = state # Closed (0) or Opened (1)
            self.actuation = actuation # Manual, solenoid or pneumatic
            self.diameter = diameter #diameter of the valve
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False
            
        def dP(self,node): 
            '''
            Returns the correct loss of pressure in Pa based on the fluid.
            - node: point on the hydraulic chain in which the valve is located
            '''
            if type(node.fluid) is fluids.Gas: # It's a gas
                dP = 0.0
            elif type(node.fluid) is fluids.Liquid: # It's a liquid
                S = np.pi/4*self.diameter**2
                v  = node.mdot/(S*node.fluid.density)
                dP = dPCheckValve(node.fluid,self,v) # Cannot call dPKvLiquid, since it's not a valve
            else: 
                print("Is not gas or liquid. Are you trying to push a solid through the valve?")
        


# Pressure drop in valves (from analytical equations)
def dPBallValve(fluid:fluids.Liquid,valve:Valve,delta:float,velocity:float):
    '''
    Calculates the loss of pressure in Pa for a ball valve partially or completely open under liquid flow.
    - fluid is the Fluid object
    - valve is the Valve object
    - delta is the opening angle of the valve in deg (where 90 is fully closed)
    - velocity is the fluid flow speed in m/s
    '''
    # From Idelchik, adapted by Louis Urbin (2023-24)
    xi = 0.0946*np.exp(0.1106*delta)
    dP = 1/2 * fluid.density * velocity**2 * xi
    
    return dP
    

def dPButterflyValve(fluid:fluids.Liquid,valve:Valve,delta:float,velocity:float):
    '''
    Calculates the loss of pressure in Pa for a butterfly valve partially or completely open under liquid flow.
    - fluid is the Fluid object
    - valve is the Valve object
    - delta is the opening angle of the valve in deg (where 90 is fully closed)
    - velocity is the fluid flow speed in m/s
    '''
    # From Idelchik, adapted by Louis Urbin (2023-24)
    Re = fluid.density*velocity*valve.diameter/fluid.dynamicViscosity
    xi = 1/Re + 1 - 50/Re * 0.3166 * np.exp(0.0958 * delta)
    dP = 1/2 * fluid.density * velocity**2 * xi
    
    return dP


def dPGateValve(fluid:fluids.Liquid,valve:Valve,height:float,velocity:float):  #change Fluid by N2 or H2O2
    '''
    Calculates the loss of pressure in Pa for a gate valve partially or completely open under liquid flow.
    - fluid is the Fluid object
    - valve is the Valve object
    - height is the how much of the diameter is unobstructed in m (where one valve diameter is fully opened)
    - velocity is the fluid flow speed in m/s
    '''
    # From Idelchik, adapted by Louis Urbin (2023-24)
    xi = 116.34 * np.exp(-7.98 * height / valve.diameter)
    dP = 1/2 * fluid.density * velocity**2 * xi
    
    return dP


def dPGlobeValve(fluid:fluids.Liquid,valve:Valve,velocity:float):
    '''
     Calculates the loss of pressure in Pa for a globe valve under liquid flow.
    - fluid is the Fluid object
    - valve is the Valve object
    - velocity is the fluid flow speed in m/s   
    '''
    # From Idelchik, adapted by Louis Urbin (2023-24)
    xi = 1.0973 * valve.diameter**(-0.5955)
    dP = 1/2 * fluid.density * velocity**2 * xi
    
    return dP


def dPCheckValve(fluid:fluids.Liquid,valve:Valve,velocity:float):
    '''
    Calculates the loss of pressure in Pa for a check valve under liquid flow.
    - fluid is the Fluid object
    - valve is the Valve object
    - velocity is the fluid flow speed in m/s   
    '''
    # From Idelchik, adapted by Louis Urbin (2023-24)
    xi = 1.07 + 5.16 * valve.diameter - 6.71 * valve.diameter**2 + 4.93 * valve.diameter**3
    dP = 1/2 * fluid.density * velocity**2 * xi
    return dP


# Pressure drop in valves (from product data)
def dPKvLiquid(fluid:fluids.Liquid,valve:Valve,node):
    '''
    Calculates the loss of pressure in Pa for a valve with a known loss coefficient under a liquid flow.
    It will fail if no valve coefficient is defined.
    - fluid is the Liquid object
    - valve is the Valve object
    - node is the Node object
    '''
    # https://www.pipeflow.com/public/PipeFlowExpertSoftwareHelp/html/CvandKvFlowCoefficients1.html
    massFlow = node.mdot
    Q = 3600/fluid.density*massFlow # Assumed kg/s, transformed into m3/h
    dP = fluid.density/1000*(Q/valve.coefficient)**2 # In bar by default
 
    return dP*1e5

def dPKvGas(fluid:fluids.Gas,valve:Valve,node):
    '''
    Calculates the loss of pressure in Pa for a valve with a known loss coefficient under a gas flow. 
    If the coefficient is unknown, it assumes Kv = 1. Ideal gas is assumed for any case.
    - fluid is the Gas object
    - valve is the Valve object
    - node is the Node object
    '''
    # https://www.samsongroup.com/document/t00050en.pdf.
    massFlow = node.mdot
    pressure = node.P
    temperature = node.T
    rho = pressure/(fluid.gasConstant*temperature)
    Q = 3600/rho*massFlow# Assumed kg/s, transformed into m3/h
    rhoG = 101325/(fluid.gasConstant*273) # Density at atmospheric pressure and 0 ºC
    if valve.coefficient > 0:
        dP = (Q/(514*valve.coefficient))**2*(rhoG*temperature)/pressure
    else: # Takes coefficient as unity (as done by Zapata)
        dP = (Q/(514*1))**2*(rhoG*temperature)/pressure
    
    return dP*1e5
        
        
        
# Pressure drop in valves (from Zapata functions) - DEPRECTED BY dPKvLiquid & dPKvGas

# def dPZapataLiquid(fluid: fluids.Liquid, valve: Valve, massFlow: float):
#     # Equation presented by Zapata in his S3 project report
#     # NOTE: we assume all inputs are in SI
#     # - Ql is the mass flow needs to be in m3/h
#     # - SG is the ration between density of the liquid and that of water
#     # - Kf is the flow factor

#     rho = fluid.density # Assumed incompressible
#     SG = fluid.density/1000 # Divided by water density
#     Ql = massFlow/rho*3600 # in m3/h
    
#     try:
#         Kf = valve.fluidFactor
#     except:
#         Kf = 1  
        
#     dP = 1E5*SG*(Ql/Kf)**2
#     return dP
   
# def dPZapataGas(fluid: fluids.Gas, valve: Valve, massFlow: float, temperature: float, pressure: float):
#     # Equation presented by Zapata in his S3 project report
#     # NOTE: we assume all inputs are in SI
#     # - Qg is the mass flow needs to be in L/min
#     # - SG is the ration between density of the liquid and that of air
#     # - Kf is the flow factor
    
#     rho = pressure/(fluid.gasConstant*temperature)
#     rhoAir = pressure/(287*temperature)
#     SG = rho/rhoAir
#     Qg = massFlow/rho*1000*60
    
#     try:
#         Kf = valve.fluidFactor
#     except:
#         Kf = 1   
        
#     dP = 1E5*SG*temperature/(8062**2*pressure)*(Qg/Kf)**2
#     return dP