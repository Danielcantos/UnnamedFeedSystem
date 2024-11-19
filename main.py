# SCUBE - AEther feed system calculator program
# Feed System Team 2023-24:
# - Daniel Cantos Gálvez (danielcantosgalvez@gmail.com)
# - Hemanth Alapati
# - Louis Urbin
# - Thomas Roberge

# Feed System Team 2024-25:
# - Daniel Cantos Gálvez (danielcantosgalvez@gmail.com)
# - Nikolai Chisholm 

# Last edit: 19/11/2024 

# Definition of the system
# - Components
# - Types
# - Nodes

# Native libraries
import numpy as np
import scipy
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
import injectors

sys.path.insert(1, './Substances')
import fluids
import materials

# ---------------------------------------
# MAIN CLASSES 
# ---------------------------------------
class Node:
    def __init__(self, P:float, mdot:float, fluid, T:float):
        self.P = P
        self.mdot = mdot
        self.fluid = fluid
        self.T = T
        
# ---------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------

def nodeChainExecution(HydraulicChain,dt,inputPressure,mdot,fluid,T,verbose):
    NodeChain = [] # From the injector upstream

    NodeChain.append(Node(inputPressure,mdot,Water,Tamb))

    for i, component in enumerate(reversed(HydraulicChain)):
        if i == 0: 
            print("Injection pressure = " + str(NodeChain[i].P) + " Pa")
        elif verbose: 
            print("Current pressure = " + str(NodeChain[i].P) + " Pa")
        else: pass
    
        NextNode = NodeChain[i] # NOTE: will need to do i+1 if we put a node inside chamber
    
        match type(component): # To handle all component not strictly linked to a single dP
            case reservoirs.Tank:
                dPo = reservoirs.dPOut(component,NodeChain[i].mdot)
                if verbose: print("Outlet " + component.name + " dP = " + str(dPo) + " Pa")
            
                # Managing the tank component
                component.pressure = NextNode.P + dPo # Intermediate tank pressure inside of the tank class
                reservoirs.updateInterface(component,NextNode.mdot,dt) # Propellant is drained from the tank
             
                # Change of substance >> Change of mass flow
                NextNode.mdot = reservoirs.densityInterface(component,NodeChain[i].mdot,NodeChain[i].T,component.pressure)
                NextNode.fluid = component.interface.upstreamSubstance
            
                dPi = reservoirs.dPIn(component,NextNode.mdot,NextNode.T)
                if verbose: print("Inlet " + component.name + " dP = " + str(dPi) + " Pa")
            
                NextNode.P += dPo + dPi
                NodeChain.append(NextNode)
        
            case sources.Cylinder:
                print("Pressurizer pressure: " + str(NextNode.P) + " Pa")
                print("Pressurizer mass flow: " + str(NextNode.mdot) + " kg/s")
                print("----------------------------------------------")
                return NextNode.P, NextNode.mdot
                break
    
            case _:
                dP =  component.dP(NodeChain[i])
                if verbose: print(component.name + " dP = " + str(dP) + " Pa")
                NextNode.P += dP
                NodeChain.append(NextNode)          
    
# ---------------------------------------
# PROGRAM
# ---------------------------------------

# Ambient properties
Tamb = 293 # in K

# Fluids and materials used
Aluminium = materials.Material("Aluminium",2100,150e6,70e9, 0.1e-6)
Steel = materials.Material("Steel",7800,550e6,210e9, 0.25e-6)
Water = fluids.Liquid("Water",1000,8.9e-4)
NitrogenLiquid = fluids.Liquid("NitrogenLiquid",806.1,17.81e-6) # Air Liquide (kg/m3), 
Nitrogen = fluids.Gas("Nitrogen",17.5e-6,296.8)
Air = fluids.Gas("Air",1.81e-5,287)
HydrogenPeroxide = fluids.Liquid("H2O2",1369.6,1.24e-3) # Overleaf regression (kg/m3), 


print("--------------------------------------------")
print("AEther feed system calculator program")
print("--------------------------------------------")

# -------------------------------------------------------
# SIMULATION SETUP (INPUT)
# -------------------------------------------------------

# Objective mass flow
mode = 2
mdot = 0.378 # in kg/s
inputPressure = 1e5 # in Pa, defined at the exit of the injector
pressurizerPressure = 100e5

# -------------------------------------------------------
# HYDRAULIC CHAIN SETUP (INPUT)
# -------------------------------------------------------

# Hydraulic chain declaration (empty)
HydraulicChain = []

# List of components, in order
R1 = sources.Cylinder("R1",15e5,5e-3)
C1 = tubes.Conduit("C1",91e-3,3e-3,16e-3,Aluminium) 
PR1 = pressureReducers.PressureReducer("PR1",[pressureReducers.PressureCurve(400e5,np.array([0,1]), [120e5, 120e5])])
PR1.addPressureCurve(pressureReducers.PressureCurve(1e5,np.array([0,1]), [1e5, 1e5]))
C2 = tubes.Conduit("C2",62e-3,3e-3,5e-3,Aluminium)
SV1 = valves.Valve("SV1",True,"Solenoid","Electrical",64e-3,0.15)
C3 = tubes.Elbow("C3",0.752,3e-3,10e-3,Aluminium,90,0.479)
R2 = reservoirs.Tank("R2",1e5,5e-3, 160e-3, 3e-3, 0.064, 0.064, reservoirs.TankInterface(Air,Water,0.0))
C4 = tubes.Conduit("C4",79e-3,3e-3,6e-3,Aluminium)
SV2 = valves.Valve("SV2",True,"Solenoid","Electrical",64e-3,0.50)
MV1 = valves.Valve("MV1",True,"Ball","Manual",4e-3,-1)
C5 = tubes.Conduit("C5",11e-3,3e-3,7e-3,Aluminium)
C6 = tubes.Elbow("C6",40e-3,3e-3,4e-3,Aluminium,90,25e-3)
C7 = tubes.Conduit("C7",0.15,5e-3,16e-3,Aluminium)
I1 = injectors.Injector("I1",0.2269,0.4459,Steel)
     
# Coldflow campaign summer 2024
test = 11

HydraulicChain.append(R1)
HydraulicChain.append(C1)
HydraulicChain.append(PR1)
HydraulicChain.append(C2)
HydraulicChain.append(SV1)
HydraulicChain.append(C3)
HydraulicChain.append(R2)
HydraulicChain.append(C4)
if test == 10:
    HydraulicChain.append(SV2)
    HydraulicChain.append(C5)
else:
    HydraulicChain.append(MV1)
    HydraulicChain.append(C6)
    HydraulicChain.append(C7)
    
HydraulicChain.append(I1)

# -------------------------------------------------------
# NODE CHAIN EXECUTION
# -------------------------------------------------------

verbose = True
dt = 0.1 # NOTE: placeholder, only used for interface update
if mode == 1: # We know the downstream (injection and mass flow)
    Ppres, mdotPres =  nodeChainExecution(HydraulicChain,dt,inputPressure,mdot,Water,Tamb,verbose)
else: # We know injection and pressurizer properties 
    out = False
    mdot = 0.1
    eps = 5
    while not out: 
        Ppres, mdotPres =  nodeChainExecution(HydraulicChain,dt,inputPressure,mdot,Water,Tamb,False)
        if np.abs((Ppres - pressurizerPressure)/pressurizerPressure)*100 > eps and Ppres < pressurizerPressure:
            mdot = mdot + 0.01
        elif np.abs((Ppres - pressurizerPressure)/pressurizerPressure)*100 > eps and Ppres > pressurizerPressure: 
            mdot = mdot - 0.01
        else:
            print("Convergence achieved for mdot = " + str(mdot) + " kg/s")
            out = True