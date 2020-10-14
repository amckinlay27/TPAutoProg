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
#                                     Point                                    #
# ---------------------------------------------------------------------------- #
class Point:
    numOfPoints = 0

    def __init__(self, num, uf, config, x, y, z, w, p, r):
        self.__num = num
        self.__uf = uf
        self.__config = config
        self.__x = x
        self.__y = y
        self.__z = z
        self.__w = w
        self.__p = p
        self.__r = r
        Point.numOfPoints += 1

    def getNum(self):
        return self.__num
    
    def getUf(self):
        return self.__uf

    def getConfig(self):
        return self.__config
    
    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getZ(self):
        return self.__z

    def getW(self):
        return self.__w
    
    def getP(self):
        return self.__p

    def getR(self):
        return self.__r

    def setNum(self, num):
        self.__num = num

    def setUf(self, uf):
        self.__uf = uf

    def setConfig(self, config):
        self.__config = config

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def setZ(self, z):
        self.__z = z

    def setR(self, r):
        self.__r = r

    def setP(self, p):
        self.__p = p

    def setW(self, w):
        self.__w = w

    def __str__(self):
        return "P[" + str(self.__num) + "]{\n   GP1:\n\t" + self.__uf + ", \t" + self.__config + "\n\tX =  " + str("{:.3f}".format(self.__x)) + "  mm,\tY =  " + str("{:.3f}".format(self.__y)) + "  mm,\tZ = " + str("{:.3f}".format(self.__z)) +"  mm,\n\tW = " + str("{:.3f}".format(self.__w)) + " deg,\tP = " + str("{:.3f}".format(self.__p)) + " deg,\tR = " + str("{:.3f}".format(self.__r)) + " deg\n};\n"
