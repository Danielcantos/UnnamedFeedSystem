# AEther 23-24 (15/02/2023)
# It models valves no matter type, elements that can be closed or opened and 
# through which a small amount of pressure is lost

# - Valve.py 
# - INPUT:
# -- Pin, coefficient
# -- Pin, geometry, type
# - OUTPUT:
# -- dP

class Valve:
        def __init__(self,name,state: bool,type: str,actuation:str):
                self.name = name # Identifier on the PI&D
                self.state = state # Closed (0) or Opened (1)
                self.type = type # Ball, needle...
                self.actuation = actuation # Manual, solenoid or pneumatic
                
        def open(self):
            self.state = True
            
        def close(self):        
            self.state = False