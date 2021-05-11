#Natalie Schoen
#Quiz 1
#GEOG:5055
#Februrary 5th, 2020

#inputs:
#climate = string
#temperature measurements = list of floats

#outputs:
#folded = "F"
#unfolded = "U"

#rules:
#temperature = "<=" = folded 
#tropical = 30
#continental = 25
#other = 18

def thermMovement(climate, temperature):
    #create threshold value
    Tropical = 30
    Continental = 25
    Other = 18
    
    if climate == 'Tropical':
        for value in temperature:
            if value <= Tropical:
                print('F')
            else:
                print('U')
        
    elif climate == 'Continental':
        for value in temperature:
            if value <= Continental:
                print('F')
            else:
                print('U')
                
    else:
        for value in temperature:
            if value <= Other:
                print('F')
            else:
                print('U')