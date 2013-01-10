# -*- coding: utf-8 -*-
'''
Created on 28.11.2012

@author: tim
'''

import numpy as np
from collections import Counter

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
    # for map-coordinates
    n = (
         ((0 ,-1), (1 , 0), (0 , 1), (-1, 0)), # heading North
         ((1 , 0), (0 , 1), (-1, 0), (0 ,-1)), # heading East
         ((0 , 1), (-1, 0), (0 ,-1), (1 , 0)), # heading South
         ((-1, 0), (0 ,-1), (1 , 0), (0 , 1))  # heading West
        )
    
    # same for real-coordinates    
    m = (
         ((0 , 1), (1 , 0), (0 ,-1), (-1, 0)), # heading North
         ((1 , 0), (0 ,-1), (-1, 0), (0 , 1)), # heading East
         ((0 ,-1), (-1, 0), (0 , 1), (1 , 0)), # heading South
         ((-1, 0), (0 , 1), (1 , 0), (0 ,-1))  # heading West
        )
    
    ##
    # @brief Konstruktor
    #
    #
    def __init__(self, size=1):
        # erzeuge matrix mit -1 als inhalt
        self.map = self.create(size)

        self.size = size       
        self.pos = [self.size / 2, self.size / 2]
        
    ##
    # @brief Erzeugt neue Karte mit gegebener Grösse
    #
    #    
    def create(self, size):
        dt = np.dtype([ ('visited', int),
                        ('h_north', bool),
                        ('h_east', bool),
                        ('h_south', bool),
                        ('h_west', bool),
                        ('compass', int),
                        ('enviro',  int)])
        return np.zeros((size, size), dt)
    
    ##
    # @brief schriebt an die Stelle pos den Wert value an das Attribute
    #
    #    
    def write(self, pos, attribute, value):
        self.pos = self.toMapPos(pos)
        self.map[self.pos[1]][self.pos[0]][attribute] = value
        
    ##
    # @brief trägt Kompass und Umgebung des Roboters in Karte ein
    #
    #
    def update(self, pos, heading, env, compass):
        self.pos = self.toMapPos(pos)
        
        # die compass daten mussen angepasst werden
        # mit dem aktuellen heading
        if (compass != None):
            tcompass = compass + (heading - 1) * 2
        
            if tcompass < 0:
                tcompass += 8
            if tcompass > 7:
                tcompass -= 8
        
            self.map[self.pos[1]][self.pos[0]]['compass'] = (tcompass * 45)
        
        if env != None:
            for i in range(4):         
                #--------------------------------------------------------------#
                #       UMGEBUNG_SPEICHERN
                #--------------------------------------------------------------#
            
                x = (self.pos[0] + self.n[heading - 1][i][0])
                y = (self.pos[1] + self.n[heading - 1][i][1])
                
                tmp = self.map[y, x]['enviro']
                
                # keine Roboter mappen
                if (env[self.dir_names[i]] < 150 or env[self.dir_names[i]] > 161):
                    self.map[y, x]['enviro'] = env[self.dir_names[i]]

                
                #--------------------------------------------------------------#
                #       SACKGASSEN_LOGIC
                #--------------------------------------------------------------#
                
                if env[self.dir_names[i]] == 255 and tmp != 255:
                    # Wenn wir eine Mauer gesetzt haben
                    
                    # Position des gestzen Mauerstücks (in real Koordinaten)
                    x = (pos[0] + self.m[heading - 1][i][0])
                    y = (pos[1] + self.m[heading - 1][i][1])
                      
                    self.fill_up((x,y), heading, pos)  
                    
    ##
    # @brief Findet Sackgassen und füllt diese auf
    #
    #
    def fill_up(self, pos, heading, robo_pos):
        # Berrechne Nachbarn der gesetzten Mauer
        for b in range(4):
            tx = pos[0] + self.m[heading - 1][b][0]
            ty = pos[1] + self.m[heading - 1][b][1]
            
            wall_env = self.get_env((tx, ty), 0)            
            count = Counter(wall_env.values())
              
            if count[255] >= 3 and self.get_field((tx,ty)) != 255 and ([tx,ty] != robo_pos):
                # Bedingung erfüllt, fülle auf mit Mauer
                self.write((tx, ty),'enviro', 255)
                # Rekursion        
                self.fill_up((tx,ty), heading, robo_pos)
                            
    ##
    # @brief Setzt das Feld an Stelle pos als besucht
    #
    #
    def update_visited(self, pos):
        self.pos = self.toMapPos(pos)
        self.write(pos, 'visited', self.map[self.pos[1]][self.pos[0]]['visited'] + 1)
        
    ##
    # @brief Setzt das Feld an der Stelle pos mit dem gegebenen heading
    #
    #
    def update_head(self, pos, heading):
        self.pos = self.toMapPos(pos)
        
        if (heading == self.north):
            self.write(pos, 'h_north', True)
        elif (heading == self.east):
            self.write(pos, 'h_east', True)
        elif (heading == self.south):
            self.write(pos, 'h_south', True)
        elif (heading == self.west):
            self.write(pos, 'h_west', True)
                            
    ##
    # @brief gibt die Umgebung an der Stelle pos zurück
    #
    #
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
        
    ##
    # @brief gibt die Zahl der Besuche der Umgebung um pos zurück
    #
    #
    def get_vis_env(self, pos, heading):
        data = {}
        tpos = self.toMapPos(pos)
        try:
            data["front"] = self.map[tpos[1] + self.n[heading-1][0][1], tpos[0] + self.n[heading-1][0][0]]['visited']
        except IndexError:
            data["front"] = -1
            
        try:    
            data["right"] = self.map[tpos[1] + self.n[heading-1][1][1], tpos[0] + self.n[heading-1][1][0]]['visited']
        except IndexError:
            data["right"] = -1
            
        try:
            data["back"] = self.map[tpos[1] + self.n[heading-1][2][1], tpos[0] + self.n[heading-1][2][0]]['visited']
        except IndexError:
            data["back"] = -1
            
        try:
            data["left"] = self.map[tpos[1] + self.n[heading-1][3][1], tpos[0] + self.n[heading-1][3][0]]['visited']
        except IndexError:
            data["left"] = -1

        return data
        
    ##
    # @brief Rechnet real-koordinaten in map-koordinaten um
    #
    #
    def toMapPos(self, pos):
        # Update Map coords
        data = [0, 0]
        data[0] = self.size / 2 + pos[0] 
        data[1] = self.size / 2 - pos[1]
        
        return data
        
    ##
    # @brief Gibt den Umgebungswert an der Stelle pos zurück
    #
    #
    def get_field(self, pos):
        tpos = self.toMapPos(pos)
        return self.map[tpos[1], tpos[0]]['enviro']
        
    ##
    # @brief Gibt das heading an der Stelle pos zurück
    #
    #
    def get_head(self, pos, heading):
        tpos = self.toMapPos(pos)
        
        if (heading == self.north):
            return self.map[tpos[1], tpos[0]]['h_north']
        elif (heading == self.east):
            return self.map[tpos[1], tpos[0]]['h_east']
        elif (heading == self.south):
            return self.map[tpos[1], tpos[0]]['h_south']
        elif (heading == self.west):
            return self.map[tpos[1], tpos[0]]['h_west']
        
    ##
    # @brief Gibt zurück ob das Feld pos besucht wurde
    #
    #
    def get_visited(self, pos):
        tpos = self.toMapPos(pos)
        return self.map[tpos[1], tpos[0]]['visited']
            
    ##
    # @brief Schreibt die Karte in eine Datei (zum anschauen)
    #
    #
    def printFile(self):
        mapFile = open("map.txt", "w")
        for i in range(self.size):
            for t in range(self.size):
                mapFile.write("%s " % (self.index[self.map[i][t]['enviro']]))
                
                #mapFile.write("%3i" % (self.map[i][t]['compass']))
                
                #mapFile.write("%3i" % (self.map[i][t]['visited']))
                
                    
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
