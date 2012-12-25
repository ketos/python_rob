# -*- coding: utf-8 -*-
'''
Created on 28.11.2012

@author: tim
'''

import numpy as np
from collections import Counter
import math

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
             target : "X", wall : "#", portal : "O",
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
         ((0 ,-1), (1 , 0), (0 , 1), (-1, 0)), # heading North
         ((1 , 0), (0 , 1), (-1, 0), (0 ,-1)), # heading East
         ((0 , 1), (-1, 0), (0 ,-1), (1 , 0)), # heading South
         ((-1, 0), (0 ,-1), (1 , 0), (0 , 1))  # heading West
        )
    
    
    def __init__(self, size=1):
        # erzeuge matrix mit -1 als inhalt
        self.map = self.create(size)

        self.size = size       
        self.pos = [self.size / 2, self.size / 2]
        
        # Liste der Unterkarten die für die Sprünge notwendig sind
        self.submaps = []
        
    def create(self, size):
        dt = np.dtype([ ('visited', np.bool),
                        ('heading', int),
                        ('compass', int),
                        ('enviro',  int)])
        return np.zeros((size, size), dt)
        
    def update(self, pos, heading, env, compass):           
        
        self.pos = self.toMapPos(pos)
        # print "add ", heading, " at ", self.pos, " to map"
        # print "was: ", self.map[self.pos[1], self.pos[0]]
        self.map[self.pos[1]][self.pos[0]]['heading'] = heading
        
        # die compass daten mussen angepasst werden
        # mit dem aktuellen heading
        
        tcompass = compass + (heading - 1) * 2
        
        if tcompass < 0:
            tcompass += 8
        if tcompass > 7:
            tcompass -= 8
        
        self.map[self.pos[1]][self.pos[0]]['compass'] = (tcompass * 45)
        
        if env != None:
            # print self.n[heading-1]
            # print "Iam at ",pos[0],", ",pos[1]
            for i in range(4):         
                #--------------------------------------------------------------#
                #       UMGEBUNG_SPEICHERN
                #--------------------------------------------------------------#
            
                x = (self.pos[0] + self.n[heading - 1][i][0])
                y = (self.pos[1] + self.n[heading - 1][i][1])
                
                tmp = self.map[y, x]['enviro']
                # print "i: ",i, " add ", env[self.dir_names[i]], " (", self.dir_names[i], ") at ", self.pos[0] + self.n[heading-1][i][0], ",", self.pos[1] + self.n[heading-1][i][1],self.n[heading-1][i], "to map"
                if tmp != 255:
                    self.map[y, x]['enviro'] = env[self.dir_names[i]]
                    # print "Set ",env[self.dir_names[i]]," at ",pos[0] + self.n[heading-1][i][0],", ",pos[1] + self.n[heading-1][i][1]
                
                #--------------------------------------------------------------#
                #       SACKGASSEN_LOGIC
                #--------------------------------------------------------------#
                
                if env[self.dir_names[i]] == 255 and tmp != 255:
                    # Wenn wir eine Mauer gesetzt haben
                    
                    # Position des gestzen Mauerstücks (in real Koordinaten)
                    x = (pos[0] + self.n[heading - 1][i][0])
                    y = (pos[1] + self.n[heading - 1][i][1])
                        
                    for b in range(4):
                        tx = x + self.n[heading - 1][b][0]
                        ty = y + self.n[heading - 1][b][1]
                        # print "Look at ",tx,", ",ty
                        wall_env = self.get_env((tx, ty), i)
                        # print wall_env
                        
                        count = Counter(wall_env.values())
                        
                        if count[255] >= 3 and self.map[ty, tx]['enviro'] != 255:
                            # Bedingung erfüllt, fülle auf mit Mauer
                            # print "Füllung bei ",tx,",",ty
                            # a = raw_input()
                            self.map[ty, tx]['enviro'] = 255
                            
    def get_env(self, pos, heading):
        data = {}
        tpos = self.toMapPos(pos)
        # print self.n[heading-1][0], "heading:", heading
        try:
            data["front"] = self.map[tpos[1] + self.n[heading-1][0][1], tpos[0] + self.n[heading-1][0][0]]['enviro']
        except IndexError:
            data["front"] = -1
            
        try:    
            data["right"] = self.map[tpos[1] + self.n[heading-1][1][1], tpos[0] + self.n[heading-1][1][0]]['enviro']
        except IndexError:
            data["right"] = -1
            
        try:
            data["back"] = self.map[tpos[1] + self.n[heading-1][2][1], tpos[0] + self.n[heading-1][2][0]]['enviro']
        except IndexError:
            data["back"] = -1
            
        try:
            data["left"] = self.map[tpos[1] + self.n[heading-1][3][1], tpos[0] + self.n[heading-1][3][0]]['enviro']
        except IndexError:
            data["left"] = -1

        return data
        
    def toMapPos(self, pos):
        # Update Map coords
        data = [0, 0]
        data[0] = self.size / 2 + pos[0] 
        data[1] = self.size / 2 - pos[1]
        
        return data
        
    def get_field(self, pos):
        tpos = self.toMapPos(pos)
        return self.map[tpos[1], tpos[0]]['enviro']
        
    def get_head(self, pos):
        tpos = self.toMapPos(pos)
        return self.map[tpos[1], tpos[0]]['heading']
        
        
    def newSubmap():
        self.submaps.append(self.map)
        self.map = self.create(self.size)
        
    def fillTrap(self, pos):
        env = self.envAt(pos, self.north)
        print env
        
    def printFile(self):
        mapFile = open("map.txt", "w")
        for i in range(self.size):
            for t in range(self.size):
                #mapFile.write("%s " % (self.index[self.map[i][t]['enviro']]))
                
                mapFile.write("%3i" % (self.map[i][t]['compass']))
                
                    
                if t == self.size - 1:
                    mapFile.write("\t%i\n" % (i + 1))
                 
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
