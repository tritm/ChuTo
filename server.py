#!/usr/bin/pythoj
import socket, time
from grad import *
from threading import Thread, Condition
class Vncal(Thread):
    def __init__(self,vid,Q,cv,capa,wait): # {{{
        Thread.__init__(self)
        self.MGR_IP_ADDRESS = '203.178.135.32'
        self.NUM_SOURCES = 2
        self.Q = Q
        self.cv = cv
        self.capa = capa
        self.end_host_sockets = []
        self.max_rate_dict = {}
        self.max_rate_list = []
        self.optimal_rate_dict = {}
        self.wait = wait
        self.vid = vid
        if vid == 'eng':
            self.MGR_PORT = 1890
        else:
            self.MGR_PORT = 1990 # }}}
    def update(self,capa):
        self.capa = capa
    def listen_for_endhosts(self): # {{{
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.MGR_IP_ADDRESS, self.MGR_PORT))
        print 'Listen for connect requests from EndHosts...', self.vid
        s.listen(self.NUM_SOURCES)
        return s # }}}
    def get_max_rate(self,end_host_conn, host_id): # {{{
        print 'Ask EndHost %s for wanted max_rate...' %host_id, self.vid
        end_host_conn.send('max_rate_kbps?')
        max_rate = end_host_conn.recv(1024)
        print 'received max_rate = ' +max_rate +' from EndHost: ' +host_id, self.vid
        return max_rate # }}}
    def nw_opt_rate(self,endhost_weight): # {{{
        c = Netcal(capa = self.capa)
        all_opt_rate,cp_all = c.optFunc(endhost_weight)
        length = all_opt_rate.size[0]
        for i in range(length): 
            if all_opt_rate[i] < 1e-3: all_opt_rate[i] = 0
        return all_opt_rate,cp_all # }}}
    def end_opt_rate(self,host_id, max_rate,all_opt_rate): # {{{
        print 'Calculate optimal rates for EndHost %s ...' %host_id, self.vid  # {{{ # {{{
        if host_id == '203.178.135.103': #TA
            optimal_rate = tuple(all_opt_rate[0:2])
        elif host_id == '203.178.135.113': #TB
            optimal_rate = tuple(all_opt_rate[2:4])
        print 'optimal_rate (Mbps) for EndHost %s = %s ' %(host_id,str(optimal_rate)), self.vid
        print 'optimal_rate (pps)for EndHost %s = %s ' %(host_id,str(tuple(83.33333*s for s in optimal_rate))), self.vid
        return optimal_rate # }}}
    def send_rates(self,end_host_conn, optimal_rate, end_host_socket): # {{{
        print 'send optimal_rate = ' +str(optimal_rate) +' to EndHost ' +str(end_host_socket[1][0]), self.vid
        end_host_conn.send(str(optimal_rate)) # }}}
    def connect_to_endhosts(self): # {{{
        s = self.listen_for_endhosts()
        while len(self.end_host_sockets) < self.NUM_SOURCES:
            conn, addr = s.accept()
            print 'Accept a connect request from address = ' +str(addr), self.vid
            self.end_host_sockets.append((conn, addr))
    def run(self):
        #----- Connect to endhosts and put all connection_id to end_host_sockets
        self.connect_to_endhosts()  #
        #----------------- Get max rate of all endhosts and put to max_rate_list
        while True:
            print 'TRI.server:self.capa = ', self.capa
            for end_host_socket in self.end_host_sockets:
                host_id = end_host_socket[1][0]
                end_host_conn = end_host_socket[0]
                temp = self.get_max_rate(end_host_conn, host_id)
                print temp
                self.max_rate_dict[host_id] = int(temp) 
                self.max_rate_list.append(self.max_rate_dict[host_id])
            #----------------------------- # Calculate optimal rate for all endhosts
            endhost_weight = [float(self.max_rate_list[i])/sum(self.max_rate_list) for i in range(len(self.max_rate_list))] # }}}
            all_opt_rate,cp_all = self.nw_opt_rate(endhost_weight) 
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
            time.sleep(self.wait*6)
            # }}}
        
    
