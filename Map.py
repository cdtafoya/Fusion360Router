'''
Created on Sep 21, 2017

@author: Carlos
'''
from __future__ import print_function
import sys
from email._header_value_parser import Terminal



class Map(object):
    '''
    classdocs
    '''

    def __init__(self, x, y, components, nets):
        self.x_size = x
        self.y_size = y
        self.space = self.makeSpace(x, y) #two-dimensional list

        self.components = components
        self.updateComponents()

        #self.start_pins = [i[0] for i in nets]
        #self.terminal_pins = [i[1] for i in nets]
        #self.updatePins()
        
        self.nets = nets
        self.updatePins()
        
        self.traces = []

    def makeSpace(self, x, y):
        """returns a list of list (Python array) representing the map
           space to route in, of size x by y.
           
        x -- integer type - length of map
        y -- integer type - height of map
           
        space -- Two-Dimensional list
        """   
        space = []
        for i in range(x):
            space.append([])
            for j in range(y):
                space[i].append(' -')
            
        return space
    
    def addComponent(self, component):

        c = component

        if (c.x + c.x_size > self.x_size or
            c.y + c.y_size > self.y_size):

            raise ValueError('Component trying to be added of size ' + str(c.size) + 
                              ' does not fit at position ' + str(c.pos) + 
                               '\n in map of size ' + str(self.space.shape))

        for i in range (c.x, c.x + c.x_size):
            for j in range(c.y, c.y + c.y_size):
                self.space[i][j] = c.letter
                #print(i, c.y, c.letter)

        # print ("end of add")

    def updatePins(self):
        #allPins = self.start_pins + self.terminal_pins
        for net in self.nets:
            
            for pin in net.pins:
                
                if self.space[pin.x][pin.y] == ' o':
                    raise  ValueError('Pin' +str(pin.name)+ "with position " +str(pin.pos)+
                                      ' cannot be placed on existing obstacle')
    
                self.space[pin.x][pin.y] = pin.name

    def updateComponents(self):
        cs = self.components
        self.space = self.makeSpace(self.x_size, self.y_size)
        # print (len(self.components))
        c = len(cs)
        for i in range(c):
            self.addComponent(cs[i])

        # print ("finshed for loop")

    def printComponents(self):
        for c in self.components: 
            print (c.size + ' ' + c.position)

    def addPin(self, pin):
        self.pins.append(pin)
        self.space[pin.x][pin.y] = pin.name
        pin.extension = self.pin_e_length

    def addTrace(self, trace):
        self.traces.append(trace)


class Component(object):
    '''
    classdocs
    '''

    def __init__(self, size, position):
        self.size = size
        self.x_size = size[0]
        self.y_size = size[1]
        self.pos = position  # position of top right cell
        self.x = position[0]
        self.y = position[1]
        self.letter = ' o'

    def setLetter(self, letter):
        self.letter = ' ' + str(letter)

    def setPosition(self, position):
        self.position = position


class Pin(object):
    '''
    classdocs
    '''

    
    def __init__(self,name, net, component, position):
        '''
        Constructor
        '''
        self.name = name
        self.net = net
        self.component = component
        self.id = 0
        self.extension = 0  # Length of extension from component
        
        if net == 'GND':
            self.pos = None
            self.x = None
            self.y = None 
        else:
            self.pos = position
            self.x = position[0]
            self.y = position[1]
        
        self.oppos = None  # Points to Pin object that this Pin must connect to
        self.attached = True  # Pin is attached to component

    def setExtension(self, direction):
        self.extension = direction

    def setPosition(self, position):
        self.pos = position

    def setOpposite(self, opposite):
        self.oppos = opposite

    def setAttached(self, attached):
        self.attached = attached

    def setX(self, x):
        self.pos = (x, self.y)
        self.x = x

    def setY(self, y):
        self.pos = (self.x, y)
        self.y = y

        
class Net(object):
    """Net object composed of pins and traces.
    
    pins -- Pin object list of Pins in net
    
    """
       
    def __init__(self, name):
        
        self.name = name  
        self.pins = []
        self.traces = None
        self.bbox = None
        self.size = 0
    
    def addPin(self, pin):
        
        pin.net = self
        self.pins.append(pin)
        self.size += 1
        
    
class Trace(object):
    """Trace objects repesent the generated connections between routed pins.
       It is classified as one of two types: 1.principal trace, which connects 
       either a net of size 2 or could be the main connection made to route
       a net of 3+. 2. auxiliary trace, which connects a pin to a principal trace
       in a net of 3+.
       
    lines -- line objects that make up the trace.
    """
    
    def __init__(self, lines):
        
        self.lines = lines
        
        
    def addLine(self, points):
        """Appends a line object to the list of lines that make up the trace.
           Additionally checks to see if it is in order, that is whether the 
           lines go from start to finish of the trace.
           
        points -- x,y coordinates contained in the line. 
        """
    
class PseudoPair(object):
    """PseudoPair objects can contain references to pins which may correspond to nets of 
        size 2 or more if they are of type "p2p" pin to pin. They also may be of type
        "p2n" pin to net. For nets of 3+, pseudoPairs are made according to what might
        be a good pair to connect initially. 
        
    type -- "p2p" pin to pin pair, "p2n" pin to net pair.
    pin -- reference to pin object being connnected.
    terminal -- reference either to pin or net being connected
    pinsInside -- integer amount dentoing pins between pin and terminal.
    netSize -- integer amount denoting if pin pair is part of net size 2 or 3+.  
    """
    
    def __init__(self, type, pin, terminal, pinsInside, netSize):
        
        self.type = type
        self.pin = pin
        self.terminal = terminal
        self.pinsInside = pinsInside
        self.netSize = netSize
        