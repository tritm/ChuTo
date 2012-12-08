#! /usr/bin/env python
from scapy.all import *
from datetime import datetime
logfile = open('endhost.log','w')
from threading import Thread
from random import randint
import time
import socket
import timeit
import os
from data import *
#p0 = (eng,vlan2), p1 = (eng,vlan3), p2 = (sci,vlan2), p3 = (sci,vlan3)
def packet_builder():
    p = [0]*4
    logfile = open('endhost.log','w')
    vlan = [2,3,2,3]
    proto = [6,6,17,17]
    infile = open('payload','r')
    vpayload = infile.readlines()
    infile.close
    for i in range(4):
        p[i] = Ether()/Dot1Q()/IP()
        p[i].dst = "78:cd:8e:81:86:59"
        p[i].src = "78:cd:8e:81:1b:b7"
        p[i][Dot1Q].vlan = vlan[i]
        p[i][IP].proto = proto[i]
        p[i][IP].payload = str(vpayload)
    return p
def connect_to_hm():       
    MGR_IP_ADDRESS = '192.168.2.5'  # The remote host
    MGR_PORT = 1890                    # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((MGR_IP_ADDRESS, MGR_PORT))
    return s
def path_traffic_sending(vlan,npackets):
        sendpfast(vlan=vlan,limit=npackets,iface="eth1")
        sendpfast(vlan=vlan,limit=npackets,iface="eth1")
        sendpfast(vlan=vlan,slice="eng",limit=npackets,iface="eth1")
def wait_for_request_from_mgr():
    data =  s.recv(1024)
    print data
    if data != 'max_rate_kbps?': 
        print >> logfile, 'data received is different from expected '
def send_max_rates():
    global ta_eng_nperiod, ta_eng_max_rate
    if ta_eng_nperiod % 10 == 0:  ta_eng_max_rate = str(randint(1,10)) 
    ta_eng_nperiod += 1
    print 'ta_eng_max_rate =' +ta_eng_max_rate
    s.send(ta_eng_max_rate)
    ta_eng_max_rate = 30
    print 'ta_eng_max_rate =' +str(ta_eng_max_rate)
    s.send(str(ta_eng_max_rate))
    #---------------------------------------------------------------- print timestamp
    print >> logfile, str(datetime.now())
def wait_for_optimal_rates():
    optimal_rates_string = s.recv(1024) 
    optimal_rates_tuple = tuple(float(s) for s in optimal_rates_string[1:-1].split(','))
    print 'optimal rate = ' + str(optimal_rates_tuple)
    return optimal_rates_tuple
p = packet_builder()
s = connect_to_hm()

while True:
    wait_for_request_from_mgr()
    send_max_rates()
    optimal_rates_tuple = wait_for_optimal_rates()
    vlan2_rate = optimal_rates_tuple[0]
    vlan2_npackets = int(vlan2_rate*period*1000000.0/12000.0)
    vlan3_rate = optimal_rates_tuple[1]
    vlan3_npackets = int(vlan3_rate*period*1000000.0/12000.0)
# packet has size 90 bytes
    vlan2_rate = optimal_rates_tuple[0]
    vlan2_npackets = int(vlan2_rate*period*102400.0/720.0)
    vlan3_rate = optimal_rates_tuple[1]
    vlan3_npackets = int(vlan3_rate*period*102400.0/720.0)
    print "vlan2_rate = %12.8f, vlan2_npackets = %i" %(vlan2_rate,vlan2_npackets)
    print "vlan3_rate = %12.8f, vlan3_npackets = %i" %(vlan3_rate,vlan3_npackets)
    t2 = Thread(target=path_traffic_sending, args=(2,vlan2_npackets,))
    t2.start()
    t3 = Thread(target=path_traffic_sending, args=(3,vlan3_npackets,))
    t3.start()
logfile.close()


