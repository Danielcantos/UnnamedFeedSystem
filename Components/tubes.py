# AEther 23-24 
# Creation: 15/02/2024
# Last edit: 19/11/2024
# It models conducts be they straight or curved and the pressure losses incurred


# - Tube.py
# - INPUT:
# -- Cf, velocity

# Outputs
# - dP at each node

# Native libraries
import numpy as np
import sys

# Custom libraries
sys.path.insert(0, './Substances')
import fluids
import materials

# CLASS AND SUBCLASS DECLARATION
class Conduit:
    # Only valid for straight tubes
    def __init__(self, name: str, length: float, thickness: float, diameter: float, material: materials.Material):
        '''
        Object used to describe straight tubes.
        - name is the code identifying the piece
        - length is the tube length in m
        - thickness is the wall thickness in m
        - diameter is the internal diameter is m
        - material is a Material object
        '''
        self.name = name # Identifier on the PI&D
        self.length = length # Self explanatory
        self.thickness = thickness # Self explanatory
        self.diameter = diameter # Internal diameter
        self.material = material # Specific object type
    
    def dP(self,node):
        '''
        Returns the correct loss of pressure in Pa based on Darcy-Weisbach
        - node: point on the hydraulic chain in which the conduit is located, and its associated data
        '''
        dP = dPDarcyWeisbach(node.fluid,self,node)
        return dP
    
class Elbow(Conduit) : 
    # For curved tubes
    def __init__(self, name: str, length: float, thickness: float, diameter: float, material: materials.Material, angle:float, radiusCurve:float):
        '''
        Object used to describe curved tube of any angle from 0º to 360º. Normally the angle should be 45º-90º.
        - name is the code identifying the piece
        - length is the tube length in m
        - thickness is the wall thickness in m
        - diameter is the internal diameter is m
        - material is a Material object
        - angle is the angle of rotation of the elbow in deg (90º is a quarter turn)
        - radiusCurve is the radius of curvature of the elbow in m (defined from the center axis of the elbow)
        '''
        super().__init__(name,length,thickness,diameter,material) # We assume that the length is equally distributed at both sides of the bend
        self.angle = angle # Angle of the bend IN DEGREES
        self.radiusCurve = radiusCurve # Not half the diameter, but the radius of the curve the tube makes
        
    def dP(self,node):
        '''
        Returns the correct loss of pressure in Pa based on analytical Reynolds correlations
        - node: point on the hydraulic chain in which the conduit is located, and its associated data
        '''
        dP = dPElbow(node.fluid,self,node)
        return dP
            
class Tee(Conduit):
    # Fot a T connector with 3 sides
    def __init__(self, name: str, length: float, thickness: float, diameter: float, material: materials.Material, direction1:int, direction2:int, direction3:int):
        super().__init__(name,length,thickness,diameter,material) # NOTE: do we need an additional input like the number of connections or an int that marks nodes?
        # The direction are defined as positive going in and negative going out
        # Input numbers defined following the normal orientation of the letter T
        direction1 = +1 
        direction2 = -1
        direction3 = -1

def frictionFactor (fluid: fluids.Liquid, tube: Conduit, massFlow: float):
    '''
    Numerical and simplifie implementation of the Darcy-Weisbach graph. Assumes liquid in this case
    - fluid is the Liquid object 
    - tube is the Conduit object
    - massFlow is the mass flow in kg/s
    '''
    # From Idelchik, adapted by Daniel Cantos Gálvez
    area = np.pi*(tube.diameter)**2/4 # Tube section
    u = massFlow/(area*fluid.density) # Speed inside of the conduit. Continuity equation
    nu = fluid.dynamicViscosity/fluid.density # Kinematic viscosity
    
    Re = u*tube.diameter/nu
  
    if Re < 2300:
        # Laminar flow
        fD = 64/Re
    elif Re < 63000:
        # Nikuradse for smooth pipes (Idelchik)
        fD = 0.3164/Re**0.25     
    else:
        # You should see this
        print("ERROR: high Re regime achieved in tube " + tube.name + " (Re = " + str(Re) + ")")
        fD = 0.3164/Re**0.25   
        
    return fD
        
        
def dPDarcyWeisbach(fluid, tube: Conduit, node):
    '''
    Returns the loss of pressure in Pa based on Darcy-Weisbach. 
    The boundary layer inside of the tube is negliged. 
    The friction coefficient for a gas is an order of magnitude, most of the time friction for a gas is negligible.
    - fluid is either a Liquid or Gas object
    - tube is the Conduit object
    - node is the Node object
    '''
    # Extracted from Idelchik as a first approximation
    massFlow = node.mdot
    area = np.pi*(tube.diameter)**2/4 # Tube section   
    
    if type(fluid) is fluids.Liquid:
        fD = frictionFactor(fluid, tube, massFlow) # Extract friction factor from Darcy-Weisbach graph
        rho = fluid.density # Assumed incompressible
    else: 
        T = node.T
        P = node.P
        r = fluid.gasConstant
        fD = 0.01 # Order of magnitude
        rho = P/(r*T)
    
    w0 = massFlow/(area*rho) # Speed inside of the conduit. Continuity equation
    Dh = tube.diameter # No BL assumption
    
    dP = fD*tube.length/Dh*rho*w0**2/2
    
    return dP

def dPElbow(fluid:fluids.Liquid, elbow:Elbow, node):
    '''
    Returns the loss of pressure in Pa for an elbow conduit. Applicability for both gases and liquids is assumed 
    - fluid is either a Liquid or Gas object
    - elbow is the Elbow object
    - node is the Node object
    '''
    massFlow = node.mdot
    area = np.pi/4*(elbow.diameter)**2 # Tube section
    
    if type(fluid) is fluids.Liquid:
        rho = fluid.density
    else:
        T = node.T
        P = node.P
        r = fluid.gasConstant
        rho = P/(r*T)
        
    u = massFlow/(area*rho) # Speed inside of the conduit. Continuity equation
    nu = fluid.dynamicViscosity/rho # Kinematic viscosity
    Re = u*elbow.diameter/nu
    
    if elbow.radiusCurve/elbow.diameter < 3: # Abrupt curve
        # Despite it only being valid for Re > 2e5 we'll use it for all cases
        lamb = 1/(1.8*np.log(Re)-1.64)**2
        xi = 1.58*lamb*elbow.radiusCurve/elbow.diameter + 1.19

    else: # Smooth curve
        if Re*np.sqrt(elbow.diameter/(2*elbow.radiusCurve)) < 600:
            lamb = 20/(Re**0.65)*(elbow.diameter/(2*2*elbow.radiusCurve))**(0.175)
        
        elif Re*np.sqrt(elbow.diameter/(2*elbow.radiusCurve)) < 1400:
            lamb = 10.4/(Re**0.55)*(elbow.diameter/(2*2*elbow.radiusCurve))**(0.225)
        
        elif Re*np.sqrt(elbow.diameter/(2*elbow.radiusCurve)) < 5000:
            lamb = 5/(Re**0.45)*(elbow.diameter/(2*2*elbow.radiusCurve))**(0.275)
        else:
            print("ERROR: high Re regime achieved in bend " + elbow.name + " (Re = " + str(Re) + ")")
            lamb = 0.05 # Worst case scenario from diagram 6.2
            
        xi = 0.0175*lamb*elbow.angle*elbow.radiusCurve/elbow.diameter


    dP = 1/2 * rho * u**2 * xi
    
    return dP

#def dPTee(fluid:fluids.Liquid,tee:Tee,massFlow:float):