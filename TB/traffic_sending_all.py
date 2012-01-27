#! /usr/bin/env python
import logging
import time
logging.getLogger("scapy").setLevel(1)
p = [0]*10
from scapy.all import *
#p0 = (eng,vlan2), p1 = (eng,vlan3), p2 = (sci,vlan2), p3 = (sci,vlan3)
vlan = [2,3,2,3]
proto = [6,6,17,17]
for i in range(4):
    p[i] = Ether()/Dot1Q()/IP()
    p[i].src = "08:00:27:c1:c5:8a"
    p[i].dst = "08:00:27:d8:ce:37"
    p[i][Dot1Q].vlan = vlan[i]
    p[i][IP].proto = proto[i]
while True:
    for j in range(4):
        sendp(p[j], iface="eth0")
        time.sleep(1)
        
