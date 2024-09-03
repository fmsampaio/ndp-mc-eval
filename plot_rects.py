import matplotlib.patches
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from models.McDecodeData import McDecodeData
from utils.defines import YUV_VIDEOS


CTU_LINES_COLORS = []

def plotScatterChart(currFramePoc, mvLog, onlyFrac=False, targetCtuLine=-1):
    frameData = mvLog.mcData[currFramePoc]
    
    rectangles = { 'L0' : [], 'L1' : [] }
    
    refLists = [0, 1]
    
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
                        if motionInfo.isFracMC():
                            color = 'red'
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
                                    alpha = 0.5
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
            ax.hlines(yTopCtuLine, xmin=0, xmax=frameWidth)
            ax.hlines(yBottomCtuLine, xmin=0, xmax=frameWidth)

        print(len(rectangles[f'L{refList}']))
        for rect in rectangles[f'L{refList}']:
            ax.add_patch(rect)
        
        ax.set_xlim([0, frameWidth]) 

        if targetCtuLine != -1:
            ax.set_ylim([yTopCtuLine - 64, yBottomCtuLine + 64]) 
        else:
            ax.set_ylim([0, frameHeight]) 

        ax.invert_yaxis()
    
    plt.show()
    #plt.savefig('/home/felipe/Projetos/ndp-repos/ndp-tcsvt/outputs/test_rect.pdf', format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    mvLog = McDecodeData(
        mvFileGzPath = '/home/felipe/Projetos/ndp-repos/outputs/baseline/mvlogs-4bits/NDP_BasketballDrive_RA_27.log.gz', 
        quarterOnly = True,
    )

    plotScatterChart(
        currFramePoc=12, 
        mvLog=mvLog,
        onlyFrac=False
    )



