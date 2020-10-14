# ---------------------------------------------------------------------------- #
#                                  TPAutoProg                                  #
# ---------------------------------------------------------------------------- #
"""
Author: Adam McKinlay
Program: TPAutoProg
Version: 1
Description: TPAutoProg can manipulate Fanuc TP programs and save changes in the 
             form of a text file that then needs to be converted to .ls file
"""

# ---------------------------------------------------------------------------- #
#                                    TPCode                                    #
# ---------------------------------------------------------------------------- #
class TPCode:
    numLines = 0

    def __init__(self, lineNum, moveType, point, speed, gunStatus):
        self.__lineNum = lineNum
        self.__moveType = moveType
        self.__point = point
        self.__speed = speed
        self.__gunStatus = gunStatus
        TPCode.numLines += 1

    def getLineNum(self):
        return self.__lineNum

    def getMoveType(self):
        return self.__moveType
    
    def getPoint(self):
        return self.__point
    
    def getSpeed(self):
        return self.__speed
    
    def getGunStatus(self):
        return self.__gunStatus

    def setLineNum(self, lineNum):
        self.__lineNum = lineNum

    def setMoveType(self, moveType):
        self.__moveType = moveType

    def setPoint(self, point):
        self.__point = point
    
    def setSpeed(self, speed):
        self.__speed = speed
    
    def setGunStatus(self, gunStatus):
        self.__gunStatus = gunStatus

    def addNumLines(self):
        TPCode.numLines +=1

    def __str__(self):
        return "  " + str(self.__lineNum) + ":" + self.__moveType + " P[" + str(self.__point) + "] " + str(self.__speed) + "mm/sec CNT100 "  + self.__gunStatus + "\t;\n"