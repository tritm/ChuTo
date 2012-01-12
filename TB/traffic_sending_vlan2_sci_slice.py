#! /usr/bin/env python
import logging
import time
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

while True:
    p = Ether()/Dot1Q()
    p.src = "08:00:27:c1:c5:8a"
    p.dst = "08:00:27:d8:ce:37"
    p[Dot1Q].vlan = 2 
    p.type = 0x0806
    sendp(p, iface="eth0")
    time.sleep(2)
