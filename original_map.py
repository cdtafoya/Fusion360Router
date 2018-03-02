from Map import Component
from Map import Map
from Map import Pin
from Map import Net
import Router
import time
import sys

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

ground_pin = Pin('GND', 'GND', 'GND',(0,0))

net_1 = Net('N$1')
net_2 = Net('N$2')
net_3 = Net('N$3')
net_4 = Net('N$4')
net_5 = Net('N$5')
net_6 = Net('N$6')
net_7 = Net('N$7')
net_8 = Net('N$8')
net_9 = Net('N$9')

net_1.addPin(Pin('S1','N$1','X', (14, 20)))
net_1.addPin(Pin('T1','N$1','X', (34, 29)))

net_2.addPin(Pin('S2','N$2','X', (14, 25)))
net_2.addPin(Pin('T2','N$2','X', (34, 31)))

net_3.addPin(Pin('S3','N$3','X', (49, 27))) 
net_3.addPin(Pin('T3','N$3','X',(52, 14)))

net_4.addPin(Pin('S4','N$4','X', (49, 29)))
net_4.addPin(Pin('T4','N$4','X', (52, 16)))

net_5.addPin(Pin('S5','N$5','X', (49, 31)))
net_5.addPin(Pin('T5','N$5','X',(58, 39)))

net_6.addPin(Pin('S6','N$6','X', (49, 33)))
net_6.addPin(Pin('T6','N$6','X', (52, 39)))

net_7.addPin(Pin('S7','N$7','X', (52, 12)))
net_7.addPin(Pin('T7','N$7','X', (59,  9)))

net_8.addPin(Pin('S8','N$8','X', (59,  7)))
net_8.addPin(Pin('T8','N$8','X', (55,  2)))

net_9.addPin(Pin('S9','N$9','X',(59,  5)))
net_9.addPin(Pin('T9','N$9','X', (57,  2)))

nets = []
nets.append((net_1))
nets.append((net_2))
nets.append((net_3))
nets.append((net_4))
nets.append((net_5))
nets.append((net_6))
nets.append((net_7))
nets.append((net_8))
nets.append((net_9))

net_10 = Net('N$X')
net_10.addPin(Pin('SX','N$X','X',(3, 46)))
net_10.addPin(Pin('TX','N$X','X',(76,2)))
net_10.addPin(Pin('BX','N$X','X',(16,12)))
#nets.append(net_10)
'''
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
'''
Program needs to route by nets. So every start_pin and terminal_pin
set needs to be kept together in a list of nets which hold references 
to these pins. 
'''

map1 = Map(80, 50, cs, nets)

start_time = time.time()
Router.route(map1, "router_output.txt")
print("--- %s seconds ---" % (time.time() - start_time))


