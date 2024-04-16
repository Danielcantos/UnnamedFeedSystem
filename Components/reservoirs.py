# AEther 23-24
# Creation: 16/02/2024
# Last edit: 12/04/2024
# Two phase containers where the propellant is kept until forced out via pressurization

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

class Tank:
    def __init__(self, name: str, pressure: float, volume: float, diameter: float, thickness: float, inputDiameter: float, outputDiameter: float, positionInterface: float):
        self.name = name
        self.pressure = pressure # Internal pressure in Pa
        self.volume = volume # Internal volume in m3
        self.diameter = diameter # Internal diameter in m
        self.length = 4/np.pi*volume/self.diameter**2
        self.thickness = thickness
        self.inputDiameter = inputDiameter
        self.outputDiameter = outputDiameter
        self.positionInterface = positionInterface
        
def updateInterface(self, fluid: fluids.Fluid, mdotOut: float, dt: float):
    # Execute this at each timestep
    emptyingSpeed =  4*mdotOut/(np.pi*fluid.density*self.diameter**2)
    displacementInterface = emptyingSpeed*dt
    self.positionInterface += displacementInterface
    
def frictionFactor (fluid: fluids.Fluid, tank: Tank, massFlow: float):
    # Numerical and simplified implementation of the Darcy-Weisbach graph
    
    area = np.pi*(tank.diameter)**2/4 # Tube section
    u = massFlow/(area*fluid.density) # Speed inside of the conduit. Continuity equation
    nu = fluid.staticViscosity/fluid.density # Kinematic viscosity
    
    Re = u*tank.diameter/nu
  
    if Re < 2300:
        # Laminar flow
        fD = 64/Re
    elif Re < 63000:
        # Nikuradse for smooth pipes (Idelchik)
        fD = 0.3164/Re**0.25     
    else:
        # You should see this
        print("ERROR: high Re regime achieved in " + tank.name + " (Re = " + str(Re) + ")")
        fD = 10
        
    return fD

def xiInput(gas: gases.Gas, tank: Tank, massFlowIn: float, temperature: float):
    
    gasDensity = tank.pressure/(gas.gasConstant*temperature)

    area = np.pi*(tank.diameter)**2/4 # Tube section
    u = massFlowIn/(area*gasDensity) # Speed inside of the conduit. Continuity equation
    nu = gas.staticViscosity/gasDensity # Kinematic viscosity
    
    Re = u*tank.diameter/nu
    
    if Re > 3.5e3:
        xi = (1-tank.inputDiameter**2/tank.diameter**2)**2
    else:
        xi = 4.3*np.power(Re,-0.16)
        
    return xi

def xiOutput(fluid: fluids.Fluid, tank: Tank, massFlow: float):

    area = np.pi*(tank.diameter)**2/4 # Tube section
    u = massFlow/(area*fluid.density) # Speed inside of the conduit. Continuity equation
    nu = fluid.staticViscosity/fluid.density # Kinematic viscosity
    
    Re = u*tank.diameter/nu
    
    if Re > 1e4:
        xi =0.5*(1-tank.inputDiameter**2/tank.diameter**2)
    else:
        xi = 6.8*np.power(Re,-0.31)
        
    return xi

def dPIn(gas: gases.Gas, tank: Tank, massFlowIn: float, speed: float, temperature: float):
    fD = 0.0 # Friction with gas assumed negligible
    xi = xiInput(gas,tank,massFlowIn, temperature)
    gasDensity = tank.pressure/(gas.gasConstant*temperature)
    dP = (xi + fD*tank.positionInterface/tank.diameter)*gasDensity*speed**2/2

def dPOut(fluid: fluids.Fluid,tank: Tank, massFlowOut: float, speed: float):   
    fD = frictionFactor(fluid,tank,massFlowOut)
    xi = xiOutput(fluid,tank,massFlowOut)
    dPOut = (xi + fD*(tank.length-tank.positionInterface)/tank.diameter)*fluid.density*speed**2/2

def dPTot(fluid: fluids.Fluid, gas: gases.Gas, tank: Tank, massFlowOut: float, temperature: float, pressure: float):
    
    area = np.pi*(tank.diameter)**2/4 # Tube section
    rho = fluid.density # Assumed incompressible
    w0 = massFlowOut/(area*rho) # Speed inside of the conduit. Continuity equation
    
    dPOutput = dPOut(fluid,tank,massFlowOut,w0)
    Pin = pressure + dPOutput
    
    massFlowIn = densityInterface(gas, tank, massFlowOut, temperature, pressure)
    dPInput = dPIn(gas,tank,massFlowIn,w0,temperature)
    
    dP = dPInput + dPOutput
    
    return dP

def densityInterface(gas: gases.Gas, tank: Tank, massFlowOut: float, temperature: float, pressure: float):
    gasDensity = tank.pressure/(gas.gasConstant*temperature)
    
    massFlowIn = massFlowOut*pressure/(gasDensity*gas.gasConstant*temperature) 
    
    # NOTE: the pressure shouldn't directly be an input, is a part of the chain
    
    return massFlowIn