# AEther 23-24
# Creation: 16/02/2024
# Last edit: 07/07/2024
# Two phase containers where the propellant is kept until forced out via pressurization

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

# ----------------------------------------------------
# CLASS DEFINITIONS
# ----------------------------------------------------

class TankInterface:
    def __init__(self, upstreamSubstance: gases.Gas, downstreamSubstance: fluids.Fluid, positionInterface: float):
        self.upstreamSubstance = upstreamSubstance # Pressurizer gas
        self.downstreamSubstance = downstreamSubstance # Fluid
        self.positionInterface = positionInterface # With respects to the 
        
class Tank:
    def __init__(self, name: str, pressure: float, volume: float, diameter: float, thickness: float, inputDiameter: float, outputDiameter: float, interface: TankInterface):
        self.name = name
        self.pressure = pressure # Internal pressure in Pa
        self.volume = volume # Internal volume in m3
        self.diameter = diameter # Internal diameter in m
        self.thickness = thickness
        self.inputDiameter = inputDiameter
        self.outputDiameter = outputDiameter
        self.interface = interface
        self.length = 4*self.volume/(np.pi*self.diameter**2)

# ----------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------

# Interfaces

def updateInterface(tank: Tank, mdotOut: float, dt: float):
    # Execute this at each timestep
    emptyingSpeed =  4*mdotOut/(np.pi*tank.interface.downstreamSubstance.density*tank.diameter**2)
    displacementInterface = emptyingSpeed*dt
    tank.interface.positionInterface += displacementInterface

def densityInterface(tank: Tank, massFlowOut: float, temperature: float, pressure: float):
    massFlowIn = massFlowOut*pressure/(tank.interface.upstreamSubstance.gasConstant*temperature*tank.interface.downstreamSubstance.density) 
    
    # NOTE: the pressure shouldn't directly be an input, is a part of the chain
    
    return massFlowIn

# Helper functions pressure
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
    
    FF = tank.inputDiameter/tank.diameter
    
    if Re > 3.5e3:
        xi = (1-FF)**2
    elif Re > 500:
        xi = -8.44556 - 26.163*(1-FF)**2 - 5.3808*(1-FF)**4 + \
        np.log10(Re)*(6.007 + 18.5372*(1-FF)**2  + 3.9978*(1-FF)**4) + \
        (np.log10(Re))**2*(-1.02318 - 3.091691*(1-FF)**2 - 0.680943*(1-FF)**4)
    elif Re > 10:
        xi = 3.62536 + 10.744*(1-FF)**2 - 4.41041*(1-FF)**4 + \
        1/np.log10(Re)*(-18.13 - 56.77855*(1-FF)**2 + 33.40344*(1-FF)**4) + \
        1/(np.log10(Re))**2*(30.8558 + 99.9542*(1-FF)**2 - 62.78*(1-FF)**4) + \
        1/(np.log10(Re))**3*(-13.217 - 53.955*(1-FF)**2 + 33.8053*(1-FF)**4)
    else:
        xi = 30/Re
        
        #xi = 4.3*np.power(Re,-0.16) # NOTE: old Louis Urbin adjustment (2024)
        
    return xi

def xiOutput(fluid: fluids.Fluid, tank: Tank, massFlow: float):

    area = np.pi*(tank.diameter)**2/4 # Tube section
    u = massFlow/(area*fluid.density) # Speed inside of the conduit. Continuity equation
    nu = fluid.staticViscosity/fluid.density # Kinematic viscosity
    
    Re = u*tank.diameter/nu
    
    if Re > 1e4:
        xi = 0.5*(1-tank.inputDiameter**2/tank.diameter**2)
    else:
        xi = 6.8*np.power(Re,-0.31)
        
    return xi

# ----------------------------------------------------
# PRESSURE LOSSES
# ----------------------------------------------------

def dPIn(tank: Tank, massFlowIn: float, temperature: float):
    area = np.pi*(tank.diameter)**2/4 # Tube section
    gasDensity = tank.pressure/(tank.interface.upstreamSubstance.gasConstant*temperature) # Ideal gas
    w0 = massFlowIn/(area*gasDensity) # Speed inside of the conduit. Continuity equation
    
    fD = 0.0 # Friction with gas assumed negligible
    xi = xiInput(tank.interface.upstreamSubstance,tank,massFlowIn, temperature)
    
    dPIn = (xi + fD*tank.interface.positionInterface/tank.diameter)*gasDensity*w0**2/2
    
    return dPIn

def dPOut(tank: Tank, massFlowOut: float):   
    area = np.pi*(tank.diameter)**2/4 # Tube section
    rho = tank.interface.downstreamSubstance.density # Assumed incompressible
    w1 = massFlowOut/(area*rho) # Speed inside of the conduit. Continuity equation
    
    fD = frictionFactor(tank.interface.downstreamSubstance,tank,massFlowOut)
    xi = xiOutput(tank.interface.downstreamSubstance,tank,massFlowOut)
    
    dPOut = (xi + fD*(tank.length-tank.interface.positionInterface)/tank.diameter)*tank.interface.downstreamSubstance.density*w1**2/2
    
    return dPOut

def dPTot(tank: Tank, massFlowOut: float, temperature: float, pressure: float):
    area = np.pi*(tank.diameter)**2/4 # Tube section
    rho = tank.interface.downstreamSubstance.density # Assumed incompressible
    w0 = massFlowOut/(area*rho) # Speed inside of the conduit. Continuity equation
    
    dPOutput = dPOut(tank,massFlowOut,w0)
    Pin = pressure + dPOutput
    
    massFlowIn = densityInterface(tank, massFlowOut, temperature, pressure)
    dPInput = dPIn(tank,massFlowIn,w0,temperature)
    
    dP = dPInput + dPOutput
    
    return dP