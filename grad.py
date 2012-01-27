#!/usr/bin/python
from cvxopt import solvers, matrix, spdiag, log
import numpy, math
logfile = open('grad.log', 'w')
class Netcal(object):
    def routing_matrix(self): # {{{
        H = [[[0. for j in range(self.J)] for l in range(self.L)] for i in range(self.I)]
        H[0][0][0] = 1.
        H[0][1][1] = 1.
        H[0][2][0] = 1.
        H[1][0][0] = 1.
        H[1][1][1] = 1.
        H[1][2][0] = 1.
        return H # }}}
<<<<<<< HEAD
    def __init__(self,q=0.001,NULL = 1e-300, I = 2, J = 2, L = 3, capa = -1): # {{{
=======
    def __init__(self,q=0.001,NULL = 1e-300, I = 2, J = 2, L = 3, H = 0): # {{{
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
        self.q = q
        self.NULL = NULL
        self.I = I
        self.J = J
        self.L = L
        self.IJ = I*J
        self.GH1 = numpy.array([[NULL for ij in range(self.IJ)] for l in range(self.L)])
<<<<<<< HEAD
        self.capa = capa
        self.rhs2st = matrix(numpy.zeros(self.IJ))
        self.H = self.routing_matrix() # }}}
        print 'TRI.grad: self.capa = ', self.capa, 
        print 'TRI.grad: self.rhs2st = ', self.rhs2st 
    def utility(self,z): # {{{
        u = numpy.empty((self.L))
        u1 = lambda l: 1. / self.capa[l] * (sum(sum(self.H[i][l][j] * z[i][j] for j in range(self.J)) for i in range(self.I)))
=======
        self.c = matrix(1 * numpy.ones((self.L)))
        self.rhs2st = matrix(numpy.zeros(self.IJ))
        if H == 0:
            self.H = self.routing_matrix() # }}}
        else:
            self.H = H
    def utility(self,z): # {{{
        u = numpy.empty((self.L))
        u1 = lambda l: 1. / self.c[l] * (sum(sum(self.H[i][l][j] * z[i][j] for j in range(self.J)) for i in range(self.I)))
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
        for l in range(self.L): u[l] = u1(l)
        return u # }}}
    def hfunc(self,m, n, p, k, z): # {{{
        u = self.utility(z)
        if m == p and n == k: 
            return self.endhost_weight[m] / sum(z[m][j] for j in range(self.J)) ** 2 + \
<<<<<<< HEAD
                   self.q * sum(((self.H[m][l][n] / self.capa[l]) ** 2) * math.exp(u[l]) for l in range(self.L))
        elif m == p:
            return self.endhost_weight[m] / sum(z[m][j] for j in range(self.J)) ** 2 + \
                    self.q * sum((self.H[m][l][n] * self.H[p][l][k] / self.capa[l] ** 2) * math.exp(u[l]) for l in range(self.L))
        else:
            return self.q * sum(self.H[m][l][n] * self.H[p][l][k] / (self.capa[l] ** 2) * math.exp(u[l]) for l in range(self.L)) # }}}
=======
                   self.q * sum(((self.H[m][l][n] / self.c[l]) ** 2) * math.exp(u[l]) for l in range(self.L))
        elif m == p:
            return self.endhost_weight[m] / sum(z[m][j] for j in range(self.J)) ** 2 + \
                    self.q * sum((self.H[m][l][n] * self.H[p][l][k] / self.c[l] ** 2) * math.exp(u[l]) for l in range(self.L))
        else:
            return self.q * sum(self.H[m][l][n] * self.H[p][l][k] / (self.c[l] ** 2) * math.exp(u[l]) for l in range(self.L)) # }}}
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
    def func(self,x): # {{{
        z = numpy.reshape(x, (self.I, self.J))
        u = self.utility(z)
        f = -sum(self.endhost_weight[i] * log(sum(z[i][j] for j in range(self.J))) for i in range(self.I)) + self.q * sum(math.exp(u[l]) for l in range(self.L))
        return f # }}}
    def gradFunc(self,x): # {{{
        z = numpy.reshape(x, (self.I, self.J))
        Df = numpy.empty((self.I, self.J))
        u = self.utility(z)
        df1 = lambda m, n:-self.endhost_weight[m] / sum(z[m][j] for j in range(self.J)) + \
<<<<<<< HEAD
                          self.q * sum(self.H[m][l][n] / self.capa[l] * math.exp(u[l]) for l in range(self.L))
=======
                          self.q * sum(self.H[m][l][n] / self.c[l] * math.exp(u[l]) for l in range(self.L))
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
        for i in range(self.I):
            for j in range(self.J):
                Df[i][j] = df1(i, j)
        Df1 = matrix(numpy.reshape(Df, (self.IJ)))
        return Df1.T # }}}
    def hessianFunc(self,x): # {{{
        z = numpy.reshape(x, (self.I, self.J))
        Hf = numpy.empty((self.I, self.J, self.I, self.J))
        for m in range(self.I):
            for n in range(self.J):
                for p in range(self.I):
                    for k in range(self.J):
                        Hf[m][n][p][k] = self.hfunc(m, n, p, k, z)
        Hf1 = matrix(numpy.reshape(Hf, (self.IJ, self.IJ)))
        return Hf1          # }}}
    def F(self,x=None, z=None): # {{{
        n = self.I * self.J
        if x is None: return 0, matrix(1.0, (n, 1))
        if min(x) <= 0.:return None
        f = self.func(x)
        Df = self.gradFunc(x)
        if z is None: return f, Df
        H = self.hessianFunc(x) 
        return f, Df, H # }}}
    def optFunc(self,endhost_weight): # {{{
        self.endhost_weight = endhost_weight
        for l in range(self.L):
            for i in range(self.I):
                for j in range(self.J):
                    self.GH1[l][i * self.J + j] = self.H[i][l][j]
        GH = matrix(self.GH1)
        DI = -numpy.identity(self.IJ)
        G = matrix(numpy.vstack((GH, DI)))
<<<<<<< HEAD
        h = matrix(numpy.vstack((self.capa, self.rhs2st)))
        sol = solvers.cp(self.F, G, h)
        # sol['zl']: congestion price for linear constraints [0:3]:constraints for l1,l2,l3; [4:8]: constraints for z >= 0
        return sol['x'], sol['zl'] # }}}
logfile.close 
   
=======
        h = matrix(numpy.vstack((self.c, self.rhs2st)))
        sol = solvers.cp(self.F, G, h)
        return sol['x'] # }}}
logfile.close    
>>>>>>> f97112a8e44922f10ce183986a0a7e6da45df35f
    
            
    
