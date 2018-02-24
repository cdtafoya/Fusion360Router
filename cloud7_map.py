from Map import Component
from Map import Map
from Map import Pin
import Router
import time

cs = []
rn41 = Component((15, 30), (5, 60))
led = Component((10, 12), (37, 100))
msp430 = Component((35, 30), (55, 77))
usb = Component((10, 20), (70, 45))
bm240 = Component((20, 12), (95, 135))
charge = Component((25, 20), (140, 57))
kohm= Component((6, 3), (115, 75))
battery= Component((18, 30), (115, 3))
cs.append(rn41)
cs.append(led)
cs.append(msp430)
cs.append(usb)
cs.append(bm240)
cs.append(charge)
cs.append(kohm)
cs.append(battery)

nets = []
map1 = Map(170, 155, cs, nets)

Router.route(map1, "router_output.txt")