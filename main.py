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
import matplotlib.pyplot as plt

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
import fluids
import gases
import materials


# Objective mass flow
mdot = 0.5 # in kg/s might or might not be reached

# Ambient properties
Tamb = 293 # in K

# Fluids and materials used
Aluminium = materials.Material("Aluminium",2100,150e6,70e9)
Steel = materials.Material("Steel",7800,550e6,210e9)
Water = fluids.Fluid("Water",1000,8.9e-4)
NitrogenLiquid = fluids.Fluid("NitrogenLiquid",806.1,17.81e-6) # Air Liquide (kg/m3), 
Nitrogen = gases.Gas("Nitrogen",17.5e-6,296.8)
HydrogenPeroxide = fluids.Fluid("H2O2",1369.6,1.24e-3) # Overleaf regression (kg/m3), 


# Hydraulic chain declaration (empty)
HydraulicChain = []

# HYDRAULIC CHAIN SETUP
# List of components, in order
R1 = sources.Cylinder("R1",120e5,5e-3)
MV1 = valves.Valve("MV1",True,"Ball","Manual",0.064)
C1 = tubes.Conduit("C1",0.1,0.003,0.064,Aluminium) # 10 cm tube, 3 mm thick, 1/4" diam NOTE: placeholder
PR1y = np.array([1e5, 1e5])
PR1x = np.array([0.0, 1.0])
PR1 = pressureReducers.pressureReducer("PR1",PR1x,PR1y)
C2 = tubes.Conduit("C2",0.1,0.003,0.064,Aluminium)
CV1 = valves.CheckValve("CV1",True,"Ball","Manual",0.064)
C3 = tubes.Conduit("C3",0.1,0.003,0.064,Aluminium)
SV1 = valves.Valve("SV1",True,"Ball","Solenoid",0.064)
C4 = tubes.Conduit("C4",0.1,0.003,0.064,Aluminium)
BD1 = reliefs.burstDisk("BD1",False,100e5)
C5 = tubes.Conduit("C5",0.1,0.003,0.064,Aluminium)
R2 = reservoirs.Tank("R2",1e5,5e-3)
C6 = tubes.Conduit("C6",0.1,0.003,0.064,Aluminium)
B1 = tubes.Bend("B1",0.1,0.003,0.064,Aluminium,90,0.05)
C7 = tubes.Conduit("C7",0.1,0.003,0.064,Aluminium)
SV2 = valves.Valve("SV2",True,"Ball","Solenoid",0.064)
C8 = tubes.Conduit("C8",0.1,0.003,0.064,Aluminium)
MV4 = valves.Valve("MV4",True,"Ball","Manual",0.064)
C9 = tubes.Conduit("C9",0.1,0.003,0.064,Aluminium)


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
