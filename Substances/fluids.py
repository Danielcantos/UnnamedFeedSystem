# AEther 23-24
# Creation: 28/02/2024
# Last edit: 20/07/2024
# Models all types of materials and fluids

class Liquid:
    def __init__(self,name:str,density:float,dynamicViscosity:float):
        self.name = name
        self.density = density #kg/m**3
        self.dynamicViscosity = dynamicViscosity #Pa.s    
        
class Gas:
    def __init__(self,name:str,dynamicViscosity:float,gasConstant:float):
        self.name = name
        self.dynamicViscosity = dynamicViscosity
        self.gasConstant = gasConstant