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
# MAIN HELPER FUNCTIONS
# ---------------------------------------

# def dPGetter(component, node: Node):
#     dP = 0
#     match type(component):
#         case tubes.Conduit:
#             if type(node.fluid) is fluids.Liquid: # It's a liquid
#                 dP = tubes.dPDarcyWeisbach(node.fluid,component,node)
#             else: # It's a gas
#                 dP = 0   
                     
#         case tubes.Elbow:
#             if type(node.fluid) is fluids.Liquid: # It's a liquid
#                 dP = tubes.dPElbow(node.fluid,component,node)
#             else: # It's a gas
#                 dP = 0
    
#         case valves.Valve:
#             if type(node.fluid) is fluids.Liquid: # It's a liquid
#                 S = np.pi/4*component.diameter**2
#                 v  = node.mdot/(S*node.fluid.density)
#                 if component.coefficient > 0: # There is a defined coefficient
#                         dP = valves.dPKvLiquid(node.fluid,component,node.mdot)
#                 else:
#                     match component.type.lower():
#                         case "ball":
#                             dP = valves.dPBallValve(node.fluid,component,0.0,v)
#                         case "butterfly":
#                             dP = valves.dPButterflyValve(node.fluid,component,0.0,v)
#                         case "gate":
#                             dP = valves.dPGateValve(node.fluid,component,component.diameter,v)
#                         case "globe":
#                             dP = valves.dPGlobeValve(node.fluid,component,v)
#                         case _:
#                             dP = valves.dPZapataLiquid(node.fluid,component,node.mdot)
#             else: # It's a gas
#                 if component.coefficient > 0: # There is a defined coefficient
#                     dP = valves.dPKvGas(node.fluid,component,node.mdot,node.T,node.P)
#                 else:
#                     dP = valves.dPZapataGas(node.fluid,component,node.mdot,node.T,node.P)
                
#         case valves.CheckValve:
#             if type(node.fluid) is fluids.Liquid: # It's a liquid
#                 S = np.pi/4*component.diameter**2
#                 v  = node.mdot/(S*node.fluid.density)
#                 dP = valves.dPCheckValve(node.fluid,component,v)
#             else: # It's a gas
#                 dP = valves.dPZapataGas(node.fluid,component,node.mdot,node.T,node.P)
        
#         case reliefs.Relief:
#             if node.P > component.burstPressure:
#                 print("Relief has been triggered")
                
#             dP = 0
            
#         case injectors.Injector:
#             if type(node.fluid) is fluids.Liquid: # It's a liquid
#                 dP = injectors.dP(node.fluid,component,node)
#             else: # It's a gas
#                 print("Why are you injecting a gas?")
            
#         case _: 
#             print("Error")
    
#     return dP      
        
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
mdot = 0.378 # in kg/s
inputPressure = 1e5 # in Pa, defined at the exit of the injector

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

NodeChain = [] # From the injector upstream

NodeChain.append(Node(inputPressure,mdot,Water,Tamb))

dt = 0.1 # NOTE: placeholder, only used for interface update

for i, component in enumerate(reversed(HydraulicChain)):
    print("Current pressure = " + str(NodeChain[i].P) + " Pa")
    NextNode = NodeChain[i] # NOTE: will need to do i+1 if we put a node inside chamber
    
    match type(component): # To handle all component not strictly linked to a single dP
        case reservoirs.Tank:
            dPo = reservoirs.dPOut(component,NodeChain[i].mdot)
            print("Outlet " + component.name + " dP = " + str(dPo) + " Pa")
            
            # Managing the tank component
            component.pressure = NextNode.P + dPo # Intermediate tank pressure inside of the tank class
            reservoirs.updateInterface(component,NextNode.mdot,dt) # Propellant is drained from the tank
             
            # Change of substance >> Change of mass flow
            NextNode.mdot = reservoirs.densityInterface(component,NodeChain[i].mdot,NodeChain[i].T,component.pressure)
            NextNode.fluid = component.interface.upstreamSubstance
            
            dPi = reservoirs.dPIn(component,NextNode.mdot,NextNode.T)
            print("Inlet " + component.name + " dP = " + str(dPi) + " Pa")
            
            NextNode.P += dPo + dPi
            
            NodeChain.append(NextNode)
            
        case pressureReducers.PressureReducer:
            Pin = pressureReducers.interpolatePressure(component,NodeChain[i].P,NodeChain[i].mdot)
            NextNode.P = Pin
            print(component.name + " input pressure = " + str(Pin) + " Pa")
            NodeChain.append(NextNode)
        
        case _:
            dP =  component.dP(NodeChain[i])
            print(component.name + " dP = " + str(dP) + " Pa")
            NextNode.P += dP
            NodeChain.append(NextNode)          
        
       
    if i == len(HydraulicChain)-2: # Not counting the cylinder and the additional node of the reservoir
        print("Pressurizer mass flow: " + str(NextNode.mdot))
        break