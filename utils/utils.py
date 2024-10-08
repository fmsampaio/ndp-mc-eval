from .defines import VVC_constants, Token_offset, MV_TO_FRAC_POS

def get_n_in_2bit_fixed_point(n):
    return n >> 2, ((n >> 1) & 1) *  0.5 + (n & 1) *  0.25

def break_into_integ_n_frac(n):
    return int(n),  n - int(n)

def getFracPosition(vector):
    xMV, yMV = vector

    _ , xFracMV = break_into_integ_n_frac(xMV)
    _ , yFracMV = break_into_integ_n_frac(yMV)

    return MV_TO_FRAC_POS[(abs(xFracMV), abs(yFracMV))]

def loadLines(file_path):
    lines = []
    with open(file_path, 'r') as in_file:
        lines = in_file.readlines()
    return lines

def getMV(entry):
    # print(entry)
    xIntegMV, xFracMV = get_n_in_2bit_fixed_point(int(entry[-2]))
    yIntegMV, yFracMV = get_n_in_2bit_fixed_point(int(entry[-1]))
    
    fracPosition = MV_TO_FRAC_POS[(xFracMV, yFracMV)]
    # print((xIntegMV, yIntegMV, fracPosition))
    return (xIntegMV, yIntegMV, fracPosition) 

def getPredMode(entry):
    return int(entry[-1])

def getRefFrameIdx(entry):
    return int(entry[-1])

def getCTU(entry):
    return ( int(entry[2])//VVC_constants.CTU_size.value,  int(entry[3])//VVC_constants.CTU_size.value )

def getFrameIndex(entry):
    return int(entry[Token_offset.Frame.value])

def getPosX(entry):
    return int(entry[Token_offset.CU_position_x.value])

def getPosY(entry):
    return int(entry[Token_offset.CU_position_y.value])

def getBlockSizeX(entry):
    return int(entry[Token_offset.CU_x_size.value])

def getBlockSizeY(entry):
    return int(entry[Token_offset.CU_y_size.value])

def getLine(entry):
    return int(entry[Token_offset.CU_position_y.value]) // VVC_constants.CTU_size.value

def getAffineAnnotation(entry):
    return 1

def getCtuWindowId(xCU, yCU, frameWidth):
    if frameWidth in [3840, 4096]:
        ctuWindowId = ( (yCU // VVC_constants.CTU_size.value) * 2 ) + ( xCU // (frameWidth // 2) )
    else:
        ctuWindowId = yCU // VVC_constants.CTU_size.value  
    
    return ctuWindowId

def getCtuWindowLimits(ctuWindowId, frameWidth, frameHeight):
    xWindow = ctuWindowId % 2
    yWindow = ctuWindowId // 2

    if frameWidth in [3840, 4096]:
        xLeft = xWindow * (frameWidth // 2)
        xRight = (xWindow + 1) * (frameWidth // 2)
    else:
        xLeft = 0
        xRight = frameWidth
    
    yTop = yWindow * VVC_constants.CTU_size.value
    yBottom = (yWindow + 1) * VVC_constants.CTU_size.value
    if yBottom > frameHeight:
        yBottom = frameHeight
    
    return xLeft, xRight, yTop, yBottom

def getInterpWindowLimits(ctuWindowId, frameWidth, ctuWindowHeight, xOffset, yOffset):
    xWindow = ctuWindowId % 2
    yWindow = ctuWindowId // 2

    xLeft = xOffset
    if frameWidth in [3840, 4096]:
        xLeft += xWindow * (frameWidth // 2)
    else:
        xLeft += 0
    xRight = xLeft + VVC_constants.INTERP_WINDOW_WIDTH.value
    
    yTop = yOffset + (yWindow * VVC_constants.CTU_size.value)
    yBottom = yTop + ctuWindowHeight

    return xLeft, xRight, yTop, yBottom

relevantMetrics = {
    'MVL0'          : getMV, 
    'MVL1'          : getMV, 
    'PredMode'      : getPredMode, 
    'CTU'           : getCTU, 
    'frame'         : getFrameIndex, 
    'xCU'           : getPosX, 
    'yCU'           : getPosY, 
    'wCU'           : getBlockSizeX, 
    'hCU'           : getBlockSizeY, 
    'line'          : getLine, 
    'AffineMVL0'    : getAffineAnnotation, 
    'AffineMVL1'    : getAffineAnnotation,
    'RefIdxL0'      : getRefFrameIdx,
    'RefIdxL1'      : getRefFrameIdx,
}
