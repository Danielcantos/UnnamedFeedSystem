# AEther 23-24
# Creation: 28/02/2024
# Last edit: 28/02/2024
# Models gases and equations related to liquids

class Gas:
    def __init__(self,name:str,staticViscosity:float,gasConstant:float):
        self.name = name
        self.staticViscosity = staticViscosity
        self.gasConstant = gasConstant