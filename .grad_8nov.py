#!/usr/bin/python
from cvxopt import solvers, matrix, spdiag, log
import numpy, math
def optFunc():
    NULL = 1e-300
    I = 2; J = 2; L = 3; IJ = I*J
    GH1 = numpy.array([[NULL for ij in range(IJ)] for l in range(L)])
    #c = matrix(5*numpy.ones((L)))
    c = matrix([numpy.random.randint(10,1000) for i in range(L)])
    rhs2st = matrix(numpy.zeros(IJ))
    H = [[[0. for j in range(J)] for l in range(L)] for i in range(I)]
    H[0][0][0] = 1.
    H[0][1][1] = 1.
    H[0][2][0] = 1.
    H[1][0][0] = 1.
    H[1][1][1] = 1.
    H[1][2][0] = 1.
    q = 1
    def utility(z):
        u = numpy.empty((L))
        u1 = lambda l: 1./c[l]*(sum(sum(H[i][l][j]*z[i][j] for j in range(J)) for i in range(I)))
        for l in range(L): u[l] = u1(l)
        return u

    def hfunc(m,n,p,k,z):
        u = utility(z)
        if m==p and n==k: 
            return 1./sum(z[m][j] for j in range(J))**2 +\
                   q*sum(((H[m][l][n]/c[l])**2)*math.exp(u[l]) for l in range(L))
        elif m==p:
            return 1./sum(z[m][j] for j in range(J))**2 +\
                    q*sum((H[m][l][n]*H[p][l][k]/c[l]**2)*math.exp(u[l]) for l in range(L))
        else:
            return q*sum(H[m][l][n]*H[p][l][k]/(c[l]**2)*math.exp(u[l]) for l in range(L))
    def func(x):
        z = numpy.reshape(x,(I,J))
        u = utility(z)
        f = -sum(log(sum(z[i][j] for j in range(J))) for i in range(I)) + q*sum(math.exp(u[l]) for l in range(L))
        return f
    def gradFunc(x):
        z = numpy.reshape(x,(I,J))
        Df = numpy.empty((I,J))
        u = utility(z)
        df1 = lambda m,n: -1./sum(z[m][j] for j in range(J)) + \
                          q*sum(H[m][l][n]/c[l]*math.exp(u[l]) for l in range(L))
        for i in range(I):
            for j in range(J):
                Df[i][j] = df1(i,j)
        Df1 =  matrix(numpy.reshape(Df, (IJ)))
        return Df1.T
    def hessianFunc(x):
        z = numpy.reshape(x,(I,J))
        Hf = numpy.empty((I,J,I,J))
        for m in range(I):
            for n in range(J):
                for p in range(I):
                    for k in range(J):
                        Hf[m][n][p][k] = hfunc(m,n,p,k,z)
        Hf1 = matrix(numpy.reshape(Hf,(IJ,IJ)))
        return Hf1         
                    
    def F(x=None, z=None):
        n = I*J
        if x is None: return 0, matrix(1.0,(n,1))
        if min(x) <= 0.:return None
        f = func(x)
        Df = gradFunc(x)
        if z is None: return f,Df
        H = hessianFunc(x) 
        return f,Df,H

    for l in range(L):
        for i in range(I):
            for j in range(J):
                GH1[l][i*J+j] = H[i][l][j]
    GH = matrix(GH1)
    DI = -numpy.identity(IJ)
    G = matrix(numpy.vstack((GH,DI)))

    h = matrix(numpy.vstack((c,rhs2st)))
    print type(h)
    sol = solvers.cp(F,G,h)
    return sol['x']

        
