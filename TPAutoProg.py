# ---------------------------------------------------------------------------- #
#                                   AutoProg                                   #
# ---------------------------------------------------------------------------- #
"""
Author: Adam McKinlay
Program: TPAutoProg
Version: 1
Description: TPAutoProg can manipulate Fanuc TP programs and save changes in the 
             form of a text file that then needs to be converted to .ls file
"""

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #
from Point import Point
from tpCode import TPCode
import matplotlib.pyplot as plt
import logging
import argparse
import datetime
import os
import sys

# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
#Setup logging
LOG_FORMAT = "----------------------------------------\n %(levelname)s %(asctime)s - %(message)s\n----------------------------------------\n"
logging.basicConfig(filename="TPAutoProg.log", level = logging.DEBUG, format = LOG_FORMAT)
logger = logging.getLogger()

def main():
    logger.info("Start of TPAutoProg")

    flag = 1
    pointsList = []
    codeList = []
    newCodeList = []
    endLine = 10000

    #ArgumentParser
    parser = argparse.ArgumentParser(description="Manipulate Fanuc TP programs and save changes in the form of a text file", epilog="Thanks for using TPAutoProg") #will need max values for DSC to prevent DSC -> future
    parser.add_argument('-f', '--file', type=str, help="file to edit")
    parser.add_argument('-d', '--directory', type=str, help="location of file")
    args = parser.parse_args()

    #Check if directory exists
    directory = args.directory
    if(not os.path.isdir(directory)):
        print(f"Error: directory: '{directory}' does not exist")
        logger.error(f"Error: directory: '{directory}' does not exist")
        exit(1)

    #Check if file exists
    readFile = args.file
    filePath = directory + "/" + readFile
    if(not os.path.isfile(filePath)):
        print(f"Error: file: '{readFile}' does not exist")
        logger.error(f"Error: file: '{readFile}' does not exist")
        exit(0)
    
    #Welcome Message
    print("File found!\nHow would you like to proceed?")
    logger.info("File found!\nHow would you like to proceed?")
    pointsList, codeList = setupPoints(filePath, pointsList, codeList)
    
    #Infinite program options
    while(flag!=-1):
        menuOptions()
        userOptionChoice = int(validateNum("Enter an option: ", "Option", 1, 7))
        logger.info(f"User entered: {userOptionChoice}")

        #Change a Point
        if(userOptionChoice == 1):
            userPointOption = int(validateNum("Enter a point to change: ", "Point", 1, len(pointsList)))
            userCordChoice = input("Enter the coordinate to change (x, y, z): ")
            userNewValue = float(input("Enter the new value for the point: "))
            pointsList = touchUpPoint(pointsList, userPointOption, userCordChoice, userNewValue)
            
            logger.info(f"Coordinate to change: {userPointOption}")
            logger.info(f"Axis to change: {userCordChoice}")
            logger.info(f"New value: {userNewValue}")
            logger.info("\n********************************\nPoint successfully changed!\n********************************")
            
            print("\n********************************")
            print("Point successfully changed!")
            print("********************************\n")

        #Translate all points about (x, y, z)
        elif(userOptionChoice == 2):
            userCordChoice = input("Enter the coordinate to change (x, y, z): ")
            userTranslationValue = float(input("Enter the value of the translation: "))
            pointsList = translatePoints(pointsList, userCordChoice, userTranslationValue)

            logger.info(f"Coordinates Axis to change: {userCordChoice}")
            logger.info(f"Axis Translation value: {userTranslationValue}")
            logger.info("\n********************************\nPoints successfully translated!\n********************************")

            print("\n********************************")
            print("Points successfully translated!")
            print("********************************\n")

        #Replicate cycle throughout offset and offset value
        elif(userOptionChoice == 3):
            userStartLineChoice = int(input("Enter the line of the start of the cycle: "))
            userEndLineChoice = int(input("Enter the line of the end of the cycle: "))
            userCordChoice = input("Enter the offset-coordinate (x, y, z): ")
            userTranslationValue = float(input("Enter the offset value: "))
            userCyclesNeeded = int(input("Enter the number of cycles needed: "))

            endLine = userEndLineChoice
            newCodeList, pointsList = copyCycle(codeList, pointsList, userStartLineChoice, userEndLineChoice, userCordChoice, userTranslationValue, userCyclesNeeded)

            logger.info(f"Start of cycle: {userStartLineChoice}")
            logger.info(f"End of cycle: {userEndLineChoice}")
            logger.info(f"Axis of translation: {userCordChoice}")
            logger.info(f"Translation value: {userTranslationValue}")
            logger.info(f"Number of cycles needed: {userCyclesNeeded}")
            logger.info("\n********************************\nCycle successfully copied!\n********************************")

            print("\n********************************")
            print("Cycle successfully copied!")
            print("********************************\n")

        #Change repating points
        elif(userOptionChoice == 4):
            userCordChoice = input("Enter the offset-coordinate (x, y, z): ")
            userCurrentNew = float(input("Enter the current number to replace: "))
            userNewValue = float(input("Enter the new number to replace old value: "))
            pointsList = changeRepeatingPoints(pointsList, userCurrentNew, userNewValue, userCordChoice)

            logger.info(f"Axis selected: {userCordChoice}")
            logger.info(f"Current numerical value: {userCurrentNew}")
            logger.info(f"New numerical value: {userNewValue}")
            logger.info("\n********************************\nRepating points successfully changed!\n********************************")

            print("\n********************************")
            print("Repating points successfully changed!")
            print("********************************\n")

        #Change hand orientation
        elif(userOptionChoice == 5):
            userCordChoice = input("Enter the offset-coordinate (x, y, z): ")
            pointsList = copyHand(pointsList, userCordChoice)

            logger.info(f"Axis selected: {userCordChoice}")
            logger.info("\n********************************\nHand successfully changed!\n********************************")

            print("\n********************************")
            print("Hand successfully changed!")
            print("********************************\n")

        #Display 3D view
        elif(userOptionChoice == 6):
            displayGrpah(pointsList, readFile)
            logger.info("Graph Displayed")

        #End program
        elif(userOptionChoice == 7):
            printToFile(pointsList, newCodeList, filePath, readFile, endLine)
            print("\n********************************")
            print("End of program \n-TPAutoProg")
            print("********************************\n")
            print("WARNING: The text file generated need to be converted to an .ls file prior to upload.")
            print("WARNING: This program does not guarantee created program will have correct orentations and be within your systems DCS.")
            
            logger.warning("The text file generated need to be converted to an .ls file prior to upload.")
            logger.warning("This program does not guarantee created program will have correct orentations and be within your systems DCS.")
            logger.info("\n********************************\nEnd of program \n-TPAutoProg\n********************************")

            exit(0)
    

# ---------------------------------------------------------------------------- #
#                                    Modules                                   #
# ---------------------------------------------------------------------------- #

# -------------------------------- setupPoints ------------------------------- #

"""
setUpPoints
Arguments: 
    filePath   - the directory path to the file
    pointsList - list of all coordinates currently in file
    codeList   - list of all lines of code currently in file with robot movement

Return 
    pointList  - updated list of all coordinates currently in file 
    codeList   - updated list of all lines of code currently in file with robot movement

Description    - setupPoints reads the orginal file for all robot coordinates and lines of code with robot movement    
"""
def setupPoints(filePath, pointsList, codeList):
    inputFile = open(filePath, 'r', encoding='utf-8')

    #Code variables
    lineNum = None
    moveType = None
    codePoint = None
    moveSpeed = None
    gunStatus = None

    #Coordinate variables
    inputPoint = None
    uf = None
    config = None
    x = None
    y = None
    z = None
    w = None
    p = None
    r = None

    #Begin reading file
    line = inputFile.readline()
    while (line != ''):
        #Read Code
        if('/MN' in line):
            while('/POS' not in line):
                if(':L' in line):
                    lineNum = int((line[2:line.index(':')]).strip())
                    moveType = line[line.index(':')+1:line.index('P')-1].strip()
                    codePoint = int(line[line.index('P')+2:line.index(']')].strip())
                    moveSpeed = int(line[line.index(']')+2:line.index('m')].strip())
                    #print(line[line.index(']')+2:line.index('m')].strip())

                    if('Gun=' in line):
                        gunStatus = "Gun=" + line[line.index('=')+1:line.index('=')+4].strip()
                    if('Gun=' not in line):
                        gunStatus = ""

                    #Declare and append TPCode object
                    lineOfCode = TPCode(lineNum, moveType, codePoint, moveSpeed, gunStatus)
                    codeList.append(lineOfCode)
                    logger.debug(f"Line of code added: {lineOfCode}")
                
                #Keep track of non robot movement lines of code
                if('L' not in line):
                    TPCode.numLines += 1
                else:
                    TPCode.numLines += 1
                line = inputFile.readline()

        #Read Coordinate
        if('/POS' in line):
            while('/END' not in line):
                if('P[' in line):
                    inputPoint = line[line.index('[') + 1:line.index(']')].strip()
                    if(':' in inputPoint):
                        inputPoint = inputPoint[0:inputPoint.index(':')].strip()
                    inputPoint = int(inputPoint)
                elif('UF' in line):
                    uf = line[line.index('UF'): line.index('CONFIG')-3].strip()
                    config = line[line.index('CONFIG'): len(line) -1].strip()
                elif('X' in line):
                    tempCords = line.rsplit(',\t')
                    x = float(filterCords(tempCords,0))
                    y = float(filterCords(tempCords,1))
                    z = float(filterCords(tempCords,2))
                elif('W' in line):
                    tempCords = line.rsplit(',\t')
                    w = float(filterCords(tempCords, 3))
                    p = float(filterCords(tempCords, 4))
                    r = float(filterCords(tempCords, 5))
                    point = Point(inputPoint, uf, config, x, y, z, w, p, r)
                    pointsList.append(point)
                    logger.debug(f"Coordinate added: {point}")
                    
                line = inputFile.readline()

        line = inputFile.readline()
    inputFile.close()
    return pointsList, codeList

# -------------------------------- filterCords ------------------------------- #
"""
filterCords
Arguments: 
    cords - list of all coordinates
    pos   - a reference position to coordinates or angles
Returns
    temp  - the value of the coordinate or angle striped

Description    - filterCords strips the coordinates and angles
"""
def filterCords(cords, pos):
    temp = None

    if(pos == 0):
        temp = cords[0]
        temp = temp.strip('mm')
        temp = temp.strip()
        temp = temp.strip('X')
        temp = temp.strip()
        temp = temp.strip('=')
        temp = temp.strip()
    elif(pos == 1):
        temp = cords[1]
        temp = temp.strip('mm')
        temp = temp.strip()
        temp = temp.strip('Y')
        temp = temp.strip()
        temp = temp.strip('=')
        temp = temp.strip()
    elif(pos == 2):
        temp = cords[2]
        temp = temp.strip('Z')
        temp = temp.strip()
        temp = temp.strip('=')
        temp = temp.strip()
        temp = temp.strip('mm,')
        temp = temp.strip()
    elif(pos == 3):
        temp = cords[0]
        temp = temp.strip('deg')
        temp = temp.strip()
        temp = temp.strip('W')
        temp = temp.strip()
        temp = temp.strip('=')
        temp = temp.strip()
    elif(pos == 4):
        temp = cords[1]
        temp = temp.strip('deg')
        temp = temp.strip()
        temp = temp.strip('P')
        temp = temp.strip()
        temp = temp.strip('=')
        temp = temp.strip()
    elif(pos == 5):
        temp = cords[2]
        temp = temp.strip('R')
        temp = temp.strip()
        temp = temp.strip('=')
        temp = temp.strip()
        temp = temp.strip('deg,')
        temp = temp.strip()
    return temp

# ------------------------------- touchUpPoint ------------------------------- #
"""
touchUpPoint
Arguments: 
    pointsList - list of all coordinates currently in file
    pointNum   - the coordinates being changed
    coordinate - the coordinate (x, y, z)
    newValue   - the new value of the coordinate

Returns
    pointsList - the updated points lists

Description    - touchUpPoint chagnges a coordinate of a specified value
"""
def touchUpPoint(pointsList, pointNum, coordinate, newValue):
    if (coordinate == 'x'):
        pointsList[pointNum-1].setX(newValue)

    elif(coordinate == 'y'):
        pointsList[pointNum-1].setY(newValue)

    elif(coordinate == 'z'):
        pointsList[pointNum-1].setZ(newValue)

    return pointsList

# ------------------------------ translatePoints ----------------------------- #
"""
translatePoints
Arguments: 
    pointsList       - list of all coordinates currently in file
    coordinate       - the coordinate (x, y, z)
    translationValue - the new value of the coordinates

Return
    pointsList       - the updated points lists

Description          - translatePoints changes all points of a specified coordinate
"""
def translatePoints(pointsList, coordinate, translationValue):
    for x in range(0,(len(pointsList)-1)):
        if (coordinate == 'x'):
            newValue = (float(pointsList[x].getX())+translationValue)
            pointsList[x].setX(newValue)

        elif(coordinate == 'y'):
            newValue = (float(pointsList[x].getY())+translationValue)
            pointsList[x].setY(newValue)

        elif(coordinate == 'z'):
            newValue = (float(pointsList[x].getZ())+translationValue)
            pointsList[x].setZ(newValue)

    return pointsList

# --------------------------------- copyCycle -------------------------------- #
"""
copyCycle
Arguments: 
    codeList         - list of all lines of code currently in file with robot movement
    pointsList       - list of all coordinates currently in file
    startLine        - the start of the cycle to be copied
    endLine          - the end of the cycle to be copied
    offsetCoordinate - the coordinate to translate the new cycles
    offsetValue      - the value to translate the new cycles
    numCycles        - the number of cycles desired

Return
    fullSetCodeList  - the updated list of all lines of code currently in file with robot movement
    newPointsList    - the updated list of all coordinates currently in file

Description          - copyCycle replicates a specified cycle for n number of times
"""
def copyCycle(codeList, pointsList, startLine, endLine, offsetCoordinate, offsetValue, numCycles):
    #Declare Variables
    fullSetCodeList = []
    newPointsList = pointsList.copy()
    numOfLines = codeList[len(codeList)-1].getLineNum()
    numOfPoints = pointsList[len(pointsList)-1].getNum()

    #For each cycle
    for i in range(0, numCycles):

        #For all lines of code
        for x in range(0, len(codeList)):

            #If within cycle range
            if(codeList[x].getLineNum() >= startLine and codeList[x].getLineNum() <= endLine):
                if(i>0):
                    numOfLines += 1
                    numOfPoints += 1

                    tempCodedLine = TPCode(numOfLines, codeList[x].getMoveType(), numOfPoints, codeList[x].getSpeed(), codeList[x].getGunStatus())

                    #For all points
                    for p in range(0, len(pointsList)):

                        #If the point is the same as line of code point
                        if(pointsList[p].getNum() == x+1):
                            tempPoint = Point(numOfPoints, pointsList[p].getUf(), pointsList[p].getConfig(), pointsList[p].getX(), pointsList[p].getY(), pointsList[p].getZ(), pointsList[p].getW(), pointsList[p].getP(), pointsList[p].getR())
                            
                            if (offsetCoordinate == 'x'):
                                newValue = (float(tempPoint.getX())+(offsetValue*i))
                                tempPoint.setX(newValue)

                            elif(offsetCoordinate == 'y'):
                                newValue = (float(tempPoint.getY())+(offsetValue*i))
                                tempPoint.setY(newValue)

                            elif(offsetCoordinate == 'z'):
                                newValue = (float(tempPoint.getZ())+(offsetValue*i))
                                tempPoint.setZ(newValue)
                            
                            fullSetCodeList.append(tempCodedLine)
                            newPointsList.append(tempPoint)

                            #print(tempCodedLine.__str__())
                #print(numOfPoints, ' ', numOfLines)
                #print(x+1, codeList[x].getLineNum())
    
    return fullSetCodeList, newPointsList.copy()

# -------------------------------- printToFile ------------------------------- #
"""
printToFile
Arguments
    pointsList - list of all coordinates currently in file
    codeList   - list of all lines of code currently in file with robot movement
    filePath   - path to the file
    readFile   - the file to read
    endLine    - the line to end on

Description    - prints pointsList and codeList to a file
"""
def printToFile(pointsList, codeList, filePath, readFile, endLine):
    inputFile = open(filePath, 'r', encoding='utf-8')
    outFileName = readFile[0:(len(readFile)-2)] + "txt"
    outputFile = open(outFileName,'w', encoding='utf-8')

    posIndex = 0

    line = inputFile.readline()
    while (line != ''):
        while('/POS' not in line):
            outputFile.write(line)
            line = inputFile.readline()

        outputFile.flush()
        if('/POS' in line):
            for lineOfCode in codeList:
                outputFile.write(lineOfCode.__str__())

            outputFile.write(line)
            line = inputFile.readline()
            
            for x in range(0, len(pointsList)):
                outputFile.write(pointsList[x].__str__())
                line = inputFile.readline()
                
            while('/END' not in line):
                line = inputFile.readline()
        
        outputFile.write(line)
        line = inputFile.readline()

    outputFile.flush()
    outputFile.close()
    inputFile.close()

# --------------------------- changeRepeatingPoints -------------------------- #
"""
changeRepeatingPoints

Arguments: 
    pointsList - list of all coordinates currently in file
    currentNum - the current value to replace
    newNum     - the new value to use for replacement
    coordinate - the coordinate to change

Return
    pointsList - list of all coordinates currently in file

Description    - changeRepeatingPoints changes all points with a specified value
"""
def changeRepeatingPoints(pointsList, currentNum, newNum, coordinate):
    for i in range(0, len(pointsList)):
        if (coordinate == 'x'):
            if(pointsList[i].getX() == currentNum):
                pointsList[i].setX(newNum)

        elif(coordinate == 'y'):
            if(pointsList[i].getY() == currentNum):
                pointsList[i].setY(newNum)

        elif(coordinate == 'z'):
            if(pointsList[i].getZ() == currentNum):
                pointsList[i].setZ(newNum)
    
    return pointsList

# --------------------------------- copyHand --------------------------------- #
"""
copyHand

Arguments: 
    pointsList - list of all coordinates currently in file
    coordinate - the coordinate to change

Returns
    pointsList - list of all updated coordinates

Description: 
    copyHand will take the current coordinates and flip them for the other hand style
"""
def copyHand(pointsList, coordinate):
    for i in range(0, len(pointsList)):
        if (coordinate == 'x'):
            pointsList[i].setX(pointsList[i].getX()*-1)
            pointsList[i].setW(pointsList[i].getW()*-1)

        elif(coordinate == 'y'):
            pointsList[i].setY(pointsList[i].getY()*-1)
            pointsList[i].setP(pointsList[i].getP()*-1)

        elif(coordinate == 'z'):
            pointsList[i].setZ(pointsList[i].getZ()*-1)
            pointsList[i].setR(pointsList[i].getR()*-1)
    
    return pointsList

# ------------------------------- displayGrpah ------------------------------- #
"""
displayGrpah

Arguments: 
    pointsList - list of all coordinates currently in file
    title      - the name of the file

Description: 
    displayGrpah will generate a graphical view of the robots path of movement
"""
def displayGrpah(pointsLists, title):
    #Initialize graph
    fig = plt.figure()
    graph = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []

    #Get all points, store in plane
    for point in pointsLists:
        x.append(point.getX())
        y.append(point.getY())
        z.append(point.getZ())
        #graph.scatter(x, y, z)
    
    #Plot path and graph Labels
    graph.plot(x, y, z)
    graph.set_xlabel('X')
    graph.set_ylabel('Y')
    graph.set_zlabel('Z')
    plt.title(title)
    plt.show()

# -------------------------------- menuOptions ------------------------------- #
"""
menuOptions
Description - menuOptions displays a list of all options
"""
def menuOptions():
    print("1. Translate a point")
    print("2. Translate all points of a specified coordinate")
    print("3. Copy a cycle")
    print("4. Change repeating point of a specified coordinate")
    print("5. RH -> LH or LH -> RH")
    print("6. Display graph")
    print("7. Exit the program\n")
    logger.info("\n1. Translate a point\n2. Translate all points of a specified coordinate\n3. Copy a cycle\n4. Change repeating point of a specified coordinate\n5. RH -> LH or LH -> RH\n6. Display graph\n7. Exit the program")

# -------------------------------- validateNum ------------------------------- #
"""
validateNum
Arguments: 
    phrase  - The main message sent to user
    focus   - The variable trying to be obtained
    lower   - the lower bound
    upper   - the upper bound

Return
    num     - The number for input

Description - validateNum validates the user input ensuring that the number is a number and within its bounds
"""
def validateNum(phrase, focus, lower, upper):
    try:
        num = int(input(phrase))
        while num < lower or num > upper:
            print("Error: ", focus, " must enter ", lower, " to ", upper, ". Please try again.\n", sep='')
            logger.error(f"{focus} must enter {lower} to {upper}.")
            num = int(input(phrase))
        return num

    #Handle String Input -> rec
    except ValueError:
        print("ERROR:", focus, "must be an integer. Plase try agian.\n")
        logger.error(f"{focus} must be an integer.")
        return validateNum(phrase, focus, lower, upper)

# ---------------------------------------------------------------------------- #
#                                   Call Main                                  #
# ---------------------------------------------------------------------------- #
main()

# ------------------------------------ EOF ----------------------------------- #