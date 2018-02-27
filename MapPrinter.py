'''
Created on Feb 27, 2018

@author: Carlos
'''

def printMap(Map):
    """Print Map given in console.

    Map -- must be list (Two-dimensional) type
    """

    # Print column number line
    print(' =  ', end='')
    for i in range(0, len(Map)):
        if i < 10:
            print ('  ' + str(i), end='')
        else:
            print(' '+str(i), end='')
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
            if len(Map[y][x]) == 1:
                space = '  '
            elif len(Map[y][x]) == 2:
                space = ' '
            else:
                space = ''
            print (space + Map[y][x], end='')
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
            space  = None
            if len(Map[y][x]) == 2:
                space = ' '
            else:
                space = ''
            outputFile.write(space + Map[y][x])
        outputFile.write('\n')
    
    