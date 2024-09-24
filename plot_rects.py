import matplotlib.patches
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from models.McDecodeData import McDecodeData
from utils.defines import YUV_VIDEOS, MV_TO_FRAC_POS_QUARTER

from utils.utils import getCtuWindowLimits, getInterpWindowLimits

X_MARGIN = 64
Y_MARGIN = 64

X_WINDOW_MARGIN = 0.05
Y_WINDOW_MARGIN = 0.2

CTU_LINES_COLORS = []

def readPrefFracs(currFramePoc, mvLog): 
    decoderOptLogFileName = f'/home/felipe/Projetos/ndp-repos/outputs/frac-only-training/opt-logs-4bits/NDP_Netflix_{mvLog.video}_{mvLog.config}_{mvLog.qp}.opt.log'
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


def plotScatterChart(currFramePoc, mvLog, onlyFrac=False, targetCtuLine=-1, enableNotes=False, highlightPrefFrac=False):
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
                            if fracPos == prefFrac and highlightPrefFrac:
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

    frameWidth = YUV_VIDEOS[mvLog.video]['res'][0]
    frameHeight = YUV_VIDEOS[mvLog.video]['res'][1]

    if targetCtuLine != -1:
        xLeft, xRight, yTop, yBottom = getCtuWindowLimits(targetCtuLine, frameWidth, frameHeight)
        # xLeft, xRight, yTop, yBottom = getInterpWindowLimits(targetCtuLine, frameWidth, 128, -64, 0)

    fig = plt.figure()
    
    for refList in refLists:
        ax = fig.add_subplot(1, 2, refList+1)

        if targetCtuLine != -1:
            ax.hlines(yTop, xmin=xLeft, xmax=xRight)
            ax.hlines(yBottom, xmin=xLeft, xmax=xRight)

            ax.vlines(xLeft, ymin=yTop, ymax=yBottom)
            ax.vlines(xRight, ymin=yTop, ymax=yBottom)

        print(len(rectangles[f'L{refList}']))
        for rect in rectangles[f'L{refList}']:
            ax.add_patch(rect)

        if targetCtuLine != -1:
            xWindowMargin = int(X_WINDOW_MARGIN * (xRight - xLeft))
            yWindowMargin = int(Y_WINDOW_MARGIN * (yBottom - yTop))

            ax.set_xlim([xLeft - xWindowMargin, xRight + xWindowMargin])
            ax.set_ylim([yTop - yWindowMargin, yBottom + yWindowMargin])

             # Annotate pref frac hit
            if enableNotes:
                ctuLineKey = (targetCtuLine, f'L{refList}')
                _, prefFracHit = prefFracDict[ctuLineKey]
                note = f'Hit%: {prefFracHit}'
                ax.annotate(note, (xLeft - xWindowMargin, yBottom + yWindowMargin))

        else:
            ax.set_xlim([0 - X_MARGIN, frameWidth + X_MARGIN]) 
            ax.set_ylim([0 - Y_MARGIN, frameHeight + Y_MARGIN])

         
        ax.invert_yaxis()
        ax.set_title(f'Access map - Reference frame L{refList}')
    
    plt.show()
    #plt.savefig('/home/felipe/Projetos/ndp-repos/ndp-tcsvt/outputs/test_rect.pdf', format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    mvLog = McDecodeData(
        mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/baseline/mvlogs-4bits/NDP_Netflix_Boat_RA_22.log.gz', 
        #mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/frac-only/mvlogs-opt-4bits/NDP_CatRobot_LD_37.opt.log.gz', 
        quarterOnly = True,
    )

    plotScatterChart(
        currFramePoc=21, 
        mvLog=mvLog,
        onlyFrac=False,
        targetCtuLine=29,
        # enableNotes=True,
        highlightPrefFrac=True,
    )

    # plotScatterChart(
    #     currFramePoc=8, 
    #     mvLog=mvLog,
    #     onlyFrac=False,
    #     targetCtuLine=16,
    #     # enableNotes=True,
    #     highlightPrefFrac=True,
    # )

    # plotScatterChart(
    #     currFramePoc=1, 
    #     mvLog=mvLog,
    #     onlyFrac=False,
    #     targetCtuLine=11,
    #     # enableNotes=True,
    #     highlightPrefFrac=True,
    # )

