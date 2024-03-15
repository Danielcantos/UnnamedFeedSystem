# AEther 23-24
# Creation: 16/02/2024
# Last edit: 15/03/2024
# Two phase containers where the propellant is kept until forced out via pressurization

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import gases
import materials

class Tank:
    def __init__(self, name: str, pressure: float, volume: float):
        self.name = name
        self.pressure = pressure
        self.volume = volume