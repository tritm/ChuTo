#! /usr/bin/env python
from server import *
from cvxopt import matrix
import numpy, time
def initvar():
    global eng_Q, sci_Q, eng_cv, sci_cv, L, sub_capa, eng_capa, sci_capa
    global eng_capa_temp, sci_capa_temp, socket_wait_time
    socket_wait_time = 60
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
def get_cp(cv, Q):
    # cv: conditional variable, Q: queue
    cv.acquire()
    while not Q:
        cv.wait()
    cp = eng_Q.pop()
    cv.release()
    return cp
initvar()
eng = Vncal('eng', eng_Q, eng_cv, eng_capa)
eng.start()
   