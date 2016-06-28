#! /usr/bin/env python
from server import *
from cvxopt import matrix
import numpy, time
def initvar(): # {{{
    global eng_Q, sci_Q, eng_cv, sci_cv, L, sub_capa, eng_capa, sci_capa
    global eng_capa_temp, sci_capa_temp, wait, delta
    eng_Q = []
    sci_Q = []
    eng_cv = Condition()
    sci_cv = Condition()
    L = 3
    sub_capa = matrix(.2 * numpy.ones(L))
    eng_capa = matrix(.1*numpy.ones(L))
    sci_capa = matrix(.1*numpy.ones(L))
    eng_capa_temp = matrix(-1000*numpy.ones(L))
    sci_capa_temp = matrix(-1000*numpy.ones(L))
    wait = 10
    delta = .001# }}}
def get_cp(cv, Q): # {{{
    # cv: conditional variable, Q: queue
    cv.acquire()
    while not Q:
        cv.wait()
    cp = Q.pop()
    cv.release()
    return cp # }}}
initvar() # {{{
eng = Vncal('eng', eng_Q, eng_cv, eng_capa,wait)
eng.start()
sci = Vncal('sci', sci_Q, sci_cv, sci_capa,wait)
sci.start() # }}}
while True: # {{{
    #------------------------------------------------------ get congestion price
    eng_cp_all = get_cp(eng_cv,eng_Q)
    sci_cp_all = get_cp(sci_cv,sci_Q)
    eng_cp = eng_cp_all[0:L]
    sci_cp = sci_cp_all[0:L]
    print 'TRI.hm: eng_cp = \n', eng_cp
    print 'TRI.hm: sci_cp = \n', sci_cp
    #--------------------------------------- calculate new virtual link capacity
    for l in range(L):
        eng_capa_temp[l] = eng_capa[l] + delta*(sci_cp[l]- eng_cp[l])/2
        sci_capa_temp[l] = sci_capa[l] + delta*(eng_cp[l] - sci_cp[l])/2
    #-------------- re-normalize to make eng_capa[l] + sci_capa[l] = sub_capa[l]
    for l in range(L):
        eng_capa[l] = eng_capa_temp[l]/(eng_capa_temp[l]+sci_capa_temp[l])*sub_capa[l]
        sci_capa[l] = sci_capa_temp[l]/(eng_capa_temp[l]+sci_capa_temp[l])*sub_capa[l]
    #----------------------------------------- update back to eng and sci object
    print "TRI.hm: eng_capa = \n", eng_capa
    print "TRI.hm: sci_capa = \n", sci_capa
    eng.update(eng_capa)
    sci.update(sci_capa)
    
    #----------------------------------------time.sleep(wait) # }}}
    
