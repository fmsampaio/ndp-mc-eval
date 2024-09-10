import matplotlib.patches
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from models.McDecodeData import McDecodeData
from utils.defines import YUV_VIDEOS

from utils.defines import MV_TO_FRAC_POS_QUARTER

X_MARGIN = 64
Y_MARGIN = 64

CTU_LINES_COLORS = []

def readPrefFracs(currFramePoc, mvLog): 
    decoderOptLogFileName = f'/home/felipe/Projetos/ndp-repos/outputs/frac-only/opt-logs-4bits/NDP_{mvLog.video}_{mvLog.config}_{mvLog.qp}.opt.log'
    fp = open(decoderOptLogFileName, 'r')

    returnableDict = {}

    for line in fp.readlines()[1:-1]:
        tokens = line.split(';')
        ctuLineKey = tokens[0]
        framePocLine = int(ctuLineKey.split('_')[0])
        ctuLine = int(ctuLineKey.split('_')[1])
        refList = f'L{ctuLineKey.split("_")[2]}'
        if currFramePoc == framePocLine:    
            prefFrac = int(tokens[2])
            prefFracHit = float(tokens[3])
            returnableDict[(ctuLine, refList)] = (prefFrac, prefFracHit)

    return returnableDict            


def plotScatterChart(currFramePoc, mvLog, onlyFrac=False, targetCtuLine=-1):
    frameData = mvLog.mcData[currFramePoc]
    
    rectangles = { 'L0' : [], 'L1' : [] }
    
    refLists = [0, 1]

    prefFracDict = readPrefFracs(currFramePoc, mvLog)
    
    # alphaStep = 0.8 / len(frameData.ctuLines)

    # iAlpha = 0.0
    for ctuLineId, ctuLineData in frameData.ctuLines.items():
        if targetCtuLine != -1 and ctuLineId != targetCtuLine:
            continue
        for _, ctuData in ctuLineData.CTUs.items():
            for _, cuData in ctuData.CUs.items():
                print(cuData)
                for refList, motionInfo in cuData.motionInfo.items():
                    if refList in cuData.motionInfo:
                        ctuLineKey = (ctuLineId, refList)
                        prefFrac, _ = prefFracDict[ctuLineKey]

                        fracPos = MV_TO_FRAC_POS_QUARTER[motionInfo.fracMV]

                        alpha = 0.4                        
                        if motionInfo.isFracMC():
                            if fracPos == prefFrac:
                                color = 'red'
                                alpha = 0.6  
                            else:
                                color = 'pink'
                        else:
                            color = 'palegreen'

                        if not onlyFrac or motionInfo.isFracMC():
                            rectangles[refList].append(
                                matplotlib.patches.Rectangle (
                                    xy = (cuData.xCU + motionInfo.integMV[0] , cuData.yCU + motionInfo.integMV[1]),
                                    width = cuData.wCU,
                                    height = cuData.hCU,
                                    edgecolor = 'black',
                                    facecolor = color,
                                    alpha = alpha
                                    # alpha = iAlpha + 0.1
                                )
                            )
        # iAlpha += alphaStep

    frameWidth = int(YUV_VIDEOS[mvLog.video]['res'].split('x')[0])
    frameHeight = int(YUV_VIDEOS[mvLog.video]['res'].split('x')[1])

    if targetCtuLine != -1:
        yTopCtuLine = 128 * targetCtuLine
        yBottomCtuLine = yTopCtuLine + 128

    fig = plt.figure()
    
    for refList in refLists:
        ax = fig.add_subplot(1, 2, refList+1)

        if targetCtuLine != -1:
            ax.hlines(yTopCtuLine, xmin=0-X_MARGIN, xmax=frameWidth+X_MARGIN)
            ax.hlines(yBottomCtuLine, xmin=0-X_MARGIN, xmax=frameWidth+X_MARGIN)

        print(len(rectangles[f'L{refList}']))
        for rect in rectangles[f'L{refList}']:
            ax.add_patch(rect)
        
        ax.set_xlim([0 - X_MARGIN, frameWidth + X_MARGIN]) 

        if targetCtuLine != -1:
            ax.set_ylim([yTopCtuLine - Y_MARGIN, yBottomCtuLine + Y_MARGIN])
            # Annotate pref frac hit
            ctuLineKey = (targetCtuLine, f'L{refList}')
            _, prefFracHit = prefFracDict[ctuLineKey]
            note = f'Hit%: {prefFracHit}'
            ax.annotate(note, (0, yBottomCtuLine + Y_MARGIN))
        else:
            ax.set_ylim([0 - Y_MARGIN, frameHeight + Y_MARGIN]) 

        ax.invert_yaxis()
    
    plt.show()
    #plt.savefig('/home/felipe/Projetos/ndp-repos/ndp-tcsvt/outputs/test_rect.pdf', format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    mvLog = McDecodeData(
        mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/baseline/mvlogs-4bits/NDP_CatRobot_LD_22.log.gz', 
        # mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/frac-only/mvlogs-opt-4bits/NDP_CatRobot_LD_22.opt.log.gz', 
        quarterOnly = True,
    )

    plotScatterChart(
        currFramePoc=1, 
        mvLog=mvLog,
        onlyFrac=False,
        targetCtuLine=0
    )



