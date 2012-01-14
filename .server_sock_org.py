#!/usr/bin/python
import socket

MGR_IP_ADDRESS = '203.178.135.32'
MGR_PORT = 1890
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((MGR_IP_ADDRESS, MGR_PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    print data
    conn.send(data)
conn.close()