# Tutorial Controller
# Starts as a hub, and your job is to turn this into a learning switch.

import logging

from nox.lib.core import *
import nox.lib.openflow as openflow
from nox.lib.packet.ethernet import ethernet
from nox.lib.packet.packet_utils import mac_to_str, mac_to_int

#import sys
#PYDEVD_PATH = '/home/tritm/.eclipse/org.eclipse.platform_3.7.0_155965261/plugins/org.python.pydev.debug_2.2.2.2011082312/pysrc'
#if sys.path.count(PYDEVD_PATH)<1:
#    sys.path.append(PYDEVD_PATH)
#import pydevd
#pydevd.settrace('203.178.135.99', port=5678,stdoutToServer=True,stderrToServer=True)

log = logging.getLogger('nox.coreapps.examples.pyswitch')

class pyswitch(Component):  
    
    def __init__(self, ctxt):
        Component.__init__(self, ctxt)
        # Dict mac_to_port_i to store the bridge table of dp_id = i
        
    def datapath_join_callback(self,dpid,stats):
        log.info('dpid = %s',dpid)
        attrs = {}
        if dpid == 1:
            attrs[1] = {core.IN_PORT:1,core.DL_VLAN:2}
            outport =  2
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[1], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
            attrs[2] = {core.IN_PORT:2, core.DL_VLAN:2}
            outport = 1
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[2], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
            attrs[3] = {core.IN_PORT:1, core.DL_VLAN:3}
            outport = 3
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[3], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
            attrs[4] = {core.IN_PORT:3, core.DL_VLAN:3}
            outport = 1
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[4], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)                            
        elif dpid == 2:
            attrs[5] = {core.IN_PORT:1,core.DL_VLAN:2}
            outport =  2
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[5], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
            attrs[6] = {core.IN_PORT:2,core.DL_VLAN:2}
            outport =  1
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[6], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
        elif dpid == 3:
            attrs[7] = {core.IN_PORT:2,core.DL_VLAN:2}
            outport =  1
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[7], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
            attrs[8] = {core.IN_PORT:1, core.DL_VLAN:2}
            outport = 2
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[8], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)
            attrs[9] = {core.IN_PORT:2, core.DL_VLAN:3}
            log.info('TRI:inport 2,vlan 3')
            outport = 3
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[9], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)  
            attrs[10] = {core.IN_PORT:3, core.DL_VLAN:3}
            outport = 2 
            actions = [[openflow.OFPAT_OUTPUT, [0, outport]]]
            self.install_datapath_flow(dp_id = dpid, attrs = attrs[10], idle_timeout = 0,
                                       hard_timeout = 0, actions = actions, buffer_id = None,
                                       priority = openflow.OFP_DEFAULT_PRIORITY, inport = None,
                                       packet = None)            
    def install(self):
        self.register_for_datapath_join(lambda dpid, stats : 
                                        self.datapath_join_callback(dpid,stats))
    def getInterface(self):
        return str(pyswitch)
    
def getFactory():
    class Factory:
        def instance(self, ctxt):
            return pyswitch(ctxt)

    return Factory()
