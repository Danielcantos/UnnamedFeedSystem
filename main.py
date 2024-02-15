# SCUBE-AEther feed system calculations program
# Developed by the Feed System Team 2023-24:
# - Daniel Cantos Gálvez (danielcantosgalvez@gmail.com)
# - Hemanth Alapati
# - Louis Urbin
# - Stanislas Le Person
# - Thomas Roberge


# Definition of the system
# - Components
# - Types
# - Nodes

# Native libraries
import numpy as np

# Custom libraries
import valves
import tubes

# Hydraulic chain declaration (empty)
HydraulicChain = []

# HYDRAULIC CHAIN SETUP
# List of components, in order
MV1 = valves.Valve("MV1",True,"Ball","Manual")

# Definition of the chain
HydraulicChain.append(MV1)