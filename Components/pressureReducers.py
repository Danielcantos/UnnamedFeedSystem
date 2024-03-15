# AEther 23-24
# Creation: 16/02/2024
# Last edit: 15/03/2024
# It models pressure reducers that contain an incoming flow and deliver a set output pressure no matter it

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

# CLASS AND SUBCLASS DECLARATION
class pressureReducer:
    def __init__(self, name: str, objectivePressure: float):
        self.name = name # Identifier on the PI&D
        self.objectivePressure = objectivePressure # The expected output pressure. May on may not be able to provide it exactly