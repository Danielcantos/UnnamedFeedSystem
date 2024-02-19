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
import sys

# Custom libraries
sys.path.insert(0, './Components') # Should work with or without .vscode folder
import valves
import tubes
import filters
import pressureReducers
import sources
import reliefs
import reservoirs

sys.path.insert(1, './Substances')
import substances


# Objective mass flow
mdot = 0.5 # in kg/s might or might not be reached

# Fluids and materials used
Aluminium = substances.Material("Aluminium",2100,150e6,70e9)
Steel = substances.Material("Steel",7800,550e6,210e9)
Water = substances.Fluid("Water",1000,8.9e-4)
Nitrogen = substances.Gas("Nitrogen",17.5e-6,296.8)

# Hydraulic chain declaration (empty)
HydraulicChain = []

# HYDRAULIC CHAIN SETUP
# List of components, in order
R1 = sources.Cylinder("R1",120e5,5e-3)
MV1 = valves.Valve("MV1",True,"Ball","Manual")
C1 = tubes.Conduit("C1",10e-3,3e-3,0.25,"Test")
PR1 = pressureReducers.pressureReducer("PR1",80e5)
C2 = tubes.Conduit("C2",10e-3,3e-3,0.25,"Test")
CV1 = valves.checkValve("CV1")
C3 = tubes.Conduit("C3",10e-3,3e-3,0.25,"Test")
SV1 = valves.Valve("SV1",True,"Ball","Solenoid")
C4 = tubes.Conduit("C4",10e-3,3e-3,0.25,"Test")
BD1 = reliefs.burstDisk("BD1",100e5)
C5 = tubes.Conduit("C5",10e-3,3e-3,0.25,"Test")
R2 = reservoirs.Tank("R2",1e5,5e-3)
C6 = tubes.Conduit("C6",10e-3,3e-3,0.25,"Test")
B1 = tubes.Bend("B1",10e-3,3e-3,0.25,"Test",90)
C7 = tubes.Conduit("C7",10e-3,3e-3,0.25,"Test")
SV2 = valves.Valve("SV2",True,"Ball","Solenoid")
C8 = tubes.Conduit("C8",10e-3,3e-3,0.25,"Test")
MV4 = valves.Valve("MV4",True,"Ball","Manual")
C9 = tubes.Conduit("C9",10e-3,3e-3,0.25,"Test")


# Definition of the chain
HydraulicChain.append(R1)
HydraulicChain.append(MV1)
HydraulicChain.append(C1)
HydraulicChain.append(PR1)
HydraulicChain.append(C2)
HydraulicChain.append(CV1)
HydraulicChain.append(C3)
HydraulicChain.append(SV1)
HydraulicChain.append(C4)
HydraulicChain.append(BD1)
HydraulicChain.append(C5)
HydraulicChain.append(R2)
HydraulicChain.append(C6)
HydraulicChain.append(B1)
HydraulicChain.append(C7)
HydraulicChain.append(SV2)
HydraulicChain.append(C8)
HydraulicChain.append(MV4)
HydraulicChain.append(C9)

