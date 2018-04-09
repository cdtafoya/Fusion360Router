from Map import Component
from Map import Map
from Map import Pin
from Map import Net
import Router
import time
import MapPrinter
import SearchAlgorithms as SA

c1 = Component((10,3), (12,8))


cs = []
cs.append(c1)

net_1 = Net('N$1')

net_1.addPin(Pin('A1','N$1', 'X', (3,3)))
net_1.addPin(Pin('T','N$1', 'X', (17,17)))

nets = []
nets.append((net_1))




sample = Pin('A1','N$1', 'X', (20,20))
sample2 = Pin('A1','N$1', 'X', (9,9))
map2 = Map(100,100, [], [])
end = (40,40)
d = SA.A_Star(sample, map2.space, end)
