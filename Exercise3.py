# -*- coding: utf-8 -*-
"""
Created on Sun May 07 13:53:33 2017

@author: Molli
"""
import numpy as np
import matplotlib.pyplot as plt
import math

#returns distance between the transmitter and given location of car in meters
def distance(lat2, lon2):
    #transmitter location
    lat1 = 7.096981
    lon1 = 50.707211
    
    #radius of earth in meters    
    radius = 6371 * 1000 

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    d = 2 * radius * math.asin(math.sqrt(a))

    return d

#path loss calculated using FSP + TRG model
def PL_FSP_TRG(D):
    y = 1.35
    ht = 50.0
    hr = 2.0
    
    dc = (4*np.pi*ht*hr)/y
    
    PL_FT = []
    for i in range(0,len(D)):
        d=D[i]
        if d<=dc:
            ratio = (16*math.pow(d,2)*math.pow(np.pi,2))/(math.pow(y,2))
        else:
            ratio = math.pow(d,4)/(math.pow(ht,2)*math.pow(hr,2))
        PL_FT.append(10 * math.log(ratio,10))

    return PL_FT
    
#path loss calculated using TLD model
def PL_TLD(D):
    d0 = 1.0
    d1 = 200.0
    d2 = 500.0
    n0 = 2.0
    n1 = 3.0
    n2 = 3.0
    L0 = 19.377
    
    PL_TD = []
    for i in range(0,len(D)):
        d=D[i]
        if d<d0:
            PL_TD.append(0)
        elif d0<=d and d<d1:
            PL_TD.append(L0 + 10*n0*math.log(d/d0,10))
        elif d1<=d and d<d2:
            PL_TD.append(L0 + 10*n0*math.log(d1/d0,10) + 10*n1*math.log(d/d1,10))
        else:
            PL_TD.append(L0 + 10*n0*math.log(d1/d0,10) + 10*n1*math.log(d2/d1,10) + 10*n2*math.log(d/d2,10))
           
    return PL_TD          
    
def main():
    Dlist = [] #for list of distances from transmitter
    Signal = [] #for list of measured relative signal strengths
    with open('ex1.csv', 'rb') as csvfile:
        for row in csvfile.readlines():
            array = row.split(',')
            dist = distance ( float(array[2]), float(array[1]))
            Dlist.append(dist)
            Signal.append(array[3])
               
    D = np.asarray(Dlist,dtype=float)
    
    PL_FT = PL_FSP_TRG(D)
    
    PL_TL = PL_TLD(D)
    
    #Display plots for both the models 
    plt.plot(D,PL_FT,'r',D,PL_TL,'b')
    plt.ylabel('Path Loss [dB]')
    plt.xlabel('Distance [m]')
    plt.show()
    
    #Display plots for measured relative signal strength
    plt.plot(D,Signal)
    plt.ylabel('Relative Signal Strength')
    plt.xlabel('Distance [m]')
    plt.show()
    

if __name__ == '__main__': # boilerplate code to invoke main()
    main()