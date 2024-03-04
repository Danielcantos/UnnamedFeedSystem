# AEther 23-24
# Creation: 16/02/2024
# Last edit: 04/03/2024
# Any and all relief mechanisms

class burstDisk:
    def __init__(self,name:str,state:bool,burstPressure:float):
        self.name = name # Identifier on the PI&D
        self.state = state
        self.burstPressure = burstPressure # Design pressure for which it will activate