# -*- coding: utf-8 -*-
"""
Created on Sun May 07 13:53:33 2017

@author: Molli
"""
import numpy as np
import matplotlib.pyplot as plt
import math

#path loss calculated using FSP + TRG model
def PL_FSP_TRG(D):
    y = input('Enter wavelength: ')
    ht = input('Enter transmitter antenna height: ')
    hr = input('Enter reciever antenna height: ')
    
    dc = (4*np.pi*ht*hr)/y
    PL = np.linspace(1,10000,10000)
    for i in range(1,10000):
        d=D[i]
        if d<=dc:
            ratio = (16*math.pow(d,2)*math.pow(np.pi,2))/(math.pow(y,2))
        else:
            ratio = math.pow(d,4)/(math.pow(ht,2)*math.pow(hr,2))
        PL[i] = 10 * math.log(ratio,10)
    
    plt.plot(D,PL)
    plt.ylabel('Path Loss [dB]')
    plt.xlabel('Distance [m]')
    plt.show()

#path loss calculated using TLD model
def PL_TLD(D):
    d0 = input('Enter first distance field:  ')
    d1 = input('Enter second distance field: ')
    d2 = input('Enter third distance field:  ')
    n0 = input('Enter first path loss distance exponent:  ')
    n1 = input('Enter second path loss distance exponent: ')
    n2 = input('Enter third path loss distance exponent:  ')
    L0 = input('Path loss at reference distance d0: ')
    
    PL = np.linspace(1,10000,10000)
    for i in range(1,10000):
        d=D[i]
        if d<d0:
            PL[i]=0
        elif d0<=d and d<d1:
            PL[i] = L0 + 10*n0*math.log(d/d0,10)
        elif d1<=d and d<d2:
            PL[i] = L0 + 10*n0*math.log(d1/d0,10) + 10*n1*math.log(d/d1,10)
        else:
            PL[i] = L0 + 10*n0*math.log(d1/d0,10) + 10*n1*math.log(d2/d1,10) + 10*n2*math.log(d/d2,10)
           
    plt.plot(D,PL)
    plt.ylabel('Path Loss [dB]')
    plt.xlabel('Distance [m]')
    plt.show()          
    
def main():
    D = np.linspace(1,10000,10000)  #Distance values  

    PL_FSP_TRG(D)
    PL_TLD(D)

if __name__ == '__main__': # boilerplate code to invoke main()
    main()