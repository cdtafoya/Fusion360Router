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
from Map import Trace
import MapPrinter as MP
import SearchAlgorithms as SA
import OrderSets
import sys
import time

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
component_cushion = 2


def route(Map, outputFile):
    component_cushion = 2
    trace_cushion = 1
  
    routed_dict = {}
    routed_amt = 0
    for net in Map.nets:
        for pin in net.pins:
            extendPin(Map, pin, 2)
            #make routed dictionary
            routed_dict[pin.component+pin.name] = 0
        
    
    #Net pre-processing (determining hub for 3+ nets, net bounding box order.)
    print (routed_dict)
    MP.printMap(Map.space)
    #pseudoPairs = orderSets(Map)

    MP.printMap(Map.space)

    #####################################################
    # Rotuing process
    #####################################################
    traces = []
    routedPairs = []
    pseudoPairs = []
    trace_code = 0
    pseudoPairs = OrderSets.orderSets(Map)
    

    while routed_amt < len(routed_dict):
                
        WorkMap = makeWorkMap(Map.space)
        
        pair = pseudoPairs.pop(0)
        print ( pair.type, pair.pin.name, pair.terminal.name, pair.pinsInside, pair.netSize)
        
        if pair.type == "p2p":
            
            sx = pair.pin.x
            sy = pair.pin.y
            tx = pair.terminal.x
            ty = pair.terminal.y
            
            WorkMap[sx][sy] = ' S'
            WorkMap[tx][ty] = ' T'
            
        #elif pair.type == "p2n":

        MP.printMap(WorkMap)

        #Add Cushiom
        print ("ADD CUSHION for set ", pair.pin.net.name )
        WorkMap = addCushion(Map, component_cushion, WorkMap, pair.pin.net)
        MP.printMap(WorkMap)
        print ("ADD TRACE CUSHION for set ", pair.pin.net.name)
        WorkMap = addTraceCushion(Map, trace_cushion, WorkMap, pair)
        MP.printMap(WorkMap)
        
        iFound, _ ,  WorkMap = SA.bubble(pair.pin, WorkMap)
        print ("IFOUND: " + str(iFound))
        MP.printMap(WorkMap)
        points = makeTrace(pair, iFound, WorkMap)
        #traces list needs more information for being able to remove
        # parts of traces that are ripped up
        
        new_trace = Trace(points, hex(trace_code), pair)
        pair.addTrace(new_trace)
        Map.addTrace(new_trace)
        pair.pin.net.addTrace(new_trace)
        trace_code += 1
        drawTrace(new_trace, Map)

        MP.printMap(Map.space)

        pair.setRouted()
        if pair.netSize > 2:
            pseudoPairs = OrderSets.updateSets(pair.pin.net, pseudoPairs, Map)
        
        routedPairs.append(pair)
        routed_amt += 2
        #sys.exit()

    MP.printMap(Map.space)
    MP.printMapFile(Map.space, outputFile)
    for trace in Map.traces.keys():
        print (trace)
        #print (len(Map.traces))
        #print (trace.points)
    for pair in routedPairs:
        print(pair.pin.name)
        print (pair.trace.points)
        
    point = (21,31) 
    #deleteTrace(point, Map)
    
    for trace in Map.traces.keys():
        print (trace)
    
def deleteTrace(point, Map):
    
    trace_code = Map.space[point[0]][point[1]]
    print (trace_code)
    trace = Map.traces[trace_code]
    
    pair = trace.pseudoPair
    
    pair.unsetRouted()
    trace.pair.pin.net.deleteTrace(trace)
        
    del Map.traces[trace_code]
 

def step(p1, p2):

    if p1 < p2:
        step = 1
    else:
        step = -1

    return step


def addTraceCushion(MapInfo, cushion, WorkMap, pair):
    
    sx = pair.pin.x
    sy = pair.pin.y
    tx = pair.terminal.x
    ty = pair.terminal.y
    
    for trace in MapInfo.traces.values():
        id = 0
        while id < len(trace.points) - 1:
            start = trace.points[id]
            end = trace.points[id+1]
            p1 = (min(start[0],end[0]), min(start[1],end[1]))
            p2 = (max(start[0],end[0]), max(start[1],end[1]))

            x_left = p1[0] - cushion
            x_right = p2[0] + cushion + 1
            y_top = p1[1] - cushion
            y_bottom = p2[1] + cushion + 1

            for y in range(y_top, y_bottom):
                for x in range(x_left, x_right):
                    if (x, y) == (sx, sy) or (x, y) == (tx, ty):
                        WorkMap[x-1:x+1, y-1:y+1] = ' -'
                        continue
                    WorkMap[x][y] = ' o'

            id += 1

    return WorkMap


def drawTrace(trace, Map):
    points = trace.points
    id = 0
    while id < len(points) - 1:
        current = points[id]
        next = points[id+1]
        for x in range(current[0], next[0] + step(current[0],next[0]) , step(current[0],next[0])):
            for y in range(current[1], next[1] + step(current[1], next[1]), step(current[1], next[1])):
                Map.space[x][y] = trace.code
        id += 1

    Map.space[trace.pseudoPair.pin.x][trace.pseudoPair.pin.y] = trace.pseudoPair.pin.name 
    Map.space[trace.pseudoPair.terminal.x][trace.pseudoPair.terminal.y] = trace.pseudoPair.terminal.name 
    #Map.space[points[0][0]][points[0][1]] = 'T' + str(i + 1)
    #Map.space[points[id][0]][points[id][1]] = 'S' + str(i + 1)


def addCushion(MapInfo, cushion, WorkMap, current_net):
    """ Add a cushion to components of a certain amount of millimeters to
        avoid routing too close to components.

    MapInfo -- Map class object containing information about components.
    cushion -- int, millimeter amount of cushion to add to components.
    WorkMap -- list (Two-dimensional), array to add cushion to.
    current_pair -- pair object currently being routed

    WorkMap -- list (Two-dimensional), map space with cushion added to components.
    """

    #Cushion Components
    '''This might need to only be done once at the beginning of routing process...
    '''
    
    #current_net = current_pair.pin.net
    print (current_net.name)
    
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


def makeTrace(pair, label, Map):
    """ Make a trace from a terminal (end) pin. This method is simply
        a wrapper for the main process, setDirection(), for making a
        trace thorugh a map given its full wave propagation map.

    end -- tuple, point on map in which we are starting the trace from.
    label -- int, wave propagation number of current point.
    Map -- type must be list (Two-dimensional). Wave propagation map.

    tracepoints -- list of tuples containing coordinates of points on trace
    """
    end = pair.terminal.pos
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
    expectedLabel = (label - 1)
    tracePoints = []
    linePoints = []
    goalFound = False

    tracePoints.append(turnPoint)

    for dir in directions:

        startX, startY = getNextPos(dir, turnPoint, Map)
        actualLabel = Map[startX][startY]
        #print ("ACTUAL LABEL: " + str(actualLabel), len(actualLabel))

        #if Map[startX][startY][0] is not ' ':
        #    continue

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
        expectedLabel = (label - 1)

        nextX, nextY = getNextPos(dir, current, Map)
        nextLabel = Map[nextX][nextY]

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


def findSTP(pin1, pin2, pin3, Map):
    
    #makes a map space with the area where optimal netting can be placed between to points
    #on the iteration back label as T or whatever is the final value the algorithm searches
    #for on the way back. 
    WorkMap = makeWorkMap(Map.space)
    WorkMap = addCushion(Map, component_cushion, WorkMap, pin1.net)
    MP.printMap(WorkMap)
    sys.exit()
    

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


