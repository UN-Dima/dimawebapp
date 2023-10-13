import math

def nan_2_zero(x):
    if math.isnan(x):
        return 0
    return x