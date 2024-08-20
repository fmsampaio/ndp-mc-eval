from utils.defines import VVC_constants

class Frame:
    def __init__(self, poc):
        self.poc = poc
        self.ctuLines = {}
    
    def addCuInCTU(self, xCU, yCU, wCU, hCU):
        xCTU = xCU // VVC_constants.CTU_size.value
        yCTU = yCU // VVC_constants.CTU_size.value

        ctuLineId = yCTU

        if ctuLineId not in self.ctuLines:
            self.ctuLines[ctuLineId] = CTULine(ctuLineId)
            
        if (xCTU, yCTU) not in self.ctuLines[ctuLineId].CTUs:
            ctuData = CTU(xCTU, yCTU)
            self.ctuLines[ctuLineId].CTUs[(xCTU, yCTU)] = ctuData
        else:
            ctuData = self.ctuLines[ctuLineId].CTUs[(xCTU, yCTU)]

        cuData = ctuData.addCU(xCU, yCU, wCU, hCU)        
        return cuData
       
    def __str__(self):
        returnable =  f'Frame: POC {self.poc} \n'
        for ctuLineKey in self.ctuLines:
            ctuLineData = self.ctuLines[ctuLineKey]
            returnable += str(ctuLineData)       
        return returnable

class CTULine:
    def __init__(self, ctuLine):
        self.ctuLine = ctuLine
        self.CTUs = {}

    def __str__(self):
        returnable = f'CTU Line: {self.ctuLine} | Num of CTUs {len(self.CTUs)}'
        for ctuKey in self.CTUs:
            ctuData = self.CTUs[ctuKey]
            returnable += str(ctuData)
        return returnable


class CTU:
    def __init__(self, xCTU, yCTU):
        self.xCTU = xCTU
        self.yCTU = yCTU
        self.CUs = {}
    
    def addCU(self, xCU, yCU, wCU, hCU):
        cuKey = (xCU, yCU)
        
        if cuKey not in self.CUs:
            cuData = CU(xCU, yCU, wCU, hCU)
            self.CUs[cuKey] = cuData
        else:
            cuData = self.CUs[cuKey]

        return cuData
    
    
    def __str__(self):
        returnable = f'CTU: ({self.xCTU},{self.yCTU}) Num. of CUs {len(self.CUs)}\n'
        for cuKey in self.CUs:
            cuData = self.CUs[cuKey]
            returnable += str(cuData)
        return returnable

class CU:
    def __init__(self, xCU, yCU, wCU, hCU):
        self.xCU = xCU
        self.yCU = yCU
        self.wCU = wCU
        self.hCU = hCU
        self.motionInfo = { }

    def addMotionInfo(self, refList, refPoc, fullMV, integMV, fracMV):
        refListKey = f'L{refList}'
        self.motionInfo[refListKey] = MotionInfo(refPoc, fullMV, integMV, fracMV)

    def __str__(self):
        returnable = f'CU: ({self.xCU}, {self.yCU}) [{self.wCU}x{self.hCU}]\n'
        for info in self.motionInfo:
            motionInfo = self.motionInfo[info]
            returnable += f'{info} --> {str(motionInfo)}\n'
        return returnable

class MotionInfo:
    def __init__(self, refPoc, fullMV, integMV, fracMV):
        self.refPoc = refPoc
        self.fullMV = fullMV
        self.integMV = integMV
        self.fracMV = fracMV
        
    def isFracMC(self):
        return self.fracPosition != 0

    def __str__(self):
        return f'Ref. {self.refPoc} | Full. {self.fullMV} Integ. {self.integMV} Frac. {self.fracMV}'