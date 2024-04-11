# AEther 23-24
# Creation: 28/02/2024
# Last edit: 21/03/2024
# Models solids and equations related to liquids

class Material:
    def __init__(self,name:str,density:float,yieldStrength:float,youngModulus:float,roughness:float):
        self.name = name
        self.density = density
        self.yieldStrength = yieldStrength
        self.youngModulus = youngModulus