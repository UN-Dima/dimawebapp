import math

def nan_2_zero(x):
    if type(x) != float:
        if x == 'No Aplica' or x == 'nan':
            return 0
        else:
            return x
    if math.isnan(x):
        return 0
    return x
