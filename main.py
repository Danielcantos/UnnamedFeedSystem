# SCUBE-AEther feed system calculations program
# Developed by the Feed System Team 2023-24:
# - Daniel Cantos Gálvez (danielcantosgalvez@gmail.com)
# - Hemanth Alapati
# - Louis Urbin
# - Stanislas Le Person
# - Thomas Roberge


#####Constants#####


nu_N2 =   #visco N2

nu_H2O2 =     #visco H202

q0 = 

rho = 

V = 

f_N2 = 64/Re_N2  #approx for Re<2000

f_H2O2 = 64/Re_H2O2

#####System definition#####

systeme = ["add system components (with parameters)  here from right to left"]  #Are the operations commutative? if yes, if so, we don't care about ordering the list 

## exemple : systeme = [[pipe,L,D],[singular,kv],[singular,kv], [pipe,L,D]]
## singular regroup valve, filter.... 
##We need to know if it's N2 or H2O2 in the conponent->add a bool 