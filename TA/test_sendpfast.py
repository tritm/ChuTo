#! /usr/bin/env python
from scapy.all import *
from threading import Thread
import threading
import time
import timeit
import logging
#class Operation(threading._Timer):
#    def __init__(self, *args, **kwargs):
#         threading._Timer.__init__(self, *args, **kwargs)
#         self.setDaemon(True)
#
#    def run(self):
#        while True:
#            self.finished.clear()
#            self.finished.wait(self.interval)
#            if not self.finished.isSet():
#                self.function(*self.args, **self.kwargs)
#            else:
#                return
#            self.finished.set()
#
#class Manager(object):
#
#    ops = []
#
#    def add_operation(self, operation, interval, args=[], kwargs={}):
#        op = Operation(interval, operation, args, kwargs)
#        self.ops.append(op)
#        thread.start_new_thread(op.run, ())
#
#    def stop(self):
#        for op in self.ops:
#            op.cancel()
##        self._event.set()

def traffic_sending(pps = 20,loop=2000000):
	sendpfast(p,pps=pps,loop=loop,iface="lo")
def packet():
	infile = open('payload', 'r')
	vpayload = infile.readlines()
	infile.close
	p = Ether() / Dot1Q() / IP()
	p.dst = "08:00:27:c1:c5:8a"
	p.src = "08:00:27:d8:ce:37"
	p[Dot1Q].vlan = 2
	p[IP].proto = 6
	p[IP].payload = str(vpayload)
	return p

if __name__ == '__main__':
	p = packet()
	print p.show	
	traffic_sending()
#	timer = Manager()
#	timer.add_operation(traffic_sending,1)
#	while True:
#		time.sleep(.1)



 
