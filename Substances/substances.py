class Material:
    def __init__(self,name:str,density:float,yieldStrength:float,youngModulus:float):
        self.name = name
        self.density = density
        self.yieldStrength = yieldStrength
        self.youngModulus = youngModulus
        
        
class Fluid:
    def __init__(self,name:str,density:float,staticViscosity:float):
        self.name = name
        self.density = density
        self.staticViscosity = staticViscosity
        
class Gas:
    def __init__(self,name:str,staticViscosity:float,gasConstant:float):
        self.name = name
        self.staticViscosity = staticViscosity
        self.gasConstant = gasConstant