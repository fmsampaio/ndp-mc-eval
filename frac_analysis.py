import os
import pyperclip

from models.McDecodeData import McDecodeData

OUTPUTS_PATH = '/home/felipe/Projetos/ndp-repos/outputs/'
MV_LOG_FILES_PATH = f'{OUTPUTS_PATH}baseline/mvlogs-4bits/'
FRAC_ANALYSIS_REPORT_PATH = f'{OUTPUTS_PATH}frac-analysis-reports/'

VIDEOS = [
    'CatRobot',
    'FoodMarket4',
    # 'DinnerScene',
    # 'PierSeaside',
    # 'Boat',
    # 'TunnelFlag',
    # 'SquareAndTimelapse'
]

def runFracAnalysis():
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

    
    for mvLogFileName in filtered:
        if '.log.gz' not in mvLogFileName:
            continue

        print(f'[info] [{fileCount}/{len(filtered)}] Processing {mvLogFileName}')
        
        mvlog = McDecodeData(f'{MV_LOG_FILES_PATH}{mvLogFileName}', quarterOnly=True)

        fpAccum = open(f'{FRAC_ANALYSIS_REPORT_PATH}{mvlog.experimentInfo}_frac_analysis.csv', 'w')
        reportAccum, _ = mvlog.reportFracAnalysisQuarter() 
        fpAccum.write(reportAccum)
        fpAccum.close()        
        
        fileCount += 1

def runMcPctgAnalysis():
    mvLogFilesList = os.listdir(MV_LOG_FILES_PATH)
    mvLogFilesList.sort()
    
    if len(VIDEOS) == 0:
        filtered = mvLogFilesList
    
    else:
        filtered = []
        for file in mvLogFilesList:
            for video in VIDEOS:
                if video in file and '.log.gz' in file:
                    filtered.append(file)

    fileCount = 1

    print(len(filtered), filtered)
    
    fpOutput = open(f'{FRAC_ANALYSIS_REPORT_PATH}report-frac-mc-analysis.csv', 'w')
    
    for mvLogFileName in filtered:
        if '.log.gz' not in mvLogFileName:
            continue

        print(f'[info] [{fileCount}/{len(filtered)}] Processing {mvLogFileName}')
        
        mvlog = McDecodeData(f'{MV_LOG_FILES_PATH}{mvLogFileName}', quarterOnly=True)
        fracPctg = mvlog.reportFracMcPctg()

        reportLine = f'{mvlog.video};{mvlog.config};{mvlog.qp};{fracPctg}\n'
        print(reportLine)

        fpOutput.write(reportLine)

        fileCount += 1
    
    fpOutput.close()


if __name__ == '__main__':
    runMcPctgAnalysis()
    # runFracAnalysis()

    # mvLog = McDecodeData(f'{MV_LOG_FILES_PATH}NDP_Netflix_Boat_RA_22.log.gz', quarterOnly=True)
    # report, _ = mvLog.reportFracAnalysisQuarter()
    # pyperclip.copy(report)
    # print(report)


