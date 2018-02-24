'''
Created on Sep 28, 2017

@author: Carlos
'''

from Map import Map
from Map import Component
from Map import Pin
from Map import Trace
from Map import Net
from Map import PseudoPair
import sys
import time

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def route(Map, outputFile):
    component_cushion = 2
    trace_cushion = 1
    '''
    for pin in Map.start_pins:
        #print (pin.pos)
        extendPin(Map, pin, 2)
        print (pin.name, pin.extension)
        #print (pin.pos)


    for pin in Map.terminal_pins:
        #print (pin.pos)
        extendPin(Map, pin, 2)
        print (pin.name, pin.extension)
        #print (pin.pos)
    '''
    routed_dict = {}
    routed_amt = 0
    for net in Map.nets:
        for pin in net.pins:
            extendPin(Map, pin, 2)
            #make routed dictionary
            routed_dict[pin.component+pin.name] = 0
        
    
    #Net pre-processing (determining hub for 3+ nets, net bounding box order.)
    print (routed_dict)
    printMap(Map.space)
    pseudoPairs = orderSets(Map)

    printMap(Map.space)

    #####################################################
    # Rotuing process
    #####################################################
    traces = []
    routedPairs = []
    while routed_amt < len(routed_dict):
        WorkMap = makeWorkMap(Map.space)
        
        pair = pseudoPairs.pop(0)
        print ( pair.type, pair.pin.name, pair.terminal.name, pair.pinsInside, pair.netSize)
        
        if pair.type == "p2p":
            
            sx = pair.pin.x
            sy = pair.pin.y
            tx = pair.terminal.x
            ty = pair.terminal.y
            
            coords = (sx, sy, tx, ty)
        
            WorkMap[sx][sy] = ' S'
            WorkMap[tx][ty] = ' T'

        printMap(WorkMap)


        print ("ADD CUSHION for set ", pair.pin.net.name )
        WorkMap = addCushion(Map, component_cushion, WorkMap, pair.pin.net)
        printMap(WorkMap)
        print ("ADD TRACE CUSHION for set ", pair.pin.net.name)
        WorkMap = addTraceCushion(traces, trace_cushion, WorkMap, coords)
        printMap(WorkMap)
        iFound, WorkMap = bubble(pair.pin.pos, WorkMap)

        printMap(WorkMap)

        points = trace(pair.terminal.pos, iFound, WorkMap)
        #traces list needs more information for being able to remove
        # parts of traces that are ripped up
        traces.append(points)
        drawTrace(points, Map)

        printMap(Map.space)

        sys.exit()

    printMap(Map.space)
    printMapFile(Map.space, outputFile)
    

def makeNetQueue(netlist):
    x= 2
    
    
def step(p1, p2):

    if p1 < p2:
        step = 1
    else:
        step = -1

    return step


def addTraceCushion(traces, cushion, WorkMap, coords):

    for points in traces:
        id = 0
        while id < len(points) - 1:
            start = points[id]
            end = points[id+1]
            p1 = (min(start[0],end[0]), min(start[1],end[1]))
            p2 = (max(start[0],end[0]), max(start[1],end[1]))

            x_left = p1[0] - cushion
            x_right = p2[0] + cushion + 1
            y_top = p1[1] - cushion
            y_bottom = p2[1] + cushion + 1

            for y in range(y_top, y_bottom):
                for x in range(x_left, x_right):
                    if (x, y) == (coords[0], coords[1]) or (x, y) == (coords[2], coords[3]):
                        WorkMap[x-1:x+1, y-1:y+1] = ' -'
                        continue
                    WorkMap[x][y] = ' o'

            id += 1

    return WorkMap


def drawTrace(points, Map):
    i = 0
    id = 0
    while id < len(points) - 1:
        current = points[id]
        next = points[id+1]
        for x in range(current[0], next[0] + step(current[0],next[0]) , step(current[0],next[0])):
            for y in range(current[1], next[1] + step(current[1], next[1]), step(current[1], next[1])):
                Map.space[x][y] = 'c' +str(i+1)
        id += 1

    Map.space[points[0][0]][points[0][1]] = 'T' + str(i + 1)
    Map.space[points[id][0]][points[id][1]] = 'S' + str(i + 1)


def addCushion(MapInfo, cushion, WorkMap, current_net):
    """ Add a cushion to components of a certain amount of millimeters to
        avoid routing too close to components.

    MapInfo -- Map class object containing information about components.
    cushion -- int, millimeter amount of cushion to add to components.
    WorkMap -- list (Two-dimensional), array to add cushion to.
    current_net -- net object currently being routed

    WorkMap -- list (Two-dimensional), map space with cushion added to components.
    """

    #Cushion Components
    '''This might need to only be done once at the beginning of routing process...
    '''
    for component in MapInfo.components:
        x_left = component.x - cushion
        x_right = component.x + component.x_size + cushion
        y_top = component.y - cushion
        y_bottom = component.y + component.y_size + cushion

        for y in range(y_top, y_bottom):
            for x in range(x_left, x_right):
                WorkMap[x][y] = ' o'

    #Cushion Pins
    for net in MapInfo.nets:
        
        if net == current_net:
            continue
        
        for pin in net.pins:
           
            x_left = pin.x - 1
            x_right = pin.x + 1
            y_top = pin.y - 1
            y_bottom = pin.y + 1
 
            for y in range(y_top, y_bottom + 1):
                for x in range(x_left, x_right + 1):
                    WorkMap[x][y] = ' o'
 
    return WorkMap


def trace(end, label, Map):
    """ Make a trace from a terminal (end) pin. This method is simply
        a wrapper for the main process, setDirection(), for making a
        trace thorugh a map given its full wave propagation map.

    end -- tuple, point on map in which we are starting the trace from.
    label -- int, wave propagation number of current point.
    Map -- type must be list (Two-dimensional). Wave propagation map.

    tracepoints -- list of tuples containing coordinates of points on trace
    """

    tracePoints = setDirection(end, label, Map)
    print (tracePoints)

    return tracePoints


def setDirection(turnPoint, label, Map):
    """ Set the direction of a line we are going to traverse the map with.
        Will recursively be called through its call to line. setDirection checks
        which direction to go from a point at which we must change direction.
        line() then traverses on a straight line unitl it must change direction
        and calls setDirection() again.

    turnPoint -- tuple, point on map in which we are looking for a direction to turn
    label -- int, wave propagation number of current point.
    Map -- type must be list (Two-dimensional). Wave propagation map.

    tracepoints -- list of tuples containing coordinates of points on trace
    """

    directions = [0, 1, 2, 3]
    expectedLabel = (label - 1) % 10
    tracePoints = []
    linePoints = []
    goalFound = False

    tracePoints.append(turnPoint)

    for dir in directions:

        startX, startY = getNextPos(dir, turnPoint, Map)
        actualLabel = Map[startX][startY][1]

        if Map[startX][startY][0] is not ' ':
            continue

        if actualLabel == 'S':
            print ("Goal found in setDirection()")
            tracePoints.append((startX, startY))
            break

        if startX == -1:
            print ("next point exceeds limits of Map")
            continue

        if not actualLabel.isdigit():
            print ("next point is not a number")
            continue
        else:
            actualLabel = int(actualLabel)

        if actualLabel != expectedLabel:
            print ("actuallabel: ", str(actualLabel),
                   "expectedLabel: ", str(expectedLabel))
            continue

        # =======================================================================
        # If none of the previous conditions are true, then a valid direction
        # has been found and line() is called starting from the first point in
        # that direction.
        # =======================================================================
        print ("current point is: ", startX, startY)
        linePoints, goalFound = line(dir, (startX, startY), actualLabel, Map)
        tracePoints += linePoints

        if goalFound is True:  # If the terminal pin has been found in line()
            break

    return tracePoints


def line(dir, current, label, Map):
    """ Extend a line through map using the wave propagation numbers
        as a guide.

    dir -- direction line extends.
    current -- type tuple, current point we are traversing through.
    label -- type int, wave propagation number of current point.
    Map -- type must be list (Two-dimensional). Wave propagation map.

    tracepoints -- list of tuples containing coordinates of points on trace
    """

    tracePoints = []
    #tracePoints.append(current)  # start by adding first point in line

    while True:
        expectedLabel = (label - 1) % 10

        nextX, nextY = getNextPos(dir, current, Map)
        nextLabel = Map[nextX][nextY][1]

        if nextLabel is 'S':
            tracePoints.append((nextX, nextY))  # uncomment to include S point
            return tracePoints, True  # return points collected and goalFound = True

        if nextLabel.isdigit():

            nextLabel = int(nextLabel)

            if int(nextLabel) == expectedLabel:
                # tracePoints.append((nextX, nextY)) # uncomment to get points in line
                current = (nextX, nextY)
                label = nextLabel
            else:
                tracePoints += setDirection(current, label, Map)
                return tracePoints, True

        else:
            tracePoints += setDirection(current, label, Map)
            return tracePoints, True


def getNextPos(dir, cur, Map):
    """ Get the x and y coordinates of a point next to a given point in the
        given direction.

    dir -- int, direction of point we want from current point.
    cur -- tuple, current point.
    Map -- type must be list (Two-dimensional).

    nextX -- int, x-coordinate of point dir from cur.
    nextY -- int, y_coordinate of point dir from cur.
    """

    x = cur[0]
    y = cur[1]

    if dir == UP:
        nextX = x
        nextY = y - 1
    elif dir == RIGHT:
        nextX = x + 1
        nextY = y
    elif dir == DOWN:
        nextX = x
        nextY = y + 1
    elif dir == LEFT:
        nextX = x - 1
        nextY = y

    if nextX not in range(len(Map)) or nextY not in range(len(Map[0])):
        return -1, -1

    return nextX, nextY





def makeWorkMap(Map):
    """ Copy Two-Dimensional list used as map for performing searches.

    Map -- must be type list (Two-Dimensional)

    newMap -- list type, exact copy of Map.
    """

    newMap = []
    for i in range(len(Map)):
        newMap.append([])
        for j in range(len(Map[0])):
            newMap[i].append(Map[i][j])
    return newMap


def orderSets(Map):
    """ Order pin pairs for routing using bounding box heuristic. The bounding box
        of a pair counts how many other pins lie within the box made from xS to
        xT and yS to yT. Map.start_pins and Map.terminal_pins are modified
    
    Map -- Map type object contatining entire information of routing space, components, pins, nets etc

    pseudoPins -- list containing information on order pins will be routed next.
    """
    pseudopairs = []        
    
    for net in Map.nets:
        pins = net.pins
        if len(pins) == 2:
            
            bbox_idx = calculatePinsInBBox(net, 0, 1, Map)
            pseudopair = PseudoPair("p2p",pins[0], pins[1], bbox_idx, net.size)
            pseudopairs.append(pseudopair)
            
        elif len(pins) > 2:
            for i in range(len(pins)):
                for j in range(i,len(pins)):
                    
                    if pins[i] == pins[j]:
                        continue
                    
                    bbox_idx = calculatePinsInBBox(net, i, j, Map)
                    pseudopair = PseudoPair("p2p",pins[i], pins[j], bbox_idx, net.size)
                    pseudopairs.append(pseudopair)
            
    for pair in pseudopairs:
        print (pair.type, pair.pin.name, pair.terminal.name, pair.pinsInside, pair.netSize)
    pseudopairs.sort(key=lambda bbox : bbox.pinsInside)        
    for pair in pseudopairs:
        print (pair.type, pair.pin.name, pair.terminal.name, pair.pinsInside, pair.netSize)
                   
    #sys.exit()
    
    return pseudopairs

    '''
    for i in range(len(S)):
        Map.space[S[i].x][S[i].y] = 'S' + str(i+1)
        S[i].id = i
        Map.space[T[i].x][T[i].y] = 'T' + str(i+1)
        T[i].id = i
    
    return S, T
    '''
    
def calculatePinsInBBox(net,p1,p2, Map):
    
    bbox_idx = 0
    p1 = net.pins[p1]
    p2 = net.pins[p2]
    
    for net2 in Map.nets:
        if net == net2:
            continue
        #print ("iter:"+net2.name) 
        pins2 = net2.pins

        for pin2 in pins2:
    
            if (pin2.x in range(p1.x, p2.x + step(p1.x, p2.x), step(p1.x, p2.x)) and
                    pin2.y in range(p1.y, p2.y + step(p1.y, p2.y), step(p1.y, p2.y))):
                bbox_idx += 1
    
    return bbox_idx

def findPinWall(Map, pin):
    """ Determines where the component a pin is connected to is located in
        relation to the pin.

    Map -- type must be list (Two-dimensional).
    pin -- type must be Pin object.

    return -- integer dicating direction of component wall in relation to pin.
              returns -1 if it has no wall.
    """

    surrounding = []

    for j in range(pin.y - 1, pin.y + 2):
        for i in range(pin.x - 1, pin.x + 2):
            surrounding.append(Map.space[i][j])

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

    if max(directions) < 2:
        return -1

    return directions.index(max(directions))


def extendPin(Map, pin, e_length):
    """ Create extension on pin from component.

    Map -- type must be list (Two-dimensional).
    pin -- type must be Pin object.
    e_length -- integer dictating millimeters pin will be extended.
    """

    wallDir = findPinWall(Map, pin)

    # if pin has no wall, it is not extended
    if wallDir == -1:
        return

    # extends in the diretion opposite of component
    extendDir = (wallDir + 2) % 4

    for i in range(0, e_length):
        if extendDir == UP:
            Map.space[pin.x][pin.y - i] = ' o'
        elif extendDir == RIGHT:
            Map.space[pin.x + i][pin.y] = ' o'
        elif extendDir == DOWN:
            Map.space[pin.x][pin.y + i] = ' o'
        elif extendDir == LEFT:
            Map.space[pin.x - i][pin.y] = ' o'

    if extendDir == 0:
            pin.setY(pin.y - e_length)
            Map.space[pin.x][pin.y] = pin.name
    elif extendDir == 1:
            pin.setX(pin.x + e_length)
            Map.space[pin.x][pin.y] = pin.name
    elif extendDir == 2:
            pin.setY(pin.y + (e_length))
            Map.space[pin.x][pin.y] = pin.name
    elif extendDir == 3:
            pin.setX(pin.x - (e_length))
            Map.space[pin.x][pin.y] = pin.name

    pin.extension = e_length


def bubble(start, Map):
    """ Perform wave propagation portion of Lee Algorithm for routing.

    start -- Tuple containing coordinate of start Pin.
    Map -- type must be list (Two-dimensional).

    iteration_found_at -- integer dictating wave propagation number end
                          terminal was found at.
    Map -- updated list (Two-dimensional) map with wave propagation performed on it.
    """

    found = False
    iteration = 0
    temp = []
    iteration_found_at = None
    workingPoints = []
    workingPoints.append(start)

    while found is False:

        for each in workingPoints:

            directions = []
            directions.append((each[0], each[1] - 1))  # above
            directions.append((each[0], each[1] + 1))  # below
            directions.append((each[0] + 1, each[1]))  # right
            directions.append((each[0] - 1, each[1]))  # left

            for dir in directions:

                x = dir[0]
                y = dir[1]

                if x < 0 or x > len(Map) - 1:
                    continue
                if y < 0 or y > len(Map[0]) - 1:
                    continue

                    print (x, y)
                if Map[x][y] == ' -':
                    Map[x][y] = " " + str(iteration)
                    temp.append(dir)

                if Map[x][y] == ' T':
                    print (" Found at: " + str(x) + " , " + str(y))
                    found = True
                    iteration_found_at = iteration
                    break

        # =======================================================================
        # Here, if temp is empty, it means there are no more workingpoints
        # which means there is nowhere else to go and no path has been found.
        # =======================================================================
        workingPoints = temp
        temp = []

        iteration = (iteration + 1) % 10

    return iteration_found_at, Map


def printMap(Map):
    """Print Map given in console.

    Map -- must be list (Two-dimensional) type
    """

    # Print column number line
    print(' =  ', end='')
    for i in range(0, len(Map)):
        if i < 10:
            print (' ' + str(i), end='')
        else:
            print(i, end='')
    print()

    # Print extra line
    for i in range(0, len(Map) + 2):
        print ("  ", end='')
    print()

    # Print Map with row number
    for x in range(len(Map[0])):
        if x < 10:
            print (' ' + str(x) + '  ', end='')
        else:
            print (str(x) + '  ', end='')
        for y in range(len(Map)):
            print (Map[y][x], end='')
        print()
        
def printMapFile(Map, outputFile):
    """Print Map given in console.

    Map -- must be list (Two-dimensional) type
    """
    outputFile = open(outputFile, "w+")
    
    # Print column number line
    outputFile.write(' =  ')
    for i in range(0, len(Map)):
        if i < 10:
            outputFile.write('  ' + str(i))
        elif i > 9 and i < 100:
            outputFile.write(' ' + str(i))
        else:
            outputFile.write(str(i))
    outputFile.write('\n')

    # Print Map with row number
    for x in range(len(Map[0])):
        if x < 10:
            outputFile.write(' ' + str(x) + '  ')
        else:
            outputFile.write(str(x) + '  ')
        for y in range(len(Map)):
            outputFile.write(' ' + Map[y][x])
        outputFile.write('\n')
    
    
    
                