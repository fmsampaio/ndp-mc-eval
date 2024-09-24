from enum import Enum
from utils.utils import *
from utils.defines import *

import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

class Cycles():

    def __init__(self, characFp):
        self.cycles = { 
            "vima" : {},
            "avx2" : {}
        }

        dfCharac = pd.read_csv(characFp, delimiter=';')
        for idx in dfCharac.index:
            isa = dfCharac["ISA"][idx]
            type = dfCharac["Interpolation Type"][idx]
            size = self.get_label(dfCharac["Width"][idx], dfCharac["Height"][idx])
            cycles = dfCharac["Cycles"][idx]
            if size not in self.cycles[isa]:
                self.cycles[isa][size] = {}
            self.cycles[isa][size][type] = cycles
        
        self.unsupportedBlockSizes = set()
        
                
    def get_label(self, size_x, size_y):
        return str(size_x)+"x"+str(size_y)

    def get_operations(self, fracPos):
        return INTERP_OPERATIONS[fracPos]

    def get_cycles(self, size, vector, isa):
        operations = self.get_operations(vector)
        sizeLabel = self.get_label(*size)

        if sizeLabel not in self.cycles[isa.value]:
            self.unsupportedBlockSizes.add(sizeLabel)
            return 0

        cycles = 0
        for op in operations:
            cycles += self.cycles[isa.value][sizeLabel][op]

        return cycles


if __name__ == '__main__':
    cycObj = Cycles('/home/felipe/Projetos/ndp-repos/ndp-tcsvt/inputs/kernels.csv')
    print(cycObj.get_operations((2.25, 1.75)))
    print(cycObj.get_cycles((64, 64), (2, 4.5), "avx2"))