from utils.utils import *

def get_operations( vector):
        operations = []
        vx, vy = vector
        _ , vxFrac = break_into_integ_n_frac(vx)
        _ , vyFrac = break_into_integ_n_frac(vy)

        if vxFrac == 0.0 and vyFrac == 0.0:
            operations.append("I")
        else :
            if vxFrac % 0.5 == 0.0:
                if vxFrac != 0.0:
                    operations.append("H")
            else:
                operations.append("H")
                operations.append("H")

        if vyFrac % 0.5 == 0.0:
            if vyFrac != 0.0:
                operations.append("V")
        else:
            operations.append("V")
            operations.append("V")

        return operations

MVs = {
    0  : (0   , 0   ),
    1  : (0   , 0.25),
    2  : (0   , 0.5 ),
    3  : (0   , 0.75),
    4  : (0.25, 0   ),
    5  : (0.25, 0.25),
    6  : (0.25, 0.5 ),
    7  : (0.25, 0.75),
    8  : (0.5 , 0   ),
    9  : (0.5 , 0.25),
    10 : (0.5 , 0.5 ),
    11 : (0.5 , 0.75),
    12 : (0.75, 0   ),
    13 : (0.75, 0.25),
    14 : (0.75, 0.5 ),
    15 : (0.75, 0.75),
}

for pos, mv in MVs.items():
    print(f'{pos} : {get_operations(mv)},')