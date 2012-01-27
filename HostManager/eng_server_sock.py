<<<<<<< HEAD
#!/usr/bin/python
=======
#!/usr/bin/python # {{{
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
import socket, time
from grad import *
c = Netcal()
end_host_sockets = []
max_rate_dict = {}
max_rate_list = []
optimal_rate_dict = {}
socket_wait_time = 60
<<<<<<< HEAD
NUM_SOURCES = 2
=======
NUM_SOURCES = 2 # }}}
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
def listen_for_endhosts(): # {{{
    MGR_IP_ADDRESS = '203.178.135.32'
    MGR_PORT = 1890
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((MGR_IP_ADDRESS, MGR_PORT))
    print 'Listen for connect requests from EndHosts...'
    s.listen(NUM_SOURCES)
    return s # }}}
def get_max_rate(end_host_conn, host_id): # {{{
    print 'Ask EndHost %s for wanted max_rate...' %host_id
    end_host_conn.send('max_rate_kbps?')
    max_rate = end_host_conn.recv(1024)
    print 'received max_rate = ' +max_rate +' from EndHost: ' +host_id
    return max_rate # }}}
def nw_opt_rate(endhost_weight): # {{{
<<<<<<< HEAD
    print endhost_weight
    all_opt_rate = c.optFunc(endhost_weight)
    print 'TRI'
    print all_opt_rate
=======
    all_opt_rate = c.optFunc(endhost_weight)
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
    length = all_opt_rate.size[0]
    for i in range(length): 
        if all_opt_rate[i] < 1e-3: all_opt_rate[i] = 0
    return all_opt_rate # }}}
def end_opt_rate(host_id, max_rate,all_opt_rate): # {{{
    print 'Calculate optimal rates for EndHost %s ...' %host_id 
    if host_id == '203.178.135.103': #TA
        optimal_rate = tuple(all_opt_rate[0:2])
    elif host_id == '203.178.135.113': #TB
        optimal_rate = tuple(all_opt_rate[2:4])
    print 'optimal_rate (Mbps) for EndHost %s = %s ' %(host_id,str(optimal_rate))
    print 'optimal_rate (pps)for EndHost %s = %s ' %(host_id,str(tuple(83.33333*s for s in optimal_rate)))
    return optimal_rate # }}}
def send_rates(end_host_conn, optimal_rate): # {{{
    print 'send optimal_rate = ' +str(optimal_rate) +' to EndHost ' +str(end_host_socket[1][0])
    end_host_conn.send(str(optimal_rate)) # }}}
def connect_to_endhosts(): # {{{
    s = listen_for_endhosts()
    while len(end_host_sockets) < NUM_SOURCES:
        conn, addr = s.accept()
        print 'Accept a connect request from address = ' +str(addr)
        end_host_sockets.append((conn, addr))
    return  end_host_sockets  # }}}
end_host_sockets = connect_to_endhosts() # {{{
while True:
    for end_host_socket in end_host_sockets:
        host_id = end_host_socket[1][0]
        end_host_conn = end_host_socket[0]
        temp = get_max_rate(end_host_conn, host_id)
        print temp
        max_rate_dict[host_id] = int(temp) 
        max_rate_list.append(max_rate_dict[host_id])
    # Calculate optimal rate for all endhosts
    endhost_weight = [float(max_rate_list[i])/sum(max_rate_list) for i in range(len(max_rate_list))]
    all_opt_rate = nw_opt_rate(endhost_weight)  
    # Send optimal rate to endhosts
    for end_host_socket in end_host_sockets:
        host_id = end_host_socket[1][0]
        end_host_conn = end_host_socket[0]
        optimal_rate_dict[host_id] = end_opt_rate(host_id, max_rate_dict[host_id],all_opt_rate)
        send_rates(end_host_conn, optimal_rate_dict[host_id])
    time.sleep(socket_wait_time)
s.close() # }}}
    
