'''
Created on Jan 3, 2018

@author: cdtafoya
'''
from Map import Component
from Map import Map
from Map import Pin
from collections import OrderedDict
import Router
from unittest.test.testmock.support import SomeClass

class Trace(object):
    
    def __init__(self, points):
        self.points = points
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

s1 = Trace([p1,p2])
s2 = Trace([p3,p2])

ss = []
ss.append(s1)
ss.append(s2)

for i in ss:
    print( i)
    
s1.points = None
print (s1.points)

for i in ss:
    print( i)
    
d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}

# dictionary sorted by key
dn = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
#fn ={}
fn = OrderedDict({})
fn['bla'] = p1
fn['bla2'] = p2
fn['bla3'] = p3
fn['bla4'] = p2

#print (fn[0])

for d in range(len(fn)):
    print (fn.popitem(last=False))


trace_d = {}
trace_d[s1] = s2
trace_d[s2] = s1

ss.pop(s2)











