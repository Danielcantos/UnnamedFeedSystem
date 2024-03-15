# AEther 23-24
# Creation: 16/02/2024
# Last edit: 15/03/2024
# It models a porous filter than traps undesirable particulate material on the fluid flow

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

# CLASS AND SUBCLASS DECLARATION
class filter:
    def __init__(self, name: str):
        self.name = name # Identifier on the PI&D