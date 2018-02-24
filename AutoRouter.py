'''
Created on Jul 29, 2017

@author: Carlos Tafoya
'''
from __future__ import print_function
import numpy
import sys
from point import point

global found
global mtPoint

if __name__ == '__main__':
    pass


def copyMap(Map):
    newMap = numpy.empty((len(Map), len(Map[0])), dtype=numpy.object)
    for i in range(len(Map)):
        for j in range(len(Map[0])):
            newMap[i][j] = Map[i][j]
    
    return newMap
    
    
def printMap2():

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

def verticalLine(c, p, PointName, Map):
    global found
    
    if PointName == 'S':
        dirX = 'h'
        dirY = 'v'
        intersect = 's'
        goaldirX = 'k'
        goal = 'T'
    else:
        dirX = 'k'
        dirY = 'u'
        intersect = 't'
        goaldirX = 'h'
        goal = 'S'

    vPoints = []

    line = []
    below = range(p.Y - 1, -1, -1)
    line.append(below)
    above = range(p.Y + 1, len(Map[0]), 1)
    line.append(above)

    for segment in line:
        for i in segment:

            if Map[p.X][i] != ' -':

                if dirX in Map[p.X][i]:
                    Map[p.X][i] = intersect + str(c)

                elif goaldirX in Map[p.X][i] or goal in Map[p.X][i]:
                    if goal in Map[p.X][i]:
                        found = True
                    Map[p.X][i] = ' +'
                    print (" Point found at: " + str(p.X) + " ," + str (i))
                    mtPoint.append(point(p.X, i))
                    print (Map[p.X][i])
                    print (mtPoint)
                    return -1

                else:
                    break

            else:
                Map[p.X][i] = dirY + str(c)
                vPoints.append(point(p.X, i))

    return vPoints


def horizontalLine(c, p, PointName, Map):
    global found

    if PointName == 'S':
        dirX = 'h'
        dirY = 'v'
        intersect = 's'
        goaldirY = 'u'
        goal = 'T'
    else:
        dirX = 'k'
        dirY = 'u'
        intersect = 't'
        goaldirY = 'v'
        goal = 'S'

    hPoints = []

    line = []
    left = range(p.X - 1, -1, -1)
    line.append(left)
    right = range(p.X + 1, len(Map), 1)
    line.append(right)

    for segment in line:
        for i in segment:
            if Map[i][p.Y] != ' -':

                if dirY in Map[i][p.Y]:
                    Map[i][p.Y] = intersect + str(c)

                elif goaldirY in Map[i][p.Y] or goal in Map[i][p.Y]:
                    print (" Point found at: " + str(i) + " ," + str(p.Y))
                    if goal in Map[i][p.Y]:
                        found = True
                    Map[i][p.Y] = ' +'
                    mtPoint.append(point(i, p.Y))
                    return -1

                else:
                    break

            else:
                Map[i][p.Y] = dirX + str(c)
                hPoints.append(point(i, p.Y))


    return hPoints

def getNextPos(dir, cur, Map):
    
    if dir == 0:
        nextX = cur.X
        nextY = cur.Y -1
    elif dir == 1:
        nextX = cur.X +1
        nextY = cur.Y
    elif dir == 2:
        nextX = cur.X
        nextY = cur.Y +1
    elif dir == 3:
        nextX = cur.X -1
        nextY = cur.Y


    if nextX not in range(len(Map)) or nextY not in range(len(Map[0])):
        return -1, -1

    return nextX, nextY

def mapIterator(i, goal, dir, Map):

    X, Y = getNextPos(dir, mtPoint[0], Map)
    current = point(X, Y)
    start = current
    curSym = Map[current.X][current.Y]
    print (curSym)
    print (goal)
    print (len(Map))

    if goal == "T":
        change = "t"
    else:
        change = "s"
        
    temp = []
    temp.append(current)
    path = []
    first = 0
    i  = 0
    while goal not in curSym: #and i < 29:
        #just add a counter for first time: in first time i only check one direction whatever dir is
        #if curSym == " +":
        #    return None
        
        print ("Current Symbol: " + curSym)
        print (goal)

        nextX, nextY = getNextPos(dir, current, Map)

        if nextX == -1 and first == 0:   #means we are on first line and reached the limit; meaning this line goes nowhere
            print ("HERE1")
            return []

        if nextX == -1:
            print ("HERE2")
            current = start
            temp = []
            temp.append(current)
            curSym = Map[current.X][current.Y]
            dir = (dir + 2) % 4
            continue

        nextSym = Map[nextX][nextY]

        if nextSym[0] in curSym  or nextSym[0] in change:
            current = point(nextX, nextY)
            temp.append(current)
        else:
            path = path + temp
            current = point(nextX, nextY)
            start = current
            temp = []
            first = 1
            temp.append(current)
            dir = (dir + 1) % 4

        curSym = Map[current.X][current.Y]
        
        i += 1
        
    print ("Current Symbol: " + curSym)
    path.append(current)
    return path

def findPath(Map):
    
    #===========================================================================
    # 1. AT Some point I will have to add a check for the End points being right next
    #     to the point of intersection.
    # 2. Also, for setting above, below right left, a check will need to be added for 
    #    points next to the edge, beyond the lenght and width of the array
    #===========================================================================
    poi = mtPoint[0]
    above = Map[poi.X][poi.Y - 1]
    below = Map[poi.X][poi.Y + 1]
    left = Map[poi.X - 1][poi.Y]
    right = Map[poi.X + 1][poi.Y]

    directions = []
    directions.append(above)
    directions.append(right)
    directions.append(below)
    directions.append(left)

    i = 0

    s = []
    
    options = {0: ['u', 'v'],
               1: ['h', 'k']}

    print (found)
    for dir, d in enumerate(directions):
        
        if found:
            if 'u' in d or 'k' in d:
                i = (i + 1) % 2
                continue

        print (d[0])
        print (options[i])
        if d[0] in ['u', 'k']:
            goal = "T"
        else:
            goal = "S"
        if d[0] in options[i]:
            s = s + mapIterator(i, goal, dir, Map)
        i = (i + 1) % 2

    return s
    
def Route(S, T, Map):
    global mtPoint
    global found
    mtPoint = []
    found = False
    #Initialize pilot Lines
   
    vs = verticalLine(0, S, 'S', Map)
    hs = horizontalLine(0, S, 'S', Map)
    vt = verticalLine(0, T, 'T', Map)
    ht = horizontalLine(0, T, 'T', Map)

    c = 1

    printMap(Map)


    jmp = 0
    while not mtPoint:

        print (" Iteration: " + str(c))

        htemp = []
        vtemp = []

        for p in vs:
            hPoints = horizontalLine(c, p, 'S', Map)
            if hPoints == -1:
                jmp = 1
                break
            htemp += hPoints

        if mtPoint:
            break
        
        for p in hs:
            if 's' not in Map[p.X][p.Y]:
                vPoints = verticalLine(c, p, 'S',Map)
                if vPoints == -1:
                    jmp = 1
                    break
                vtemp += vPoints

        if mtPoint:
            break
        
        vs = vtemp
        hs = htemp

        htemp = []
        vtemp = []
        #print ("vt")
        #for i in vt:
        #    print(str(i.X) + " , " + str (i.Y))
        for p in vt:
            hPoints = horizontalLine(c, p, 'T', Map)
            if hPoints == -1:
                jmp = 1
                break
            htemp += hPoints
        
        if mtPoint:
            break
        #print ("ht")
        #for i in ht:
        #    print(str(i.X) + " , " + str (i.Y))
        for p in ht:
            if 't' not in Map[p.X][p.Y]:
                vPoints = verticalLine(c, p, 'T', Map)
                if vPoints == -1:
                    jmp = 1
                    break
                vtemp += vPoints
            
        if mtPoint:
            break
        
        vt = vtemp
        ht = htemp

        printMap(Map)

        c += 1

    s = findPath(Map)
    
    return s
    print ("BEFORE")
    printMap(Map)
    Map = MapOriginal
    for each in s:
        Map[each.X][each.Y] = ' c'
    print ("AFTER")
    printMap(Map)
    
    
    

#===============================================================================
# Make an original Map -> make similar work map -> 
#2. Once route is found, update original -> reset owrk map wirh method       
#===============================================================================

# Map is (x,y) x wide and  y high
Map = numpy.empty((40, 30), dtype=numpy.object)

Map.fill(' -')

addComponent(16, 23, 3, 12, ' o', Map)
addComponent(11, 15, 16, 29, ' o', Map)
#addComponent(22, 30, 19, 26, ' o', Map)




MapOriginal = copyMap(Map)
#addComponent(16, 16, 10, 17, ' o')
#addComponent

S1 = point(5, 4)
T1 = point(34, 9)
Map[5][4] = 'S1'
Map[34][9] = 'T1'
Map[5][10] = "S2"
Map[27][7] = "T2"
printMap(Map)
s = Route(S1, T1, Map)

for each in s:
        MapOriginal[each.X][each.Y] = 'c1'

printMap(MapOriginal)
S2 = point(5, 10)
T2 = point(27, 7)

Map2 = copyMap(MapOriginal)
Map2[5][10] = " S"
Map2[27][7] = " T"
printMap(Map2)
s2 = Route(S2, T2, Map2)

for each in s2:
        MapOriginal[each.X][each.Y] = 'c2'

printMap(MapOriginal)

S3 = point(5, 22)
T3 = point(29, 25)

Map3 = copyMap(MapOriginal)
Map3[5][22] = " S"
Map3[29][25] = " T"
printMap(Map3)


s3 = Route(S3, T3, Map3)
for each in s3:
        MapOriginal[each.X][each.Y] = 'c3'
        
printMap(MapOriginal)
#addComponent(3, 3, 0, 13, ' o')
#addComponent(18, 26, 13, 13, ' o')
#addComponent(16, 16, 10, 17, ' o')





