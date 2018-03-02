'''
Created on Sep 21, 2017

@author: Carlos
'''
from Map import PseudoPair
import Router
import SearchAlgorithms as SA
import MapPrinter as MP
import sys

def orderSets(Map):
    """ Order pin pairs for routing using bounding box heuristic. The bounding box
        of a pair counts how many other pins lie within the box made from xS to
        xT and yS to yT. Map.start_pins and Map.terminal_pins are modified
    
    Map -- Map type object containing entire information of routing space, components, pins, nets etc

    pseudoPins -- list containing information on order pins will be routed next.
    """
    pseudopairs = []        
    multinets = []
    bbox_minimum = 10000

    for net in Map.nets:
        pins = net.pins
        if len(pins) == 2:
            
            if pins[0].routed:
                continue
            
            bbox_idx = calculatePinsInBBox(net, 0, 1, Map, "p2p")
            pseudopair = PseudoPair("p2p",pins[0], pins[1], bbox_idx, net.size)
            pseudopairs.append(pseudopair)
            
            if bbox_idx < bbox_minimum:
                bbox_minimum = bbox_idx

        elif len(pins) > 2:
            multinets.append(net)
            
    for net in multinets:
        mn_min = (-1, -1, 10000)
        pins = net.pins
        for i in range(len(pins)):
            for j in range(i, len(pins)):
                
                if pins[i] == pins[j] or pins[i].routed:
                    continue
                
                bbox_idx = calculatePinsInBBox(net, i, j, Map, "p2p")
                
                if bbox_idx < bbox_minimum:
                    mn_min = (i,j,bbox_idx)    
                    break
                
                if bbox_idx < mn_min[2]:
                    mn_min = (i,j,bbox_idx )
            
            if bbox_idx < bbox_minimum:
                break
            
        pseudopair = PseudoPair("p2p",pins[mn_min[0]], pins[mn_min[1]],mn_min[2], net.size)
        pseudopairs.append(pseudopair)
    
    pseudopairs.sort(key=lambda bbox : bbox.pinsInside)        

    for pair in pseudopairs:
        print(pair.type, pair.pin.name, pair.terminal.name, pair.pinsInside, pair.netSize)
    
    return pseudopairs


def updateSets(net, pseudoPairs, Map):
    print (net.name)
    print (len(net.traces))

    if net.routed == 2:
        
        p1 = net.pins[0]
        p2 = net.pins[1]
        p3 = net.pins[2]
        
        WorkMap1 = Router.makeWorkMap(Map.space)
        WorkMap1 = setGoalPositions(p3, WorkMap1, net)
        iFound, point_found, WorkMap = SA.bubble(p3, WorkMap1)
        MP.printMap(WorkMap1)
        bbox_idx = calculatePinsInBBox(net, 2, point_found, Map, "pos")

        pseudopair = PseudoPair("p2n", p3, net, bbox_idx, net.size)
        pseudoPairs.append(pseudopair)

        pseudoPairs.sort(key=lambda bbox: bbox.pinsInside)

        return pseudoPairs
        
        
def setGoalPositions(start_pin, WorkMap,net):
    
    for pin in net.pins:
        
        if pin == start_pin:
            continue
        
        WorkMap[pin.x][pin.y] = ' T'
    
    for trace in net.traces:
         
        points = trace.points
        id = 0
        while id < len(points) - 1:
            current = points[id]
            next = points[id+1]
            for x in range(current[0], next[0] + step(current[0],next[0]) , step(current[0],next[0])):
                for y in range(current[1], next[1] + step(current[1], next[1]), step(current[1], next[1])):
                    WorkMap[x][y] = ' T'
            id += 1
            
    MP.printMap(WorkMap)
    
    return WorkMap
        
def calculatePinsInBBox(net,p1,p2, Map, case):
    
    bbox_idx = 0
    p1 = net.pins[p1]
    p1x = p1.x
    p1y = p1.y

    if case == "p2p":
        p2 = net.pins[p2]
        p2x = p2.x
        p2y = p2.y
    else: 
        p2x = p2[0]
        p2y = p2[1]
        
    
    for net2 in Map.nets:
        if net == net2:
            continue
        pins2 = net2.pins

        for pin2 in pins2:
    
            if (pin2.x in range(p1x, p2x + step(p1x, p2x), step(p1x, p2x)) and
                    pin2.y in range(p1y, p2y + step(p1y, p2y), step(p1y, p2y))):
                bbox_idx += 1
    
    return bbox_idx
        
        
def step(p1, p2):

    if p1 < p2:
        step = 1
    else:
        step = -1

    return step

