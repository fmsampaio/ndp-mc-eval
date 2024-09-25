
from models.McDecodeData import McDecodeData
from utils.utils import *
from utils.defines import *
from models.Cycles import Cycles

import pyperclip

def getPrefFracStats(fracCounters):
    prefFrac = -1
    highestOcc = -1

    for i in range(1, 16):
        if fracCounters[i] > highestOcc:
            highestOcc = fracCounters[i]
            prefFrac = i
    
    if sum(fracCounters) == 0:
        return -1, -1

    prefHalfFrac = 2 if fracCounters[2] >= fracCounters[8] else 8

    prefFracHit = float(highestOcc) / sum(fracCounters)
    prefFracHitInterp = float(highestOcc) / (2048*128)

    return prefFrac, prefFracHit, prefFracHitInterp, prefHalfFrac

def calculateInterpWindowStatistics(mcData):
    interpWindowStats = {}
    for framePoc, frameData in mcData.mcData.items():
        for ctuLineId, ctuLineData in frameData.ctuLines.items():
            fracCounters = {'L0' : [0] * 16 , 'L1' : [0] * 16}
            cuSizeAccums = {'L0' : 0, 'L1' : 0}
            cuCounters = {'L0' : 0, 'L1' : 0}
            for _, ctuData in ctuLineData.CTUs.items():
                for _, cuData in ctuData.CUs.items():
                    for refList, motionInfo in cuData.motionInfo.items():
                        fracPos = MV_TO_FRAC_POS_QUARTER[motionInfo.fracMV]
                        if fracPos != 0:
                            cuSize = cuData.wCU * cuData.hCU
                            fracCounters[refList][fracPos] += cuSize
                            cuSizeAccums[refList] += cuSize
                            cuCounters[refList] += 1        

            for refList in ['L0','L1']:
                dictKey = (framePoc, ctuLineId, refList)
                if cuCounters[refList] != 0:
                    prefFrac, prefFracHit, prefFracHitInterp, prefHalfFrac = getPrefFracStats(fracCounters[refList])
                    interpWindowStats[dictKey] = {
                        'cu_size_avg' : float(cuSizeAccums[refList]) / cuCounters[refList],
                        'pref_frac' : prefFrac,
                        'pref_half_frac' : prefHalfFrac,
                        'pref_frac_hit' : prefFracHit,
                        'pref_frac_hit_interp' : prefFracHitInterp,
                    }
                else:
                    interpWindowStats[dictKey] = {
                        'cu_size_avg' : -1,
                        'pref_frac' : -1,
                        'pref_half_frac' : -1,
                        'pref_frac_hit' : -1,
                        'pref_frac_hit_interp' : -1
                    }
    
    return interpWindowStats

def speculativeInterpolationHit(fracPos, prefFrac, prefHalfFrac):
    if fracPos == prefFrac:
        return True
    elif len(FRAC_INTERP_DEPENDENCIES[prefFrac]) > 0:
        if prefFrac in [5, 7, 13, 15]:
            if prefHalfFrac == 8:
                prefFracDependencies = FRAC_INTERP_DEPENDENCIES[prefFrac][0]
            else: # prefHalfFrac == 2:
                prefFracDependencies = FRAC_INTERP_DEPENDENCIES[prefFrac][1]
        else:
            prefFracDependencies = FRAC_INTERP_DEPENDENCIES[prefFrac][0]
        return fracPos in prefFracDependencies
    else:
        return False        

def estimateCycles(mcData, interpWindowStats, cyclesData, countIntegerMC=False):
    print("Counting cycles...")
    
    avxCycles = {}
    vimaCycles = {}
    vimaSpeculativeInterp = {}

    for key in interpWindowStats:
        keyFrameCtuLineOnly = key[:2]
        avxCycles[keyFrameCtuLineOnly] = { 'L0' : 0, 'L1' : 0 }
        vimaCycles[keyFrameCtuLineOnly] = { 'L0' : 0, 'L1' : 0 }
        vimaSpeculativeInterp[keyFrameCtuLineOnly] = { 'L0' : False, 'L1' : False }

    for framePoc, frameData in mcData.mcData.items():
        for ctuLineId, ctuLineData in frameData.ctuLines.items():
            keyFrameCtuLineOnly = (framePoc, ctuLineId)
            for _, ctuData in ctuLineData.CTUs.items():
                for _, cuData in ctuData.CUs.items():
                    cuSize = (cuData.wCU, cuData.hCU)
                    for refList, motionInfo in cuData.motionInfo.items():
                        ctuWindowKey = (framePoc, ctuLineId, refList)

                        prefFrac = interpWindowStats[ctuWindowKey]['pref_frac']
                        prefHalfFrac = interpWindowStats[ctuWindowKey]['pref_half_frac']
                        prefFracHit = interpWindowStats[ctuWindowKey]['pref_frac_hit']
                        prefFracHitInterp = interpWindowStats[ctuWindowKey]['pref_frac_hit_interp']
                        cuSizeAvg = interpWindowStats[ctuWindowKey]['cu_size_avg']

                        fracPos = MV_TO_FRAC_POS_QUARTER[motionInfo.fracMV]

                        vimaSpeculativeInterp[keyFrameCtuLineOnly][refList] = True  # feat: evaluate interp window statistics to define speculativeInterp

                        if motionInfo.isFracMC():
                            avxCycles[keyFrameCtuLineOnly][refList] += cyclesData.get_cycles(cuSize, fracPos, ISA.AVX2)

                            # if fracPos != prefFrac:
                            if not speculativeInterpolationHit(fracPos, prefFrac, prefHalfFrac):
                                vimaCycles[keyFrameCtuLineOnly][refList] += cyclesData.get_cycles(cuSize, fracPos, ISA.AVX2)
                        
                        elif countIntegerMC:
                            avxCycles[keyFrameCtuLineOnly][refList] += cyclesData.get_cycles(cuSize, fracPos, ISA.AVX2)
                            vimaCycles[keyFrameCtuLineOnly][refList] += cyclesData.get_cycles(cuSize, fracPos, ISA.AVX2)
    
    for key in vimaCycles.keys():
        for refList in ['L0', 'L1']:
            ctuWindowKey = key + (refList, )
            prefFrac = interpWindowStats[ctuWindowKey]['pref_frac']
            if vimaSpeculativeInterp[key] and prefFrac != -1:
                vimaCycles[key][refList] += cyclesData.get_cycles((2048, 128), prefFrac, ISA.VIMA)
    
    return avxCycles, vimaCycles

def reportCyclesEstimation(avxCycles, vimaCycles, interpWindowStats):
    output = ''
    for ctuWindowKey in interpWindowStats:
        key = ctuWindowKey[:2]
        refList = ctuWindowKey[2]
        avx = avxCycles[key][refList]
        vima = vimaCycles[key][refList]

        prefFracHit = interpWindowStats[ctuWindowKey]['pref_frac_hit']
        prefFracHitInterp = interpWindowStats[ctuWindowKey]['pref_frac_hit_interp']
        cuSizeAvg = interpWindowStats[ctuWindowKey]['cu_size_avg']

        output += f'{key[0]};{key[1]};{refList};{"{:.3f}".format(prefFracHit)};{"{:.3f}".format(prefFracHitInterp)};{int(cuSizeAvg)};{avx};{vima}\n'
    return output


def main():
    mcData = McDecodeData(
        mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/baseline/mvlogs-4bits/NDP_Netflix_PierSeaside_LD_22.log.gz', 
        #mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/frac-only/mvlogs-opt-4bits/NDP_CatRobot_LD_37.opt.log.gz', 
        quarterOnly = True,
    )
    cyclesData = Cycles('/home/felipe/Projetos/ndp-repos/ndp-tcsvt/inputs/kernels.csv')

    interpWindowStats = calculateInterpWindowStatistics(mcData)

    avxCycles, vimaCycles = estimateCycles(mcData, interpWindowStats, cyclesData)
    
    report = reportCyclesEstimation(avxCycles, vimaCycles, interpWindowStats)

    pyperclip.copy(report)
    # print(report)
    # print(cyclesData.unsupportedBlockSizes)
    
    

if __name__ == '__main__':
    main()