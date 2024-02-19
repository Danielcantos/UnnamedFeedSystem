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
import filters
import pressureReducers
import sources
import reliefs
import reservoirs

# Objective mass flow
mdot = 0.5 # in kg/s might or might not be reached

# Hydraulic chain declaration (empty)
HydraulicChain = []

# HYDRAULIC CHAIN SETUP
# List of components, in order
R1 = sources.Cylinder("R1",120e5,5e-3)
MV1 = valves.Valve("MV1",True,"Ball","Manual")
C1 = tubes.Conduit("C1",10e-3,3e-3,0.25,"NPT1/4","Test")
PR1 = pressureReducers.pressureReducer("PR1",80e5)
C2 = tubes.Conduit("C2",10e-3,3e-3,0.25,"NPT1/4","Test")
CV1 = valves.checkValve("CV1")
C3 = tubes.Conduit("C3",10e-3,3e-3,0.25,"NPT1/4","Test")
SV1 = valves.Valve("SV1",True,"Ball","Solenoid")
C4 = tubes.Conduit("C4",10e-3,3e-3,0.25,"NPT1/4","Test")
BD1 = reliefs.burstDisk("BD1",100e5)
C5 = tubes.Conduit("C5",10e-3,3e-3,0.25,"NPT1/4","Test")
R2 = reservoirs.Tank("R2",1e5,5e-3)
C6 = tubes.Conduit("C6",10e-3,3e-3,0.25,"NPT1/4","Test")
B1 = tubes.Bend("B1",10e-3,3e-3,0.25,"NPT1/4","Test",90)
C7 = tubes.Conduit("C7",10e-3,3e-3,0.25,"NPT1/4","Test")



# Definition of the chain
HydraulicChain.append(R1)
HydraulicChain.append(MV1)