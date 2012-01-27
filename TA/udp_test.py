#!/usr/bin/python
import time, os
cmd = 'iperf -c 10.0.0.2 -u -b 100m'
while True:
	os.system(cmd)
	time.sleep(60)
