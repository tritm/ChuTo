#!/usr/bin/python
import socket

#import sys
#PYDEVD_PATH='/home/tritm/.eclipse/org.eclipse.platform_3.7.0_155965261/plugins/org.python.pydev.debug_2.2.2.2011082312/pysrc/'
#if sys.path.count(PYDEVD_PATH)<1:
#    sys.path.append(PYDEVD_PATH)
#import pydevd
#pydevd.settrace('203.178.135.95', port=5678, stdoutToServer=True, stderrToServer=True)

MGR_IP_ADDRESS = '203.178.135.32'  # The remote host
MGR_PORT = 1990                    # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((MGR_IP_ADDRESS, MGR_PORT))
print ('Connect to HostManager...')

def wait_for_request_from_mgr():
    data =  s.recv(1024)
    print 'wait_for_request_from_mgr...'
    print 'The request is: ' +data
    if data != 'max_rate_kbps?': 
        print 'data received is different from expected '
def send_max_rates():
    max_rate = '10'
    print 'Send requested max_rate = %d' %(int(max_rate)) 
    s.send(max_rate)
def wait_for_optimal_rates():
    print 'wait_for_optimal_rates...'
    optimal_rates_string = s.recv(1024)
    print 'Optimal_rates =  ' +optimal_rates_string 
    optimal_rates_tuple = tuple(float(s) for s in optimal_rates_string[1:-1].split(','))
    
wait_for_request_from_mgr()
send_max_rates()
wait_for_optimal_rates()
# store_optimal_rates()
