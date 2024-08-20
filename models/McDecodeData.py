import os
from models.mc_data_classes import *
from utils.defines import VVC_constants, YUV_VIDEOS

class McDecodeData:
    def __init__(self, video, mvFileGzPath = '', traceFileGzPath = '', calcSpec=True):
        self.mcData = {}
        self.ctuLineKeys = []
        self.ctuLineKeysSet = set()
        
        self.video = video
        self.totalCtuLineArea = VVC_constants.CTU_size.value * int(YUV_VIDEOS[self.video]['res'].split('x')[1])

        print(f'CTU Line area: {self.totalCtuLineArea}')


        if mvFileGzPath == '' and traceFileGzPath == '' or mvFileGzPath != '' and traceFileGzPath != '':
            print('[error] Please inform exactely one input file!')

        if mvFileGzPath != '':
            self.__parseMvLog(mvFileGzPath)

        if traceFileGzPath != '':
            self.__parseTrace(traceFileGzPath)

    def __addCtuWindowKey(self, currFramePoc, yCU):
        ctuLineKey = (currFramePoc, yCU // VVC_constants.CTU_size.value)
        if ctuLineKey not in self.ctuLineKeysSet:
            self.ctuLineKeys.append(ctuLineKey)
            self.ctuLineKeysSet.add(ctuLineKey)
        return ctuLineKey
    
    def __parseMvLog(self, fileGzPath):
        unGzipMvLogFileCmd = f'gzip -dk {fileGzPath}'
        print(f'[info] Unzipping mv-log file... {unGzipMvLogFileCmd}')
        os.system(unGzipMvLogFileCmd)

        filePath = fileGzPath.replace('.gz', '')

        print(f'[info] Parsing mv-log file... {filePath}')
        with open(filePath, 'r') as fpLog:
            for line in fpLog.readlines():
                tokens = line.split(';')

                currFramePoc = int(tokens[0])
                xCU = int(tokens[1])
                yCU = int(tokens[2])
                wCU = int(tokens[3])
                hCU = int(tokens[4])
                refList = int(tokens[5])
                refFramePoc = int(tokens[6])
                fullMV = int(tokens[7]), int(tokens[8])
                integMV = int(tokens[9]), int(tokens[10])
                fracMV = int(tokens[11]), int(tokens[12])                

                self.__addCtuWindowKey(currFramePoc, yCU)
                
                if currFramePoc not in self.mcData:
                    frameData = Frame(currFramePoc)
                    self.mcData[currFramePoc] = Frame(currFramePoc)
                else:
                    frameData = self.mcData[currFramePoc]

                cuData = frameData.addCuInCTU(xCU, yCU, wCU, hCU)
                cuData.addMotionInfo(refList, refFramePoc, fullMV, integMV, fracMV)             

        os.remove(filePath)

    def printMcDecodeData(self):
        print(len(self.mcData))
        for framePoc in self.mcData.keys():
            frame = self.mcData[framePoc]
            print(frame)

    def reportFracAnalysis(self):
        for _, frameData in self.mcData.items():
            for _, ctuLineData in frameData.ctuLines.items():
                accumMVs = { 'L0' : {}, 'L1' : {}}
                accumInter = { 'L0' : 0, 'L1' : 0 }
                accumCuAreaInter = 0
                for _, ctuData in ctuLineData.CTUs.items():
                    for _, cuData in ctuData.CUs.items():
                        cuArea = cuData.hCU * cuData.wCU
                        if len(cuData.motionInfo) > 0:
                            accumCuAreaInter += cuArea

                        for refList, motionInfo in cuData.motionInfo.items():
                            fracMV = motionInfo.fracMV
                            if fracMV not in accumMVs[refList]:
                                accumMVs[refList][fracMV] = 0

                            accumMVs[refList][fracMV] += cuArea
                            accumInter[refList] += cuArea
                    
                print(frameData.poc, ctuLineData.ctuLine, end=': ')
                reportInterAnalysis = float(accumCuAreaInter) / self.totalCtuLineArea
                reportFracAnalysis = { 'L0' : {} , 'L1' : {} }
                for refList, accums in accumMVs.items():
                    for fracMV, accumMV in accums.items():
                        reportFracAnalysis[refList][fracMV] = float(accumMV) / accumInter[refList]
                print(reportInterAnalysis)
                print(reportFracAnalysis)
                input()
