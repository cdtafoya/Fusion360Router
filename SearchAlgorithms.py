'''
Created on Feb 27, 2018

@author: Carlos
'''
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

                if Map[x][y] == ' -':
                    Map[x][y] = str(iteration)
                    temp.append(dir)

                if Map[x][y] == ' T':
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

