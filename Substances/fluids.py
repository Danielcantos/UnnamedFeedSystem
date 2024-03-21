# AEther 23-24
# Creation: 28/02/2024
# Last edit: 21/03/2024
# Models liquids and equations related to liquids

class Fluid:
    def __init__(self,name:str,density:float,staticViscosity:float):
        self.name = name
        self.density = density #kg/m**3
        self.staticViscosity = staticViscosity #Pa.s    