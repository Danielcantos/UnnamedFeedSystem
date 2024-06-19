# SCUBE - AEther feed system calculator program
# Developed by the Feed System Team 2023-24:
# - Daniel Cantos Gálvez (danielcantosgalvez@gmail.com)
# - Hemanth Alapati
# - Louis Urbin
# - Stanislas Le Person
# - Thomas Roberge

# Last edit: 19/06/2024 

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
import gases
import materials

# ---------------------------------------
# MAIN CLASSES 
# ---------------------------------------
class Node:
    def __init__(self, P:float, mdot:float, substance, T:float):
        self.P = P
        self.mdot = mdot
        self.substance = substance
        self.T = T
        
# ---------------------------------------
# MAIN HELPER FUNCTIONS
# ---------------------------------------

def dPGetter(component, node: Node):
    dP = 0
    match type(component):
        case tubes.Conduit:
            if type(node.substance) is fluids.Fluid: # It's a liquid
                dP = tubes.dPDarcyWeisbach(node.substance,component,node.mdot)
            else: # It's a gas
                dP = 0        
        case tubes.Bend:
            if type(node.substance) is fluids.Fluid: # It's a liquid
                dP = tubes.dPBend(node.substance,component,node.mdot)
            else: # It's a gas
                dP = 0
        case valves.Valve:
            if type(node.substance) is fluids.Fluid: # It's a liquid
                S = np.pi/4*component.diameter**2
                v  = node.mdot/(S*node.substance.density)
                match component.type.lower():
                    case "ball":
                        dP = valves.dPBallValve(node.substance,component,0.0,v)
                    case "butterfly":
                        dP = valves.dPButterflyValve(node.substance,component,0.0,v)
                    case "gate":
                        dP = valves.dPGateValve(node.substance,component,component.diameter,v)
                    case "globe":
                        dP = valves.dPGlobeValve(node.substance,component,v)
                    case _:
                        dP = valves.dPZapataLiquid(node.substance,component,node.mdot)
            else: # It's a gas
                dP = valves.dPZapataGas(node.substance,component,node.mdot,node.T,node.P)
                
        case valves.CheckValve:
            if type(node.substance) is fluids.Fluid: # It's a liquid
                S = np.pi/4*component.diameter**2
                v  = node.mdot/(S*node.substance.density)
                dP = valves.dPCheckValve(node.substance,component,v)
            else: # It's a gas
                dP = valves.dPZapataGas(node.substance,component,node.mdot,node.T,node.P)
        
        case reliefs.BurstDisk:
            if node.P > component.burstPressure:
                print("Burst disk has been triggered")
                
            dP = 0
            
        case injectors.Injector:
            if type(node.substance) is fluids.Fluid: # It's a liquid
                dP = injectors.dP(node.substance,component,node.mdot)
            else: # It's a gas
                print("Why are you injecting a gas?")
            
        #case reservoirs.Tank:
        #    print("a")
        #case pressureReducers.PressureReducer:
        #    print("a")
        
        case _: 
            print("Error")
    
    return dP      
    #if type(component) is tubes.Conduit:
        

# ---------------------------------------
# PROGRAM
# ---------------------------------------

# Ambient properties
Tamb = 293 # in K

# Fluids and materials used
Aluminium = materials.Material("Aluminium",2100,150e6,70e9, 0.1e-6)
Steel = materials.Material("Steel",7800,550e6,210e9, 0.25e-6)
Water = fluids.Fluid("Water",1000,8.9e-4)
NitrogenLiquid = fluids.Fluid("NitrogenLiquid",806.1,17.81e-6) # Air Liquide (kg/m3), 
Nitrogen = gases.Gas("Nitrogen",17.5e-6,296.8)
HydrogenPeroxide = fluids.Fluid("H2O2",1369.6,1.24e-3) # Overleaf regression (kg/m3), 


print("--------------------------------------------")
print("AEther feed system calculator program")
print("--------------------------------------------")

# -------------------------------------------------------
# SIMULATION SETUP (INPUT)
# -------------------------------------------------------

# Objective mass flow
mdot = 0.2 # in kg/s
inputPressure = 1e5 # in Pa, defined at the exit of the injector

# -------------------------------------------------------
# HYDRAULIC CHAIN SETUP (INPUT)
# -------------------------------------------------------

# Hydraulic chain declaration (empty)
HydraulicChain = []

# List of components, in order
R1 = sources.Cylinder("R1",120e5,5e-3)
MV1 = valves.Valve("MV1",True,"Ball","Manual",0.064)
C1 = tubes.Conduit("C1",0.1,0.003,0.064,Aluminium) # 10 cm tube, 3 mm thick, 1/4" diam NOTE: placeholder
PR1 = pressureReducers.PressureReducer("PR1",[pressureReducers.PressureCurve(400e5,np.array([0,1]), [120e5, 120e5])])
PR1.addPressureCurve(pressureReducers.PressureCurve(1e5,np.array([0,1]), [1e5, 1e5]))
C2 = tubes.Conduit("C2",0.1,0.003,0.064,Aluminium)
CV1 = valves.CheckValve("CV1",True,"Ball","Manual",0.064)
C3 = tubes.Conduit("C3",0.1,0.003,0.064,Aluminium)
SV1 = valves.Valve("SV1",True,"Ball","Solenoid",0.064)
C4 = tubes.Conduit("C4",0.1,0.003,0.064,Aluminium)
BD1 = reliefs.BurstDisk("BD1",False,100e5)
C5 = tubes.Conduit("C5",0.1,0.003,0.064,Aluminium)
R2 = reservoirs.Tank("R2",1e5,5e-3, 160e-3, 3e-3, 0.064, 0.064, reservoirs.TankInterface(Nitrogen,Water,0.0))
C6 = tubes.Conduit("C6",0.1,0.003,0.064,Aluminium)
B1 = tubes.Bend("B1",0.1,0.003,0.064,Aluminium,90,0.05)
C7 = tubes.Conduit("C7",0.1,0.003,0.064,Aluminium)
SV2 = valves.Valve("SV2",True,"Ball","Solenoid",0.064)
C8 = tubes.Conduit("C8",0.1,0.003,0.064,Aluminium)
MV4 = valves.Valve("MV4",True,"Ball","Manual",0.064)
C9 = tubes.Conduit("C9",0.1,0.003,0.064,Aluminium)
I1 = injectors.Injector("I1",0.3433,0.4067,Steel)

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
            dP = dPGetter(HydraulicChain[-1-i],NodeChain[i])
            print(component.name + " dP = " + str(dP) + " Pa")
            NextNode.P += dP
            NodeChain.append(NextNode)
       
    if i == 18:
        print("Pressurizer mass flow: " + str(NextNode.mdot))
        break