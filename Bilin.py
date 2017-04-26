#!/usr/bin/env python3

import math
import numpy as np
import numpy.random as rd
import pickle as pk
import matplotlib.pyplot as plt

class Bilin:
    _miss_val = -31*math.log(2)/math.log(10);
    def __init__(self, d, sig_noise, miss, sig_rc_0):
        self.d = d;
        self.D = d*d;
        self.sig_noise = sig_noise;
        self.miss = miss;
        # draw matrix for quadratic form
        self.theta_mat = rd.rand(d,d)-0.5;
        # coefficients for linear or constant terms modulated
        self.theta_mat[0,:] *= sig_rc_0;
        self.theta_mat[:,0] *= sig_rc_0;
        # draw column permutation
        self.perm = rd.permutation(self.D);
        ## make sure the fixed-facto column is not the regression target
        #while ( self.perm[0] == self.D-1 ):
        #    self.perm = rd.permutation(self.D);
        # print(self.theta_mat)

    def gen_data(self,N):
        # draw vectors
        a = rd.rand(N,self.d)-0.5;
        a[:,0]=1;
        b = rd.rand(N,self.d)-0.5;
        b[:,0]=1;
        # draw noise
        vals = self.sig_noise*rd.randn(N,self.D);
        col = 0;
        # add quadratic form
        for i in range(self.d):
            for j in range(self.d):
                vals[:, self.perm[col]] += self.theta_mat[i,j]*np.multiply(a[:,i],b[:,j]);
                col += 1;
        # draw missingness
        keep = np.zeros((N,self.D), dtype=bool);
        keep = rd.rand(N,self.D)>self.miss;
        ## make sure last column is kept
        #keep[:,self.D-1] = True;
        out = np.multiply(keep,vals)+(1-keep)*Bilin._miss_val;
        return out;

def main():

    d = 10;
    sig_noise = 0.1;
    classes = ['plus_1','minus_1']
    miss = 0.1;
    sig_rc_0 = 0.1;
    N = 100000;

    for cls in classes:
        fname = "class_"+cls+".txt.gz"
        #print "Creating "+fname;
        sim = Bilin(d,sig_noise, miss, sig_rc_0);
        np.savetxt(fname,sim.gen_data(N),"%7.3f");


def drawdata():

    d = 10;
    sig_noise = 0.1;
    classes = ['plus_1','minus_1']
    miss = 0;
    sig_rc_0 = 0.1;
    N = 500;

    sim = Bilin(d,sig_noise, miss, sig_rc_0);
    a1 = sim.gen_data(N)
    a1 = np.round(a1, 3)
    b1 = np.repeat(1, repeats=N)

    sim = Bilin(d,sig_noise, miss, sig_rc_0);
    a2 = sim.gen_data(N)
    a2 = np.round(a2, 3)
    b2 = np.repeat(-1, repeats=N)

    a = np.concatenate( (a1,a2) )
    b = np.concatenate( (b1,b2) )

    pk.dump( obj=a, file=open('Data_x.pkl', 'wb') )
    pk.dump( obj=b, file=open('Data_y.pkl', 'wb') )

    #plt.hist(a[0,:], bins=200)
    # plt.hist(a)
    # plt.show()


drawdata()
