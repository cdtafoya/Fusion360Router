from Map import Component
from Map import Map
from Map import Pin
import Router
import time

c3 = Component((9, 9), (60, 5))
c4 = Component((7, 11), (45, 10))
c5 = Component((14, 7), (35, 27))
c6 = Component((7, 10), (7, 18))
c7 = Component((18, 8), (47, 40))

cs = []
cs.append(c3)
cs.append(c4)
cs.append(c5)
cs.append(c6)
cs.append(c7)

start_pins = []
terminal_pins = []

ground_pin = Pin('GND',(0,0))

net_1 = [Pin('S1', (14, 20)), Pin('T1', (34, 29)) ]
net_2 = [Pin('S2', (14, 25)), Pin('T2', (34, 31)) ]
net_3 = [Pin('S3', (49, 27)), Pin('T3', (52, 14)) ]
net_4 = [Pin('S4', (49, 29)), Pin('T4', (52, 16)) ]
net_5 = [Pin('S5', (49, 31)), Pin('T5', (58, 39)) ]
net_6 = [Pin('S6', (49, 33)), Pin('T6', (52, 39)) ]
net_7 = [Pin('S7', (52, 12)), Pin('T7', (59,  9)) ]
net_8 = [Pin('S8', (59,  7)), Pin('T8', (55,  2)) ]
net_9 = [Pin('S9', (59,  5)), Pin('T9', (57,  2)) ]

nets = []
nets.append(net_1)
nets.append(net_2)
nets.append(net_3)
nets.append(net_4)
nets.append(net_5)
nets.append(net_6)
nets.append(net_7)
nets.append(net_8)
nets.append(net_9)

start_pins.append(Pin('S1', (14, 20)))
start_pins.append(Pin('S2', (14, 25)))
start_pins.append(Pin('S3', (49, 27)))
start_pins.append(Pin('S4', (49, 29)))
start_pins.append(Pin('S5', (49, 31)))
start_pins.append(Pin('S6', (49, 33)))
start_pins.append(Pin('S7', (52, 12)))
start_pins.append(Pin('S8', (59, 7)))
start_pins.append(Pin('S9', (59, 5)))
#start_pins.append(Pin('S0', (14, 20)))

terminal_pins.append(Pin('T1', (34, 29)))
terminal_pins.append(Pin('T2', (34, 31)))
terminal_pins.append(Pin('T3', (52, 14)))
terminal_pins.append(Pin('T4', (52, 16)))
terminal_pins.append(Pin('T5', (58, 39)))
terminal_pins.append(Pin('T6', (52, 39)))
terminal_pins.append(Pin('T7', (59, 9)))
terminal_pins.append(Pin('T8', (55, 2)))
terminal_pins.append(Pin('T9', (57, 2)))
#terminal_pins.append(Pin('T0', (31, 35)))

'''
Program needs to route by nets. So every start_pin and terminal_pin
set needs to be kept together in a list of nets which hold references 
to these pins. 
'''

map1 = Map(80, 50, cs, nets)

Router.printMap(map1.space)
start_time = time.time()
Router.route(map1, "router_output.txt")
print("--- %s seconds ---" % (time.time() - start_time))


