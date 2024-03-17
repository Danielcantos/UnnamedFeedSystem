# AEther 23-24 
# Creation: 15/02/2024
# Last edit: 04/03/2024
# It models conducts be they straight or curved and the pressure losses incurred


# - Tube.py
# - INPUT:
# -- Cf, velocity

# Outputs
# - dP at each node

# CLASS AND SUBCLASS DECLARATION
class Conduit:
    # Only valid for straight tubes
    def __init__(self,name:str,length:float,thickness:float,diameter:float,material):
        self.name = name # Identifier on the PI&D
        self.length = length # Self explanatory
        self.thickness = thickness # Self explanatory
        self.diameter = diameter # Internal diameter
        self.material = material # Specific object type
        self.fluid_velocity #velocity of the incoming fluid
        
class Bend(Conduit):
    # For curved tubes
    def __init__(self,name:str,length:float,thickness:float,diameter:float,material,angle:float):
        super().__init__(name,length,thickness,diameter,material) # We assume that the length is equally distributed at both sides of the bend
        self.angle = angle # Self explanatory
        
class Tee(Conduit):
    # Fot a T connector with 3 sides
    def __init__(self,name:str,length:float,thickness:float,diameter:float,material):
        super().__init__(name,length,thickness,diameter,material) # NOTE: do we need an additional input like the number of connections or an int that marks nodes?


# Pressure drop
def dp_conduit(conduit:Conduit, fluid: fluids.Fluid, material:conduit.material):
        
    Re = fluid.density * conduit.fluid_velocity * conduit.diameter / fluid.viscosity
    f_D = moody(Re, material.roughness / conduit.diameter)                                  # need an implementation of the Moody graph
    dp = f_D * conduit.length / conduit.diameter * 1/2 * fluid.density * fluid_velocity**2
    
    return dp

def dp_bend(conduit:Conduit, fluid: fluids.Fluid, material:conduit.material):
        
    
    return dp

def dp_tee(conduit:Conduit, fluid: fluids.Fluid, material:conduit.material):
        
   
    
    return dp
