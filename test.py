'''
Created on Jan 3, 2018

@author: cdtafoya
'''
from Map import Component
from Map import Map
from Map import Pin
import Router

'''
When initializing nets and pins. should be:
The simpler XML will contain the name of each net.
So each net should be initilied.

net1 = Net('N$1') etc.
nets.append(net1)

then each pin is initialized and added to its repsective net.

pin1 = Pin('GND', Component (could be string or pointer to actual component object),
          (x1, y1))
net1.addPin(pin1)



'''

p1 = (0,0,3)
p2 = (0,0,1)
p3 = (0,0,2)
li = []
li.append(p1)
li.append(p2)
li.append(p3)
print (li)
li.sort(key=lambda pseudoPin : pseudoPin[2])
print (li)

