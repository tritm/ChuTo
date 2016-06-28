from grad import *
from numpy import reshape
import numpy
from server import *

def printMatrix(testMatrix):
    print numpy.asarray(testMatrix, float, (6,2))

def testNetcal():
    t = Netcal()
    max_rate_list = [1, 15]
    H = t.routing_matrix()
    all_opt_rate,cp_all = t.optFunc(max_rate_list)
    print all_opt_rate
    print sum(all_opt_rate)
def testVncal():
    eng_Q = []
    eng_cv = Condition()
    eng_capa = [5, 5, 5]
    data.period = 5
    eng = Vncal('eng', eng_Q, eng_cv, eng_capa,data.period)
    eng.start()
if __name__ == "__main__":
    testVncal()
    