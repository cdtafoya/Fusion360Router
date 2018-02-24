'''
Created on Sep 21, 2017

@author: Carlos
'''


class Component(object):
    '''
    classdocs
    '''

    def __init__(self, size, position):
        self.size = size
        self.x_size = size[0]
        self.y_size = size[1]
        self.pos = position # position of top right cell
        self.x = position[0]
        self.y = position[1]
        self.letter = ' o'

    def setLetter(self, letter):
        self.letter = ' ' + str(letter)

    def setPosition(self, position):
        self.position = position
        
        
        