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