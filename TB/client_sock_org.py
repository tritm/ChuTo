#!/usr/bin/python
import socket

MGR_IP_ADDRESS = '203.178.135.32'  # The remote host
MGR_PORT = 1890         # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((MGR_IP_ADDRESS, MGR_PORT))
s.send('Hello World')
data = s.recv(1024)
s.close 
print 'Received', repr(data)
