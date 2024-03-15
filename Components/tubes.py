# AEther 23-24 
# Creation: 15/02/2024
# Last edit: 15/03/2024
# It models conducts be they straight or curved and the pressure losses incurred


# - Tube.py
# - INPUT:
# -- Cf, velocity

# Outputs
# - dP at each node

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

# CLASS AND SUBCLASS DECLARATION
class Conduit:
    # Only valid for straight tubes
    def __init__(self, name: str, length: float, thickness: float, diameter: float, material: materials.Material):
        self.name = name # Identifier on the PI&D
        self.length = length # Self explanatory
        self.thickness = thickness # Self explanatory
        self.diameter = diameter # Internal diameter
        self.material = material # Specific object type
             
class Bend(Conduit):
    # For curved tubes
    def __init__(self, name: str, length: float, thickness: float, diameter: float, material: materials.Material, angle: float):
        super().__init__(name,length,thickness,diameter,material) # We assume that the length is equally distributed at both sides of the bend
        self.angle = angle # Self explanatory
        
class Tee(Conduit):
    # Fot a T connector with 3 sides
    def __init__(self, name: str, length: float, thickness: float, diameter: float, material: materials.Material):
        super().__init__(name,length,thickness,diameter,material) # NOTE: do we need an additional input like the number of connections or an int that marks nodes?


def frictionFactor (fluid: fluids.Fluid, tube: Conduit, massFlow: float):
    # Numerical and simplified implementation of the Darcy-Weisbach graph
    
    area = np.pi*(tube.diameter)**2/4 # Tube section
    u = massFlow/(area*fluid.density) # Speed inside of the conduit. Continuity equation
    nu = fluid.staticViscosity/fluid.density # Kinematic viscosity
    
    Re = u*tube.diameter/nu
    
    print("Reynolds regime: " + str(Re))
    if Re < 2300:
        # Laminar flow
        fD = 64/Re
    elif Re < 63000:
        # Nikuradse for smooth pipes (Idelchik)
        fD = 0.3164/Re**0.25     
    else:
        # You should see this
        print("ERROR: high Re regime achieved in " + tube.name + " (Re = " + str(Re) + ")")
        fD = 10
        
    return fD
        
        
def dPDarcyWeisbach(fluid: fluids.Fluid, tube: Conduit, massFlow: float):
    # Extracted from Idelchik as a first approximation
    # - Will only work for liquids
    # - Boundary layer inside tube is negliged. NOTE: this might be too much
    
    fD = frictionFactor(fluid, tube, massFlow) # Extract friction factor from Darcy-Weisbach graph
    
    area = np.pi*(tube.diameter)**2/4 # Tube section
    rho = fluid.density # Assumed incompressible
    w0 = massFlow/(area*fluid.density) # Speed inside of the conduit. Continuity equation
    Dh = tube.diameter # No BL assumption
    
    dP = fD*tube.length/Dh*rho*w0**2/2
    
    return dP

