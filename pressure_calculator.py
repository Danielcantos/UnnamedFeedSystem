# SCUBE-AEther feed system calculations program
# Developed by the Feed System Team 2023-24:
# - Daniel Cantos Gálvez (danielcantosgalvez@gmail.com)
# - Hemanth Alapati
# - Louis Urbin
# - Stanislas Le Person
# - Thomas Roberge


#####Type of pressure losses#####

def pipe_pressure_drop (L,D,f) : #depends on Length, Diameter, coefficient of friction (Moody diagramm) velocity and volumic mass 
    
    v = q0/(pi*D**2/4)
    delta_p = f*rho*L/(2D)*v**2
    
    return delta_p

#rq : v = q0/(pi*D**2/4) en supposant conservation du debit. En effet Mach très faible devant 0,3 -> on peut supposer incompressible : rho=cste.
#f s'obtient soit avec abaque soit vu que notre reynolds vaut environ 1000, on a l'approx : f = 64/Re


def Singular_pressure_drop (kv) : #kv est un coefficient donné par le constructeur de la valve
    
    delta_p = q0**2/kv**2*rho #rho et q0 sont des variables globales
    
    return delta_p

#ici approx fluide(~gaz incompressible), les formules pour les gazs nécessite de connaitre la température tout le long du systeme


#####For the complete system#####

def total_pressure_drop (system):
    
