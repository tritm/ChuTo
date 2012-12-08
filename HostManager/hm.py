#! /usr/bin/env python
from server import *
from cvxopt import matrix
import numpy, time, os
import data
def initvar(): 
    global eng_Q, sci_Q, nox_Q, eng_cv, sci_cv, nox_cv, L, eng_capa, sci_capa
    global eng_capa_temp, sci_capa_temp, delta, conn
import numpy, time
from data import *
def initvar(): 
    global eng_Q, sci_Q, eng_cv, sci_cv, L, sub_capa, eng_capa, sci_capa
    global eng_capa_temp, sci_capa_temp, delta
    eng_Q = []
    sci_Q = []
    nox_Q = []
    eng_cv = Condition()
    sci_cv = Condition()
    nox_cv = Condition()
    L = 3
    data.sub_capa = matrix(51.20*numpy.ones(L))
    eng_capa = matrix(20.48*numpy.ones(L))
    sci_capa = matrix(30.72*numpy.ones(L))
    sub_capa = matrix(5*numpy.ones(L))
    eng_capa = matrix(2*numpy.ones(L))
    sci_capa = matrix(3*numpy.ones(L))
    eng_capa_temp = matrix(-1000*numpy.ones(L))
    sci_capa_temp = matrix(-1000*numpy.ones(L))
    delta = 1
def get_cp(cv, Q): 
    # cv: conditional variable, Q: queue
    cv.acquire()
    while not Q:
        cv.wait()
    cp = Q.pop()
    cv.release()
    return cp 
def rate(tcp_vlan2,udp_vlan2,tcp_vlan3,udp_vlan3):
   cmd_t2 = '/home/tritm/openvswitch-1.6.1/utilities/ovs-vsctl --db=tcp:192.168.0.11:3000 set queue 1c6622ec-fe4e-44ad-8703-8bbe18e7fe5f other-config:min-rate=%d other-config:max-rate=%d' %(tcp_vlan2,tcp_vlan2) 
   cmd_u2 = '/home/tritm/openvswitch-1.6.1/utilities/ovs-vsctl --db=tcp:192.168.0.11:3000 set queue ba4729ca-7f8c-46ad-976a-34d11e65472a other-config:min-rate=%d other-config:max-rate=%d' %(udp_vlan2,udp_vlan2) 
   cmd_t3 = '/home/tritm/openvswitch-1.6.1/utilities/ovs-vsctl --db=tcp:192.168.0.11:3000 set queue 2553a535-9cd9-4454-83bf-2b68e08a7203 other-config:min-rate=%d other-config:max-rate=%d' %(tcp_vlan3,tcp_vlan3) 
   cmd_u3 = '/home/tritm/openvswitch-1.6.1/utilities/ovs-vsctl --db=tcp:192.168.0.11:3000 set queue d65c1257-e484-4990-accc-db9b30ea96b6 other-config:min-rate=%d other-config:max-rate=%d' %(udp_vlan3,udp_vlan3) 
   cmd_mon = '/home/tritm/openvswitch-1.6.1/utilities/ovs-vsctl --db=tcp:192.168.0.11:3000 list queue | grep -P "external_ids|other_config" > /home/tritm/ChuTo_SimpleNetwork/HostManager/rate_adapt.log'
   os.system(cmd_t2)
   os.system(cmd_u2)
   os.system(cmd_t3)
   os.system(cmd_u3)
   os.system(cmd_mon)
initvar() 
MGR_IP_ADDRESS = "192.168.0.5"
MGR_PORT = 2000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind ((MGR_IP_ADDRESS, MGR_PORT))
s.listen(1)
conn, addr = s.accept()
print 'Accept a connection request from NOX =' + str(addr)
eng = Vncal('eng', eng_Q, eng_cv, eng_capa,data.period)
eng.start()
sci = Vncal('sci', sci_Q, sci_cv, sci_capa,data.period)
sci.start() 
nox = Nox(conn,nox_Q,nox_cv)
nox.start()
alpha = 5
i = 1
initvar() 
eng = Vncal('eng', eng_Q, eng_cv, eng_capa,period)
eng.start()
sci = Vncal('sci', sci_Q, sci_cv, sci_capa,period)
sci.start() 
while True: 
    #------------------------------------------------------ get congestion price
    eng_cp_all = get_cp(eng_cv,eng_Q)
    sci_cp_all = get_cp(sci_cv,sci_Q)
    eng_cp = eng_cp_all[0:L]
    sci_cp = sci_cp_all[0:L]
    print 'TRI.hm: eng_cp = \n', eng_cp
    print 'TRI.hm: sci_cp = \n', sci_cp
    #--------------------------------------- calculate new virtual link capacity
    for l in range(L):
        eng_capa_temp[l] = eng_capa[l] + alpha*sci_capa[l]*(eng_cp[l] - sci_cp[l])/(eng_capa[l] + sci_capa[l])
        sci_capa_temp[l] = sci_capa[l] + alpha*eng_capa[l]*(sci_cp[l] - eng_cp[l])/(eng_capa[l] + sci_capa[l])
        if eng_capa_temp[l] < 0: eng_capa_temp[l] = 0
        if sci_capa_temp[l] < 0: sci_capa_temp[l] = 0
    #-------------- re-normalize to make eng_capa[l] + sci_capa[l] = sub_capa[l]
#    print "TRI.hm: eng_capa_temp = \n", eng_capa_temp
#    print "TRI.hm: sci_capa_temp = \n", sci_capa_temp
    print 'TRI.hm: data.sub_capa[1] = %d'%data.sub_capa[1]
        eng_capa_temp[l] = eng_capa[l] + sci_capa[l]*(eng_cp[l] - sci_cp[l])/(eng_capa[l] + sci_capa[l])
        sci_capa_temp[l] = sci_capa[l] + eng_capa[l]*(sci_cp[l] - eng_cp[l])/(eng_capa[l] + sci_capa[l])
        if eng_capa_temp[l] < 0: eng_capa_temp[l] = 0
        if sci_capa_temp[l] < 0: sci_capa_temp[l] = 0
    #-------------- re-normalize to make eng_capa[l] + sci_capa[l] = sub_capa[l]
    print "TRI.hm: eng_capa_temp = \n", eng_capa_temp
    print "TRI.hm: sci_capa_temp = \n", sci_capa_temp
    for l in range(L):
        eng_capa[l] = eng_capa_temp[l]/(eng_capa_temp[l]+sci_capa_temp[l])*data.sub_capa[l]
        sci_capa[l] = sci_capa_temp[l]/(eng_capa_temp[l]+sci_capa_temp[l])*data.sub_capa[l]
    #----------------------------------------- update back to eng and sci object
    print "TRI.hm: eng_capa = \n", eng_capa
    print "TRI.hm: sci_capa = \n", sci_capa
    eng.update(eng_capa,alpha)
    sci.update(sci_capa,alpha)   
#    rate(eng_capa[0]*1e5,sci_capa[0]*1e5,eng_capa[1]*1e5,sci_capa[1]*1e5)
    i += 1
    #if (i-1)%100 == 0:
    #    alpha += 1
    eng.update(eng_capa)
    sci.update(sci_capa)
    #Use source price----------------------------------------time.sleep(wait) 
