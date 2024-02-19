# AEther 23-24
# Creation: 16/02/2024
# Last edit: 16/02/2024
# It models pressure sources such as cylinders that act as mass and pressure providers

# CLASS AND SUBCLASS DECLARATION
class Cylinder:
    def __init__(self,name:str,pressure:float,volume:float):
        self.name = name # Identifier on the PI&D
        self.pressure = pressure # Pressure, will depend on time and mass will be a result
        self.volume = volume # Internal volume
        