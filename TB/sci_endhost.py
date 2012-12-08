#! /usr/bin/env python
from scapy.all import *
logfile = open('endhost.log','w')
from threading import Thread
from random import randint
import time
import socket
import timeit
import os
cmd_kill_tcpreplay = 'killall -9 tcpreplay'
#p0 = (eng,vlan2), p1 = (eng,vlan3), p2 = (sci,vlan2), p3 = (sci,vlan3)
socket_wait_time = 60
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
        p[i].src = "78:cd:8e:81:86:59"
        p[i].dst = "78:cd:8e:81:1b:b7"
        p[i][Dot1Q].vlan = vlan[i]
        p[i][IP].proto = proto[i]
        p[i][IP].payload = str(vpayload)
    return p
def connect_to_hm():       
    MGR_IP_ADDRESS = '192.168.0.5'  # The remote host
    MGR_PORT = 1990                    # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((MGR_IP_ADDRESS, MGR_PORT))
    return s
def path_traffic_sending(vlan,npackets):
        sendpfast(vlan,limit=npackets,iface="eth1")
def wait_for_request_from_mgr():
    data =  s.recv(1024)
    print data
    if data != 'max_rate_kbps?': 
        print >> logfile, 'data received is different from expected '
def send_max_rates():
#    max_rate = str(randint(1,10)) 
    max_rate = str(0)
    s.send(max_rate)
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
    print "vlan2_rate = %f" %vlan2_rate
    vlan2_npackets = int(vlan2_rate*socket_wait_time*1000000.0/12000.0)
    print "TRI.hm: vlan2_npackets = %d" %vlan2_npackets
    vlan3_rate = optimal_rates_tuple[1]
    print "TRI.hm: vlan3_rate = %f" %vlan3_rate
    vlan3_npackets = int(vlan3_rate*socket_wait_time*1000000.0/12000.0)
    print "TRI.hm: vlan3_npackets = %d" %vlan3_npackets
    if (vlan2_npackets > 0):
        t2 = Thread(target=path_traffic_sending, args=(2,vlan2_npackets,))
        t2.start()
    if (vlan3_npackets > 0):
        t3 = Thread(target=path_traffic_sending, args=(3,vlan3_npackets,))
        t3.start()

logfile.close()


