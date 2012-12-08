#!/usr/bin/python
import socket, time
from grad import *
from threading import Thread, Condition
import data
class Vncal(Thread):
    def __init__(self,vid,Q,cv,capa,period,alpha=1): # {{{
        Thread.__init__(self)
        self.MGR_IP_ADDRESS = '192.168.0.5'
        self.NUM_SOURCES = 2
        self.Q = Q
        self.cv = cv
        self.capa = capa
        self.end_host_sockets = []
        self.max_rate_dict = {}
        self.max_rate_list = []
        self.optimal_rate_dict = {}
<<<<<<< HEAD
        self.period =period 
        self.vid = vid
        self.alpha= alpha
=======
        self.wait =wait 
        self.vid = vid
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
        if self.vid == 'eng':
            self.MGR_PORT = 1890
        else:
            self.MGR_PORT = 1990 # }}}
    def update(self,capa,alpha):
        self.capa = capa
        self.alpha = alpha
    def listen_for_endhosts(self): # {{{
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.MGR_IP_ADDRESS, self.MGR_PORT))
<<<<<<< HEAD
        print 'Listen for connect requests from EndHosts from virtual network:', self.vid
=======
        print '\nListen for connect requests from EndHosts from virtual network:', self.vid
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
        s.listen(self.NUM_SOURCES)
        return s # }}}
    def get_max_rate(self,end_host_conn, host_id): # {{{
        print '\nAsk EndHost %s for wanted max_rate...' %host_id, self.vid
        end_host_conn.send('max_rate_kbps?')
        max_rate = end_host_conn.recv(1024)
        print 'received max_rate = ' +max_rate +' from EndHost: ' +host_id, self.vid
        return max_rate # }}}
    def nw_opt_rate(self,max_rate_list): # {{{
        c = Netcal(capa = self.capa)
        all_opt_rate,cp_all = c.optFunc(max_rate_list)
<<<<<<< HEAD
        print "TRI.server: all_opt_rate ="
        print all_opt_rate,
#        print "TRI.server: cp_all ="
#        print cp_all,
=======
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
        length = all_opt_rate.size[0]
        for i in range(length): 
            if all_opt_rate[i] < 1e-3: all_opt_rate[i] = 0
        return all_opt_rate,cp_all # }}}
    def end_opt_rate(self,host_id, max_rate,all_opt_rate): # {{{
        print 'Calculate optimal rate for EndHost %s of virtual network %s...' %(host_id, self.vid)  # {{{ # {{{
        if host_id == '192.168.0.14': #TA
            optimal_rate = tuple(all_opt_rate[0:2])
        elif host_id == '192.168.0.15': #TB
            optimal_rate = tuple(all_opt_rate[2:4])
<<<<<<< HEAD
        print 'optimal_rate (100Kbps) for EndHost %s of virtual network %s = %s with alpha = (%s)' %(host_id,self.vid,str(optimal_rate),self.alpha)
=======
        print 'optimal_rate (Mbps) for EndHost %s of virtual network %s = %s ' %(host_id,self.vid,str(optimal_rate))
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
        return optimal_rate # }}}
    def send_rates(self,end_host_conn, optimal_rate, end_host_socket): # {{{
        print 'send optimal_rate = ' +str(optimal_rate) +' to EndHost ' +str(end_host_socket[1][0]), self.vid
        end_host_conn.send(str(optimal_rate)) # }}}
    def connect_to_endhosts(self): # {{{
        s = self.listen_for_endhosts()
        while len(self.end_host_sockets) < self.NUM_SOURCES:
            conn, addr = s.accept()
            print 'Accept a connect request from address = ' +str(addr), self.vid
            print 'Accept a connect request from conn = ' +str(conn), self.vid
            
            #Accept a connect request from address = ('192.168.0.14', 39023) eng
            self.end_host_sockets.append((conn, addr))
    def run(self):
        #----- Connect to endhosts and put all connection_id to end_host_sockets
        self.connect_to_endhosts()  #
        print "TRI.server: end_host_sockets = "
        for end_host_socket in self.end_host_sockets:
            print end_host_socket
        #TRI.server: end_host_sockets =
        #(<socket._socketobject object at 0x1440280>, ('192.168.0.14', 35619))
        #(<socket._socketobject object at 0x143ed00>, ('192.168.0.15', 58468))
           
        #----------------- Get max rate of all endhosts and put to max_rate_list
        while True:
<<<<<<< HEAD
#            if self.vid == 'eng':
#                print 'TRI.server:eng_capa = \n', self.capa,
#            else:
#                print 'TRI.server:sci_capa = \n', self.capa,
=======
            if self.vid == 'eng':
                print 'TRI.server:eng_capa = ', self.capa
            else:
                print 'TRI.server:sci_capa = ', self.capa
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
            for end_host_socket in self.end_host_sockets:
                #end_host_socket = (conn,addr)
                host_id = end_host_socket[1][0]
                end_host_conn = end_host_socket[0]
                print "TRI.server: host_id = " +str(host_id)
                print "TRI.server: end_host_conn = " + str(end_host_conn)
                #TRI.server: host_id = 192.168.0.14
                #TRI.server: end_host_conn = <socket._socketobject object at 0xe3a210>

                temp = self.get_max_rate(end_host_conn, host_id)
                self.max_rate_dict[host_id] = int(temp) 
                self.max_rate_list.append(self.max_rate_dict[host_id])
            #----------------------------- # Calculate optimal rate for all endhosts
            #endhost_weight = [float(self.max_rate_list[i])/sum(self.max_rate_list) for i in range(len(self.max_rate_list))] # }}}
<<<<<<< HEAD
            print 'TRI.server: max_rate_list = ', self.max_rate_list, self.vid
=======
            print 'TRI.server: max_rate_list = \n'
            print self.max_rate_list
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
            all_opt_rate,cp_all = self.nw_opt_rate(self.max_rate_list) 
            self.max_rate_list = []
            #--------------------------------------Send optimal rate to all endhosts
            for end_host_socket in self.end_host_sockets:
                host_id = end_host_socket[1][0]
                end_host_conn = end_host_socket[0]
                self.optimal_rate_dict[host_id] = self.end_opt_rate(host_id, self.max_rate_dict[host_id],all_opt_rate)
                self.send_rates(end_host_conn, self.optimal_rate_dict[host_id], end_host_socket)
            self.cv.acquire()
            self.Q.append(cp_all)
            self.cv.notify()
            self.cv.release()
<<<<<<< HEAD
            time.sleep(self.period)
=======
            time.sleep(self.wait)
>>>>>>> 0218ac36aeeff6c9857cf218080c5f46cdafa5ba
            # }}}
class Nox(Thread):
    def __init__(self,conn,Q,cv):
        Thread.__init__(self)
        self.conn = conn
        self.Q = Q
        self.cv = cv
        print "conn = ", conn
    def run(self,):
        i = 0
        while True:
            msg = self.conn.recv(1024)
            if i%2 == 0: 
                print "port_down"
                data.sub_capa[1]= 0
            else: 
                print "port_up"
                data.sub_capa[1] = 51.20
            i += 1        
    
