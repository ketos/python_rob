# -*- coding: utf-8 -*-
'''
Created on 28.11.2012

@author: tim
'''

import numpy as np

class mapping(object):
    void = -1 
    start = 20 
    target = 192
    wall = 255
    portal = 129
    loader = 128 

    north = 0
    east = 1
    south = 2
    west = 3
    
    dir_names = {
                    0 : "front", 1 : "right", 2 : "back", 3 : "left"
                }
    
    index = {void : " ", start : "S",
             target: "X", wall : "#", portal : "O",
             loader : "E", north : "^", east : ">" ,
             south : "v" , west : "<"
            }
            
        # Relative Coordinates of Front, Right, Back, Left
    # y and x are in inverted order due to array implementation
    # Example (North):        front
    #                        (-1, 0)
    #                  0, 0    0, 1    0, 2    
    # 
    #     left (0, -1) 1, 0    1, 1    1, 2 (0, 1) right
    # 
    #                  2, 0    2, 1    2, 2
    #                         (1, 0)
    #                          back
    n = (
         ((-1,0), (0, 1), (1, 0), (0,-1)), # heading North
         ((0, 1), (1, 0), (0,-1), (-1,0)), # heading East
         ((1, 0), (0,-1), (-1,0), (0, 1)), # heading South
         ((0,-1), (-1,0), (0, 1), (1, 0))  # heading West
         )
    
    
    def __init__(self, size=1):
        # erzeuge matrix mit -1 als inhalt
        self.map = np.ones((size, size), int)
        self.map *= -1
        
        self.size = size
        # set startpoint on middle
        self.map[self.size / 2][self.size / 2] = self.start
        
    def update(self, x, y, heading, env):
        self.map[y][x] = heading
        
        if env != None:
            for i in range(4):
                if(env[self.dir_names[i]] > 0):
                    self.map[(y + self.n[heading][i][0]),
                             (x + self.n[heading][i][1])] = env[self.dir_names[i]]
           
           
    def env(self, x, y, heading):
        data = {}
        try:
            data["front"] = self.map[y + self.n[heading][0][0], x + self.n[heading][0][1]]
        except IndexError:
            data["front"] = -1
        try:
            data["right"] = self.map[y + self.n[heading][1][0], x + self.n[heading][1][1]]
        except IndexError:
            data["right"] = -1
        try:
            data["back"] = self.map[y + self.n[heading][2][0], x + self.n[heading][2][1]]
        except IndexError:
            data["back"] = -1
        try:
            data["left"] = self.map[y + self.n[heading][3][0], x + self.n[heading][3][1]]
        except IndexError:
            data["left"] = -1
            
        print data
        return data
        
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
