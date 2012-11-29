# -*- coding: utf-8 -*-
'''
Created on 28.11.2012

@author: tim
'''

import numpy as np

class mapping(object):
    void, visited, start, target, wall, portal, loader = range(7)
    state_names = ("void", "visited", "start", 
                   "target", "wall", "portal", 
                   "loader")
    char = (" ", ".", "S", "X", "#", "O", "U")
    
    def __init__(self, size=1):
        self.map = np.zeros((size, size), int)
        self.size = size
        
    def update(self, x, y, value):
        self.map[y][x] = self.state_names.index(value)
        
    def printFile(self):
        mapFile = open("map.txt","w")
        for i in range(self.size):
            for t in range(self.size):
                mapFile.write("%s " % (self.char[self.map[i][t]]))
                    
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
