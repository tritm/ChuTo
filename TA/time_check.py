#! /usr/bin/env python
import time, timeit, logging
logging.getLogger("scapy").setLevel(1)
p = [0]*10
from scapy.all import *
def test():
    sendpfast(p[0],mbps=10,loop=100000,iface="eth0")
#p0 = (eng,vlan2), p1 = (eng,vlan3), p2 = (sci,vlan2), p3 = (sci,vlan3)
vlan = [2,3,2,3]
proto = [6,6,17,17]
infile = open('payload','r')
vpayload = infile.readlines()
infile.close
for i in range(4):
    p[i] = Ether()/Dot1Q()/IP()
    p[i].dst = "08:00:27:c1:c5:8a"
    p[i].src = "08:00:27:d8:ce:37"
    p[i][Dot1Q].vlan = vlan[i]
    p[i][IP].proto = proto[i]
    p[i].payload = str(vpayload)
t = timeit.Timer("test()","from __main__ import test")
print "%.2f usec/pass" % (1000000*t.timeit(number=1)/1)
                             
