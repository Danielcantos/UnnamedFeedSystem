# AEther 23-24 
# Creation: 15/02/2024
# Last edit: 16/02/2024
# It models conducts be they straight or curved and the pressure losses incurred


# - Tube.py
# - INPUT:
# -- Cf, velocity

# Outputs
# - dP at each node

# CLASS AND SUBCLASS DECLARATION
class Conduit:
    # Only valid for straight tubes
    def __init__(self,name:str,length:float,thickness:float,diameter:float,thread:str,material):
        self.name = name # Identifier on the PI&D
        self.length = length # Self explanatory
        self.thickness = thickness # Self explanatory
        self.diameter = diameter # Internal diameter
        self.thread = thread # Thread standard --> NOTE: how do we control multiple?
        self.material = material # Specific object type
        
        
class Bend(Conduit):
    # For curved tubes
    def __init__(self,name:str,length:float,thickness:float,diameter:float,thread:str,material,angle:float):
        super().__init__ # We assume that the length is equally distributed at both sides of the bend
        self.angle = angle # Self explanatory
        
class Tee(Conduit):
    # Fot a T connector with 3 sides
    def __init__(self,name:str,length:float,thickness:float,diameter:float,thread:str,material):
        super().__init__ # NOTE: do we need an additional input like the number of connections or an int that marks nodes?
