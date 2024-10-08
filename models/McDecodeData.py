import os
from models.mc_data_classes import *
from utils.defines import VVC_constants, YUV_VIDEOS, MV_TO_FRAC_POS, FRAC_POS_LIST
from utils.utils import getCtuWindowId


class McDecodeData:
    def __init__(self, mvFileGzPath, calcSpec=True, quarterOnly=True):
        self.mcData = {}
        self.ctuWindowKeys = []
        self.ctuWindowKeysSet = set()

        self.quarterOnly = quarterOnly
        
        self.__parseExperimentInfo(mvFileGzPath)

        self.frameWidth = YUV_VIDEOS[self.video]['res'][0]
        if self.frameWidth in [3840, 4096]:
            self.totalCtuLineArea = VVC_constants.CTU_size.value * (self.frameWidth // 2)
        else:
            self.totalCtuLineArea = VVC_constants.CTU_size.value * self.frameWidth

        self.__parseMvLog(mvFileGzPath)

    def __parseExperimentInfo(self, filePath):
        # '/home/felipe/Projetos/ndp-repos/outputs/baseline/mvlogs-4bits/NDP_BasketballDrive_RA_22.log.gz'
        filePath = filePath.replace('Netflix_', '')
        self.experimentInfo = filePath.split('/')[-1].split('.')[0]
        tokens = self.experimentInfo.split('_')
        self.video = tokens[1]
        self.config = tokens[2]
        self.qp = tokens[3]

    def __addCtuWindowKey(self, currFramePoc, xCU, yCU):
        ctuWindowId = getCtuWindowId(xCU, yCU, self.frameWidth)   

        ctuWindowKey = (currFramePoc, ctuWindowId)
        if ctuWindowKey not in self.ctuWindowKeysSet:
            self.ctuWindowKeys.append(ctuWindowKey)
            self.ctuWindowKeysSet.add(ctuWindowKey)
        return ctuWindowKey
    
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

                self.__addCtuWindowKey(currFramePoc, xCU, yCU)
                
                if currFramePoc not in self.mcData:
                    frameData = Frame(currFramePoc, self.frameWidth)
                    self.mcData[currFramePoc] = frameData
                else:
                    frameData = self.mcData[currFramePoc]

                cuData = frameData.addCuInCTU(xCU, yCU, wCU, hCU)

                if self.quarterOnly:
                    fracMV = (fracMV[0] & (~3), fracMV[1] & (~3))

                cuData.addMotionInfo(refList, refFramePoc, fullMV, integMV, fracMV)             
        os.remove(filePath)
        
    def printMcDecodeData(self):
        print(len(self.mcData))
        for framePoc in self.mcData.keys():
            frame = self.mcData[framePoc]
            print(frame)

    def reportFracMcPctg(self):
        accumFrac = 0
        accumTotalMC = 0
        for _, frameData in self.mcData.items():
            for _, ctuLineData in frameData.ctuLines.items():
                for _, ctuData in ctuLineData.CTUs.items():
                    for _, cuData in ctuData.CUs.items():
                        for _, motionInfo in cuData.motionInfo.items():
                            cuSize = cuData.xCU * cuData.yCU
                            if motionInfo.isFracMC():
                                accumFrac += cuSize
                            accumTotalMC += cuSize
        return float(accumFrac) / accumTotalMC

    def reportFracAnalysisQuarter(self):
        #report = 'video;config;qp;frame;ctu_line;I;Q0;'
        headerLine = 'Video; Config; QP; Frame; Ref. list; CTU line; Inter pctg.; I; H0; H1; H2; Q0; Q1; Q2; Q3; Q4; Q5; Q6; Q7; Q8; Q9; Q10; Q11\n'
        outputPctg = headerLine
        outputAccum = headerLine

        experimentReport = f'{self.video};{self.config};{self.qp};'
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
                            mvPos = MV_TO_FRAC_POS[motionInfo.fracMV]
                            if mvPos not in accumMVs[refList]:
                                accumMVs[refList][mvPos] = 0

                            accumMVs[refList][mvPos] += cuArea
                            if mvPos != 0:
                                accumInter[refList] += cuArea
                    
                reportInterAnalysis = float(accumCuAreaInter) / self.totalCtuLineArea
                reportFracAnalysis = { 'L0' : {} , 'L1' : {} }
                for refList, accums in accumMVs.items():
                    for mvPos, accumMV in accums.items():
                        reportFracAnalysis[refList][mvPos] = float(accumMV) / (accumInter[refList])

                for refList, report in reportFracAnalysis.items():
                    reportLine = f'{experimentReport}{frameData.poc};{refList};{ctuLineData.ctuLine};'
                    reportLine += f'{"{:.4f}".format(float(accumInter[refList]) / self.totalCtuLineArea)};'

                    for mvPos in FRAC_POS_LIST:
                        pctgToReport = 0
                        if mvPos in report:
                            pctgToReport += report[mvPos]
                        
                        reportLine += f'{"{:.4f}".format(pctgToReport)}'
                        if mvPos != 'Q11':
                            reportLine += ';'
                        else:
                            reportLine += '\n'
                    outputPctg += reportLine

                for refList, accum in accumMVs.items():
                    reportLine = f'{experimentReport}{frameData.poc};{refList};{ctuLineData.ctuLine};'
                    reportLine += f'{"{:.4f}".format(float(accumInter[refList]) / self.totalCtuLineArea)};'

                    for mvPos in FRAC_POS_LIST:
                        accumToReport = 0
                        if mvPos in accum:
                            accumToReport += accum[mvPos]
                        
                        reportLine += str(accumToReport)
                        if mvPos != 'Q11':
                            reportLine += ';'
                        else:
                            reportLine += '\n'
                    outputAccum += reportLine
        return outputAccum, outputPctg