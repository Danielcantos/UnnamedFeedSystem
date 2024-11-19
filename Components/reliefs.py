# AEther 23-24
# Creation: 16/02/2024
# Last edit: 19/11/2024
# Any and all relief mechanisms

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import materials

class Relief:
    def __init__(self, name: str, state: bool, burstPressure: float):
        '''
        Defines any relief device (relief valve, burst disk...) installed on the line. 
        Triggers if the pressure limit is surpassed.
        - name is the code identifying the piece 
        - state is a boolean defining untriggered (False) and triggered (True) states. NOTE: unused as of 19/11/2024
        - burstPressure is the design pressure for which it will activate
        '''
        self.name = name # Identifier on the PI&D
        self.state = state
        self.burstPressure = burstPressure # Design pressure for which it will activate
        
    def dP(self,node):
        if node.P >self.burstPressure:
            print("Relief has been triggered")
            self.state = True
            
        dP = 0
        
        return dP