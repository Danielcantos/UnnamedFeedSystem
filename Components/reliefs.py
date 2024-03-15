# AEther 23-24
# Creation: 16/02/2024
# Last edit: 15/03/2024
# Any and all relief mechanisms

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

class burstDisk:
    def __init__(self, name: str, state: bool, burstPressure: float):
        self.name = name # Identifier on the PI&D
        self.state = state
        self.burstPressure = burstPressure # Design pressure for which it will activate