# -*- coding: utf-8 -*-
'''
Created on 28.11.2012

@author: tim
'''

import numpy as np

class mapping(object):
    void = 0
    visited = 1 
    start = 2 
    target = 192
    wall = 255
    portal = 129
    loader = 128
    
    index = {void : " ", visited : ".", start : "S",
             target: "X", wall : "#", portal : "O",
             loader : "E"
            }
    
    
    def __init__(self, size=1):
        self.map = np.zeros((size, size), int)
        self.size = size
        # set startpoint on middle
        self.map[self.size / 2][self.size / 2] = self.start
        
    def update(self, x, y, value):
        if(self.map[y][x] != self.start):
            self.map[y][x] = value
        
    def printFile(self):
        mapFile = open("map.txt","w")
        for i in range(self.size):
            for t in range(self.size):
                mapFile.write("%s " % (self.index[self.map[i][t]]))
                    
                if t == self.size - 1:
                    mapFile.write("\t%i\n"%(i+1))
                 
        mapFile.write("\n")   
        
        for i in range(1, self.size + 1):
            if (i%2 == 1) and (i < 10):
                mapFile.write("%i   " % i)
            elif (i%2 == 1) and (i < 100):
                mapFile.write("%i  " % i)
            elif (i%2 == 1):
                mapFile.write("%i " % i)
                 
        mapFile.write("\n")
                    
        for i in range(1, self.size + 1):
            if (i%2 == 0) and (i < 10):
                mapFile.write("  %i " % i)
            elif (i%2 == 0) and (i < 100):
                mapFile.write("  %i" % i)
            elif (i%2 == 0):
                mapFile.write(" %i" % i)
        
        mapFile.close()
