from Map import Component
from Map import Map
from Map import Pin
from Map import Net
import Router
import time

cs = []
first = Component((12, 18), (10, 16))
second = Component((12, 18), (33, 16))
third = Component((12, 18), (56, 16))
cs.append(first)
cs.append(second)
cs.append(third)
nets = []

net_1 = Net('N$1')
net_2 = Net('N$2')
net_3 = Net('N$3')
net_4 = Net('N$4')

net_1.addPin(Pin('A1','N$1','X', (15,15)))
net_1.addPin(Pin('B1','N$1','X',(37, 15)))
net_1.addPin(Pin('C1','N$1','X',(62,34)))

net_2.addPin(Pin('A2','N$2','Y',(15,34)))
net_2.addPin(Pin('B2','N$2','Y',(37, 34)))
net_2.addPin(Pin('C2','N$2','Y',(62,15)))

net_3.addPin(Pin('A3','N$3','Z', (5,20)))
net_3.addPin(Pin('B3','N$3','Z', (50, 42)))

net_4.addPin(Pin('A4','N$4','ZZ', (29, 46)))
net_4.addPin(Pin('B4','N$4','ZZ', (21, 46)))

nets.append(net_1)
nets.append(net_2)
nets.append(net_3)
nets.append(net_4)
map1 = Map(80, 50, cs, nets)

start_time = time.time()
Router.route(map1, "router_output.txt")
print("--- %s seconds ---" % (time.time() - start_time))