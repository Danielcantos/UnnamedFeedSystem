# AEther 23-24
# Creation: 16/02/2024
# Last edit: 16/02/2024
# Any and all relief mechanisms

class burstDisk:
    def __init__(self,name:str,burstPressure:float):
        self.name = name # Identifier on the PI&D
        self.burstPressure = burstPressure # Design pressure for which it will activate