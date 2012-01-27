#!/usr/bin/python
import os, time
cmd = 'iperf -c 10.0.0.1'
while True:
	os.system(cmd)
	time.sleep(60)

