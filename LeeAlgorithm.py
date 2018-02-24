'''
Created on Aug 25, 2017

@author: Carlos
'''
from __future__ import print_function
import numpy
import sys
import enum
from point import point

if __name__ == '__main__':
    pass

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def copyMap(Map):
    newMap = numpy.empty((len(Map), len(Map[0])), dtype=numpy.object)
    for i in range(len(Map)):
        for j in range(len(Map[0])):
            newMap[i][j] = Map[i][j]
    
    return newMap

def printMap(Map):

    print(' =  ', end='')
    for i in range(0, len(Map)):
        if i < 10:
            print (' ' + str(i), end='')
        else:
            print(i, end='')
    print()

    for i in range(0, len(Map)+2):
        print ("  ", end='')
    print()

    for x in range(len(Map[0])):
        if x < 10:
            print (' ' + str(x) + '  ', end='')
        else:
            print (str(x) + '  ', end='')
        for y in range(len(Map)):
            print (Map[y][x], end='')
        print()


def addComponent(x1, x2, y1, y2, cLetter, Map):
    print ("iin add componenct")
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            Map[i][j] = cLetter

def bubble(start, Map):

    workingPoints = []
    workingPoints.append(start)
    found = False
    iteration = 0
    temp = []
    c = 0
    iFound = None
    #sys.exit(0)
    while found is False:

        # print("iteration: " + str(iteration))
        
        for each in workingPoints:

            #print ("Working Point X: " + str(each.X) + " Y: " +str(each.Y))
            
            directions = []

            directions.append(point(each.X, each.Y - 1))  # above
            directions.append(point(each.X, each.Y + 1))  # below
            directions.append(point(each.X + 1, each.Y))  # right
            directions.append(point(each.X - 1, each.Y))  # left

            for dir in directions:

                if dir.X < 0 or dir.X > len(Map) - 1:
                    break
                if dir.Y < 0 or dir.Y >len(Map[0]) - 1:
                    break


                #print ("X: " + str(dir.X) + " Y: " +str(dir.Y))
                if Map[dir.X][dir.Y] == ' -':

                    if iteration < 10:
                        Map[dir.X][dir.Y] = " " + str(iteration)
                    #else:
                    #    Map[dir.X][dir.Y] =  str(iteration)
                    
                    temp.append(dir)
                    #print("----------------- True -------------------")

                if Map[dir.X][dir.Y] == ' T':
                    print (" Found at: "+ str(dir.X) + " , " + str(dir.Y))
                    found = True
                    iFound = iteration
                    break

        #=======================================================================
        # Here, if temp is empty, it means there are no more workingpoints
        # which means there is nowhere else to go and no path has been found.
        #=======================================================================
        workingPoints = temp
        temp = []

        #printMap(Map)
        #iteration += 1
        iteration = (iteration + 1) % 10

    return iFound, Map

def getNextPos(dir, cur, Map):
    
    #===========================================================================
    # UP = 0
    # RIGHT = 1
    # DOWN = 2
    # LEFT = 3
    #===========================================================================
    if dir == UP:
        nextX = cur.X
        nextY = cur.Y -1
    elif dir == RIGHT:
        nextX = cur.X +1
        nextY = cur.Y
    elif dir == DOWN:
        nextX = cur.X
        nextY = cur.Y +1
    elif dir == LEFT:
        nextX = cur.X -1
        nextY = cur.Y


    if nextX not in range(len(Map)) or nextY not in range(len(Map[0])):
        return -1, -1

    return nextX, nextY


def line (dir, current, label, Map):

    valid = True
    tracePoints = []
    tracePoints.append(current) # start by adding first point in line 

    #print ("starting line w/ label: " +str(label))

    while valid is True:

        expectedLabel = (label - 1) % 10

        nextX, nextY = getNextPos(dir, current, Map)
        nextLabel = Map[nextX][nextY][1]

        #print(type(nextLabel))
        #print ( "expectedLabeL: " + str(expectedLabel) + " vs  actualLabeL: " + str(nextLabel))

        if nextLabel is  'S':
            print("Glorious has been found")
            # tracePoints.append(point(nextX, nextY))      # uncomment to include S point
            return tracePoints, True # return points collected, and goalFound = True

        if nextLabel.isdigit():

            nextLabel = int(nextLabel)

            if int(nextLabel) == expectedLabel:                tracePoints.append(point(nextX, nextY))
                current = point(nextX, nextY)
                label = nextLabel
            else:
                tracePoints += setDirection(current, label, Map)
                return tracePoints, True

        else:
            tracePoints += setDirection(current, label, Map)
            return tracePoints, True

def setDirection(turnPoint, label, Map):

    #print ("Looking for direction at: " + str(turnPoint.X) + " , " + str(turnPoint.Y))
    directions = [0, 1, 2, 3]
    dirFound = False
    dir = 0 # start looking above start point
    expectedLabel = (label - 1) % 10
    tracePoints = []
    linePoints = []
    goalFound = False

    # while dirFound is False:
    for dir in directions:

        #print ("dir: " + str(dir))

        startX, startY = getNextPos(dir, turnPoint, Map)
        actualLabel = Map[startX][startY][1]
        # print (type(actualLabel))

        #print ("start X and Y: " + str(startX) + ", " + str(startY))
        #print ("actualLabel: " + str(actualLabel))

        if startX == -1:  # if next point exceeds limits, then try next direction
            print ("exceeds limits")
            continue

        if not actualLabel.isdigit():  # if next point is not a number, then we cannot go through it, and try next direction
            print (" not number")
            continue
        else:
            actualLabel = int(actualLabel)

        if actualLabel != expectedLabel: #if next point is not a step closer to the origin, try next direction
            print ("expectedLabel: " + str(expectedLabel))
            continue

        # print ("Success!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        linePoints, goalFound = line(dir, point(startX, startY), actualLabel, Map)
        # print("size of linepoitns reutrned: " + str(len(linePoints)))
        tracePoints += linePoints

        if goalFound is True:
            print ("Set Direction has been found part")
            break

    return tracePoints


def trace(end, label, Map):
    
    print ("in trace method")
    tracePoints = setDirection(end, label, Map)
    
    return tracePoints

def orderSets(S, T):

    print ("in order sets")
    pinsInBox = [0] * len(S)
    for i, each in enumerate(S):

        for j in range(len(S) - 1):

            j = (i + j + 1) % len(S)

            xs = S[i].X
            ys = S[i].Y
            xt = T[i].X
            yt = T[i].Y

            #===================================================================
            # print ("looking at point with coordinates")
            # print ("S "  + str(xs) + " " + str(ys))
            # print("T " + str(xt)+ " " + str(yt))
            #===================================================================

            if xs > xt:
                stepX = -1
            else:
                stepX = 1

            if ys > yt:
                stepY = -1
            else:
                stepY = 1

            if S[j].X in range(xs, xt + stepX, stepX) and S[j].Y in range(ys, yt + stepY, stepY):
                pinsInBox[i] += 1

            if T[j].X in range(xs, xt + stepX, stepX) and T[j].Y in range(ys, yt + stepY, stepY):
                pinsInBox[i] += 1

    for idx, p in enumerate(pinsInBox):
        print( "Set "+str(idx)+ " has inside of it pins: " +str(p))

    #===========================================================================
    # Insert Sort, Depending on whteher i want to maintain the pins initial IDs,
    # The part inside the if clause should change so as to only keep track of the order
    # and not actually move the pinds around
    #===========================================================================

    for index, each in enumerate(pinsInBox):
        while index > 0:
            if pinsInBox[index] < pinsInBox[index - 1]:

                pinsInBox[index], pinsInBox[index - 1] = pinsInBox[index - 1], pinsInBox[index]

                S[index], S[index - 1] = S[index - 1], S[index]
                T[index], T[index - 1] = T[index - 1], T[index]

            index += -1
    #===========================================================================
    # print( "_--------")
    # for each in pinsInBox:
    #     print (each)
    # for i in range(len(S)):
    #     print(str(S[i].X) + "  " + str(S[i].Y))
    #     print(str(T[i].X) + "  " + str(T[i].Y))
    #===========================================================================
    # sys.exit(0)

    return S, T


def findPinWall(surrounding):

    up = 0
    down = 0
    left = 0
    right = 0

    for i, each in enumerate(surrounding):
        if each == ' o':
            if i == 0 or i == 1 or i == 2:
                up += 1
            if i == 2 or i == 5 or i == 8:
                right += 1
            if i == 6 or i == 7 or i == 8:
                down += 1
            if i == 0 or i == 3 or i == 6:
                left += 1

    directions = up, right, down, left

    return directions.index(max(directions))


def extendPins(Pins, Map):

    extension = 2

    for pin in Pins:
        
        surrounding = []

        for j in range(pin.Y - 1, pin.Y + 2):
            for i in range(pin.X - 1, pin.X + 2):
                surrounding.append(Map[i][j])

        wallDir = findPinWall(surrounding)

        extendDir = (wallDir + 2) % 4

        for i in range(0, extension):
            if extendDir == UP:
                Map[pin.X][pin.Y - i] = ' o'
            elif extendDir == RIGHT:
                Map[pin.X + i][pin.Y] = ' o'
            elif extendDir == DOWN:
                Map[pin.X][pin.Y + i] = ' o'
            elif extendDir == LEFT:
                Map[pin.X - i][pin.Y] = ' o'

        if extendDir == 0:
                pin.setY(pin.Y - (extension))
        elif extendDir == 1:
                pin.setX(pin.X + (extension))
        elif extendDir == 2:
                pin.setY(pin.Y + (extension))
        elif extendDir == 3:
                pin.setX(pin.X - (extension))
                
def addCushion(Map):
    
    Map[48][39] = ' i'




print("Here")
#Map = numpy.empty((50, 40), dtype=numpy.object)
Map = numpy.empty((80, 50), dtype=numpy.object)
Map.fill(' -')

'''
addComponent(10, 20, 10, 20, ' o', Map)
printMap(Map)
S1 = point(13, 9)
S2 = point(17, 9)
S3 = point(13, 21)
S4 = point(17, 21)
S5 = point(9, 15)
S6 = point(21, 15)

Ss = []
Ss.append(S1)
Ss.append(S2)
Ss.append(S3)
Ss.append(S4)
Ss.append(S5)
Ss.append(S6)
'''
'''
# Start Points
S1 = point(2, 2)
S2 = point(33, 3)
S3 = point(5, 16)
S4 = point(10, 25)
S5 = point(13, 20)
S6 = point(5, 5)
  
# Terminal Points
T1 = point(23, 23)
T2 = point(10, 10)
T3 = point(33, 29)
T4 = point(39, 29)
T5 = point(26, 6)
T6 = point(34, 8)
  
Ss = []
Ss.append(S1)
Ss.append(S2)
Ss.append(S3)
Ss.append(S4)
Ss.append(S5)
Ss.append(S6)
  
Ts = []
Ts.append(T1)
Ts.append(T2)
Ts.append(T3)
Ts.append(T4)
Ts.append(T5)
Ts.append(T6)
'''

addComponent(60, 68, 5, 13, ' o', Map)
addComponent(45, 51, 10, 20, ' o', Map)
addComponent(35, 48, 27, 33, ' o', Map)
addComponent(7, 13, 18, 27, ' o', Map)
addComponent(47, 60, 40, 47, ' o', Map)

printMap(Map)

#Start Points Isaac's Schematic
S1 = point(14, 20)
S2 = point(14, 25)
S3 = point(49, 27)
S4 = point(49, 29)
S5 = point(49, 31)
S6 = point(49, 33)
S7 = point(52, 12)
S8 = point(59, 7)
S9 = point(59, 5)

#End Points Isaac
T1 = point(34, 29)
T2 = point(34, 31)
T3 = point(52, 14)
T4 = point(52, 16)
T5 = point(58, 39)
T6 = point(52, 39)
T7 = point(59, 9)
T8 = point(55, 2)
T9 = point(57, 2)

Ss = []
Ss.append(S1)
Ss.append(S2)
Ss.append(S3)
Ss.append(S4)
Ss.append(S5)
Ss.append(S6)
Ss.append(S7)
Ss.append(S8)
Ss.append(S9)

Ts = []
Ts.append(T1)
Ts.append(T2)
Ts.append(T3)
Ts.append(T4)
Ts.append(T5)
Ts.append(T6)
Ts.append(T7)
Ts.append(T8)
Ts.append(T9)

printMap(Map)

extendPins(Ss, Map)
extendPins(Ts, Map)

printMap(Map)
s2, t2 = orderSets(Ss, Ts)

for i in range(len(Ss)):
    Map[Ss[i].X][Ss[i].Y] = 'S' + str(i+1)
    Map[Ts[i].X][Ts[i].Y] = 'T' + str(i+1)

printMap(Map)

for i in range(len(Ss)):

    print ("Now working on map " + str(i))
    WorkMap = copyMap(Map)

    WorkMap[Ss[i].X][Ss[i].Y] = ' S'
    WorkMap[Ts[i].X][Ts[i].Y] = ' T'
    
    addCushion(WorkMap)

    # printMap(Map)

    iFound, WorkMap = bubble(Ss[i], WorkMap)

    printMap(WorkMap)

    points = trace(Ts[i], iFound, WorkMap)

    for p in points:
        #Map[p.X][p.Y] = str(i) +'c'
        Map[p.X][p.Y] = 'c'+ str(i + 1)

    printMap(Map)
    
    

printMap(Map)




