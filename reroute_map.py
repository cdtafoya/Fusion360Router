from Map import Component
from Map import Map
from Map import Pin
from Map import Net
import Router
import time
import MapPrinter

c1 = Component((7,2), (0,0))
c2 = Component((3,2), (1,3))
c3 = Component((3,2), (5,3))

cs = []
cs.append(c1)
cs.append(c2)
cs.append(c3)

net_1 = Net('N$1')
net_2 = Net('N$2')

net_1.addPin(Pin('A1','N$1', 'X', (3,2)))
net_1.addPin(Pin('A2','N$1', 'X', (7,0)))

net_2.addPin(Pin('B1','N$2', 'X', (7,2)))
net_2.addPin(Pin('B2','N$2', 'X', (7,5)))

nets = []
nets.append((net_1))
nets.append((net_2))

map1 = Map(9, 7, cs, nets)

MapPrinter.printMap(map1.space)
Router.route(map1, "router_output.txt")