from models.McDecodeData import McDecodeData

if __name__ == '__main__':
    mvlog = McDecodeData(
        mvFileGzPath='/home/felipe/Projetos/ndp-repos/outputs/baseline/mvlogs-4bits/NDP_BasketballDrive_RA_22.log.gz',
        video= 'BasketballDrive',
    ) 

    # mvlog.printMcDecodeData()
    mvlog.reportFracAnalysis()