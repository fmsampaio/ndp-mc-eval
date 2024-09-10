import os
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



from models.McDecodeData import McDecodeData

OUTPUTS_PATH = '/home/felipe/Projetos/ndp-repos/outputs/'
MV_LOG_FILES_PATH = f'{OUTPUTS_PATH}baseline/mvlogs-4bits/'
ANALYSIS_REPORT_PATH = f'{OUTPUTS_PATH}interp-window-analysis/'

LARGE_INT = 999999

SMALL_SIZE = 6
MEDIUM_SIZE = 8
BIGGER_SIZE = 112

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def maximum(a,b):
    return ( a if a > b else b )

def minimum(a,b):
    return ( a if a < b else b )

def analyzeInterpWindowLimits(data):
    limits = []
    heights = []
    diffHeightsSet = set()

    for _, frameData in data.mcData.items():
        for _, ctuLineData in frameData.ctuLines.items():
            yTopLimit = { 'L0' : LARGE_INT , 'L1' : LARGE_INT }
            yBottomLimit = { 'L0' : -LARGE_INT , 'L1' : -LARGE_INT }

            for _, ctuData in ctuLineData.CTUs.items():
                for _, cuData in ctuData.CUs.items():
                    for refList, motionInfo in cuData.motionInfo.items():
                        yTop = cuData.yCU + motionInfo.integMV[1]
                        yBottom = yTop + cuData.hCU

                        yTopLimit[refList] = minimum(yTopLimit[refList], yTop)
                        yBottomLimit[refList] = maximum(yBottomLimit[refList], yBottom)
            
            for refList in ['L0', 'L1']:
                limits.append( ( yTopLimit[refList] , yBottomLimit [refList] ) )
                
                interpWindowHeight = yBottomLimit[refList] - yTopLimit[refList]
                heights.append(interpWindowHeight)
                diffHeightsSet.add(interpWindowHeight)

    hMax.append(max(heights))
    
    return limits, heights, len(diffHeightsSet)

def plotHistograms(mcDataDic):

    iSubPlot = 0
    numOfSubPlotsPerPage = 4
    numOfSubPlotsPerRow = 2
    numOfSubPlotsPerColumn = numOfSubPlotsPerPage//numOfSubPlotsPerRow

    figures = []
    axes = []

    yMaxDic = {}
    # numOfPages = len(mcDataDic) // numOfSubPlotsPerPage + (0 if len(mcDataDic) % numOfSubPlotsPerPage else 1)

    for experiment, mcData in mcDataDic.items():
        iSubId = iSubPlot % numOfSubPlotsPerPage

        if iSubId == 0:
            fig, axs = plt.subplots(numOfSubPlotsPerColumn, numOfSubPlotsPerRow)
            figures.append(fig)
            fig.subplots_adjust(hspace=0.5, wspace=0.3)

        xSub = iSubId // numOfSubPlotsPerRow
        ySub = iSubId % numOfSubPlotsPerRow

        ax = axs[xSub, ySub]
        axes.append( (experiment, ax) )

        print(xSub, ySub)

        _ , heights, numBins = mcData

        histBins = hMax // 8
        n, bins, patches = ax.hist(heights, bins=histBins, color='gray', edgecolor='black', density=True)

        mu = np.average(heights)
        sigma = np.std(heights)

        print(mu, sigma)

        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        ax.plot(bins, y)

        if xSub == numOfSubPlotsPerColumn-1:
            ax.set_xlabel('Interpolation windows height')
        if ySub == 0:
            ax.set_ylabel('Probability density')

        ax.set_title(str(experiment))
        ax.set_xlim([0, hMax // 2])

        _, xMax = ax.get_xlim()
        _, yMax = ax.get_ylim()

        if experiment[0] not in yMaxDic:
            yMaxDic[experiment[0]] = []
        yMaxDic[experiment[0]].append(yMax)

        note = f'Avg: {int(mu)}\nStd: {int(sigma)}'
        ax.annotate(note, (xMax * 0.8, 0))

        iSubPlot += 1
    
    print(len(figures))

    for exp, ax in axes:
        ax.set_ylim([0, max(yMaxDic[exp[0]])])

    pp = PdfPages(f'{ANALYSIS_REPORT_PATH}frac_analysis_plots.pdf')
    for fig in figures:
        #fig.show()
        fig.savefig(pp, format='pdf', orientation='portrait')
    pp.close()


def parseExperimentInfo(fileName):
    tokens = fileName.split('/')[-1].split('.')[0].split('_')
    video = tokens[1]
    config = tokens[2]
    qp = tokens[3]
    
    return video, config, qp

VIDEOS = []

VIDEOS += ['BQMall', 'BasketballDrill', 'RaceHorsesC', 'PartyScene'] # Class C
VIDEOS += ['BasketballDrive', 'Cactus', 'BQTerrace', 'RitualDance', 'MarketPlace'] # Class B
VIDEOS += ['CatRobot', 'DaylightRoad2', 'ParkRunning3'] # Class A2
VIDEOS += ['Campfire', 'FoodMarket4', 'Tango2'] # Class A1

hMax = []

if __name__ == '__main__':
    
    mvLogFilesList = os.listdir(MV_LOG_FILES_PATH)
    mvLogFilesList.sort()

    if len(VIDEOS) == 0:
        filtered = mvLogFilesList
    
    else:
        filtered = []
        for file in mvLogFilesList:
            for video in VIDEOS:
                if video in file:
                    filtered.append(file)

    fileCount = 1

    mvLogData = {}
    
    for mvLogFileName in filtered:
        if '.log.gz' not in mvLogFileName:
            continue

        experimentInfo = parseExperimentInfo(mvLogFileName)
        print(f'[info] [{fileCount}/{len(filtered)}] Processing {experimentInfo}')
        
        mcData = McDecodeData(f'{MV_LOG_FILES_PATH}{mvLogFileName}')

        mvLogData[experimentInfo] = analyzeInterpWindowLimits(mcData)
        
        fileCount += 1

    hMax = max(hMax)

    plotHistograms(mvLogData)