import os
from models.McDecodeData import McDecodeData

OUTPUTS_PATH = '/home/felipe/Projetos/ndp-repos/outputs/'
MV_LOG_FILES_PATH = f'{OUTPUTS_PATH}baseline/mvlogs-4bits/'
FRAC_ANALYSIS_REPORT_PATH = f'{OUTPUTS_PATH}frac-analysis-reports/'

VIDEOS = ['BasketballDrive']

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
    
    for mvLogFileName in filtered:
        if '.log.gz' not in mvLogFileName:
            continue

        print(f'[info] [{fileCount}/{len(filtered)}] Processing {mvLogFileName}')
        
        mvlog = McDecodeData(f'{MV_LOG_FILES_PATH}{mvLogFileName}')

        fpAccum = open(f'{FRAC_ANALYSIS_REPORT_PATH}{mvlog.experimentInfo}_frac_analysis.csv', 'w')
        reportAccum, _ = mvlog.reportFracAnalysis() 
        fpAccum.write(reportAccum)
        fpAccum.close()        
        
        fileCount += 1

    