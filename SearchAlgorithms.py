'''
Created on Feb 27, 2018

@author: Carlos
'''

import Router
import MapPrinter
import sys

def bubble(start_pin, Map):
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
    workingPoints.append(start_pin.pos)

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
                #print (x, y)

                if x < 0 or x > len(Map) - 1:
                    continue
                if y < 0 or y > len(Map[0]) - 1:
                    continue

                if Map[x][y] == '-':
                    Map[x][y] = str(iteration)
                    temp.append(dir)

                if Map[x][y] == 'T':
                    point_found = (x,y)
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

        iteration = (iteration + 1)

    return iteration_found_at, point_found, Map

def A_Star(start_pin, Map, end):

    node_map = initiate_map(Map) # array of cost of traveling to a node on map
    explored = initiate_explored_map(Map) # list of tuples defining if node has been examined

    #Distance List/Array. Have same values, distances is for quick lookup
    total, to_travel = initiate_distance_map(Map) #array
    distances = initiate_label_map(Map) #list

    parents = initiate_parent_map(Map)


    start = start_pin.pos
    distances.append([start, 0])
    #distances.append([0,0, float("inf")])
    explored[start] = False
    total[start[0]][start[1]] = manhattan_dist(start, end)
    to_travel[start[0]][start[1]] = 0
    distances = sorted(distances, key=lambda x: x[1])
    print(distances)

    '''
    for index, value in enumerate(distances):
        # Assuming y is in increasing order.
        if value['id'] > new_value['id']:
            y.insert(index, new_value)
            break
    '''

    MapPrinter.printMap(Map)
    count = 0
    while(True):

        found = False
        #find minimum v in distances that is also False in sptSet
        print ("looking thorugh dist 1st time:")
        for coord in distances:
            print (coord)
            if explored[coord[0]] == False:
                u = coord[0]
                distances.remove(coord)
                break
        count += 1
        explored[u] = True

        directions = []
        directions.append((u[0], u[1] - 1))  # above
        directions.append((u[0], u[1] + 1))  # below
        directions.append((u[0] + 1, u[1]))  # right
        directions.append((u[0] - 1, u[1]))

        print("this is distances array")
        print(distances)

        for i, dir in enumerate(directions):

            print("this is distances array"+ str(i))
            print(distances)

            x = dir[0]
            y = dir[1]

            if x < 0 or x > len(Map) - 1:
                continue
            if y < 0 or y > len(Map[0]) - 1:
                continue


            print ('x ' + str(x), "y " + str(y))
            if x==end[0] and y ==end[1]:
                point_found = (x, y)
                print(" Found at: " + str(x) + " , " + str(y))
                found = True
                parents[x][y] = i
                break

            if Map[x][y] != '-' :
                continue

            print("actual price of node in question")
            print((total[x][y]))
            print("actual pRICE OF node coming from ")
            print((total[u[0]][u[1]]))

            if (explored[(x,y)] == False and
                to_travel[x][y] > to_travel[u[0]][u[1]] + node_map[x][y]):
                to_travel[x][y] = to_travel[u[0]][u[1]] + node_map[x][y]
            if (explored[(x,y)] == False and
                total[x][y] > to_travel[x][y] + manhattan_dist((x,y), end)):
                total[x][y] = to_travel[x][y] + manhattan_dist((x,y), end)
                parents[x][y] = i
                print("2nd TIME:")
                for index, value in enumerate((distances)):
                #for i in range(len(distances)):
                    # Assuming y is in increasing order.
                    print (value)
                    if value[1] >= to_travel[x][y]+manhattan_dist((x,y),end):
                        print("value inserted: " + str((x,y)) + str(to_travel[x][y]+manhattan_dist((x,y),end)))
                        distances.insert(index, [(x,y), to_travel[x][y] + manhattan_dist((x,y),end)])
                        print(distances)
                        #MapPrinter.printMap(total)
                        break

        #sys.exit(0)
        if found == True:
            break

    print (count)
    MapPrinter.printMap(total)
    MapPrinter.printMap(parents)
    return distances

def manhattan_dist(coord1, coord2):
    #print ("MANH DIST:")
    #print(coord1[0] - coord2[0])
    #print(coord1[1] - coord2[1])
    return abs(coord1[0] - coord2[0]) + abs(coord1[1]-coord2[1])


def initiate_parent_map(Map):
    '''

    :param Map: two-dimensional list object
    :return:
    '''
    cost_map = Router.makeWorkMap(Map)

    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] == '-':
                cost_map[i][j] = 7

    return cost_map


def initiate_map(Map):
    '''

    :param Map: two-dimensional list object
    :return:
    '''
    node_map = Router.makeWorkMap(Map)

    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] == '-':
                node_map[i][j] = 1

    return node_map

def initiate_distance_map(Map):
    '''

    :param Map: two-dimensional list object
    :return:
    '''
    distance_map = Router.makeWorkMap(Map)
    to_travel = Router.makeWorkMap(Map)

    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] == '-':
                distance_map[i][j] = float("inf")
                to_travel[i][j] = float("inf")
            else:
                distance_map[i][j] = float("inf")
                to_travel[i][j] = float("inf")


    return distance_map, to_travel

def initiate_explored_map(Map):
    '''

    :param Map: two-dimensional list object
    :return:
    '''
    explored = {}

    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] == '-':
                explored[(i,j)] = False

    return explored


def initiate_label_map(Map):
    '''

    :param Map: two-dimensional list object
    :return:
    '''
    cost_map = Router.makeWorkMap(Map)
    distance_dict = []

    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] == '-':
                distance_dict.append([(i,j),float("inf")])
                cost_map[i][j] = float("inf")

    return distance_dict
