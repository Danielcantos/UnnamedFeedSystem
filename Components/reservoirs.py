# AEther 23-24
# Creation: 16/02/2024
# Last edit: 16/02/2024
# Two phase containers where the propellant is kept until forced out via pressurization

class Tank:
    def __init__(self,name:str,pressure:float,volume:float):
        self.name = name
        self.pressure = pressure
        self.volume = volume