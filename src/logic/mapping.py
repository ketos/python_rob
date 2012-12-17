# -*- coding: utf-8 -*-
'''
Created on 28.11.2012

@author: tim
'''

import numpy as np

class mapping(object):
    void = -1
    free = 0
    start = 20 
    target = 192
    wall = 255
    portal = 129
    loader = 128 

    north = 1
    east = 2
    south = 3
    west = 4
    
    dir_names = {
                    0 : "front", 1 : "right", 2 : "back", 3 : "left"
                }
    
    index = {void : "-", free : " ", start : "S",
             target: "X", wall : "#", portal : "O",
             loader : "E", north : "^", east : ">" ,
             south : "v" , west : "<"
            }
            
    # Relative Coordinates of Front, Right, Back, Left
    # Example (North, x and y inverted):
    #                         front
    #                        (-1, 0)
    #                  0, 0    0, 1    0, 2    
    # 
    #     left (0, -1) 1, 0    1, 1    1, 2 (0, 1) right
    # 
    #                  2, 0    2, 1    2, 2
    #                         (1, 0)
    #                          back
    n = (
         ((0,-1), (1, 0), (0, 1), (-1,0)), # heading North
         ((1, 0), (0, 1), (-1,0), (0,-1)), # heading East
         ((0, 1), (-1,0), (0,-1), (1, 0)), # heading South
         ((-1,0), (0,-1), (1, 0), (0, 1))  # heading West
         )
    
    
    def __init__(self, size=1):
        # erzeuge matrix mit -1 als inhalt
        self.map = np.ones((size, size), int)
        self.map *= -1
        
        self.size = size
        # set startpoint on middle
        self.map[self.size / 2][self.size / 2] = self.start
        
        self.pos = [self.size / 2, self.size / 2]
        
    def update(self, pos, heading, env): 
        self.pos = self.toMapPos(pos)
        #print "add ", heading, " at ", self.pos, " to map"
        #print "was: ", self.map[self.pos[1], self.pos[0]]
        self.map[self.pos[1]][self.pos[0]] = heading
        
        if env != None:
            #print self.n[heading-1]
            for i in range(4):
                tmp = self.map[(self.pos[1] + self.n[heading-1][i][1]),
                             (self.pos[0] + self.n[heading-1][i][0])]
                #print "i: ",i, " add ", env[self.dir_names[i]], " (", self.dir_names[i], ") at ", self.pos[0] + self.n[heading-1][i][0], ",", self.pos[1] + self.n[heading-1][i][1],self.n[heading-1][i], "to map"
                #print "was: ", tmp
                if tmp == -1:
                    self.map[(self.pos[1] + self.n[heading-1][i][1]),
                             (self.pos[0] + self.n[heading-1][i][0])] = env[self.dir_names[i]]
           
    
    def envAt(self, pos, heading):
        data = {}
        tpos = self.toMapPos(pos)
        #print self.n[heading-1][0], "heading:", heading
        
        data["front"] = self.map[tpos[1] + self.n[heading-1][0][1], tpos[0] + self.n[heading-1][0][0]]

        data["right"] = self.map[tpos[1] + self.n[heading-1][1][1], tpos[0] + self.n[heading-1][1][0]]

        data["back"] = self.map[tpos[1] + self.n[heading-1][2][1], tpos[0] + self.n[heading-1][2][0]]

        data["left"] = self.map[tpos[1] + self.n[heading-1][3][1], tpos[0] + self.n[heading-1][3][0]]


        return data
        
    def toMapPos(self, pos):
        # Update Map coords
        data = [0, 0]
        data[0] = self.size / 2 + pos[0] 
        data[1] = self.size / 2 - pos[1]
        
        return data
        
    def look(self, pos):
        tpos = self.toMapPos(pos)
        return self.map[tpos[1], tpos[0]]
        
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
