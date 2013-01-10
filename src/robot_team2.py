# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:56:09 2012

@author: tim
"""

from BaseRobotClient import Command, BaseRobotClient

from logic import mapping
from dbg import logger

import  GameVisualizer as viz

import time


class robot_team2(BaseRobotClient):
    
    North = 0
    East = 1
    South = 2 
    West = 3
    heading_names = ("North", "East", "South", "West")
    modes = ("rightHand", "cycle", "bomb", "turn", )
    
    map_size = 201
    def __init__(self):
        super(robot_team2, self).__init__()  
        self.index = 0
        self.turn = 1
        self.last_cmd = 0
        self.cmd = -1
        self.batt = 100

        self.rel_pos = [0, 0]
        self.last_pos = None

        self.turned = False
        self.cycle = False
        self.bombed = False
        
        self.bomb_count = 0
        self.bomb_pos = None
        self.bombs = 0
        
        self.cycle_begin = 0
        self.cycle_pos = None
        
        self.time1 = 0
        self.time2 = 0
        
        self.gv = viz.GameVisualizer(None)
        
        #Logging
        self.logger = logger.logger()
        
        # construct map with map_size full of 0
        self.map = mapping.mapping(self.map_size)
        
        # define init heading of robot as north
        self.heading = self.North
        
    def printLog(self, sensor_data, bumper):
        self.logger.info("%4i: %-11s in %f sec c:%s wh:%s" % (self.turn, 
                                                        Command.names[self.cmd],
                                                        self.time2 - self.time1,
                                                        self.cycle,
                                                        self.wasHere()))
        
    def updateBatt(self):
        if(self.cmd == Command.Stay):
            self.batt += 1
        elif(self.cmd == Command.RightTurn):
            self.batt -= 1
        elif(self.cmd == Command.LeftTurn):
            self.batt -= 1
        elif(self.cmd == Command.MoveForward):
            self.batt -= 1
            
    def updatePos(self, bumper, teleported):
        # Update heading of robot
        if(self.cmd == Command.LeftTurn):
            self.heading = (self.heading - 1) % 4
        elif(self.cmd == Command.RightTurn):
            self.heading = (self.heading + 1) % 4
        
        # If moved update position    
        elif (self.moved(bumper, teleported)):
            if(self.heading == self.North):
                self.rel_pos[1] += 1
            elif(self.heading == self.East):
                self.rel_pos[0] += 1
            elif(self.heading == self.South):
                self.rel_pos[1] -= 1
            else:
                self.rel_pos[0] -= 1  
                
    def updateMap(self, sensor_data, compass):
        # Map the enviroment
        self.map.update(self.rel_pos, self.heading+1, sensor_data, compass)
            
    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        self.time1 = time.time()

        print "compass: ", compass
        if teleported:
            a = raw_input()

        self.updatePos(bumper, teleported)          
                    
        if (self.map.get_visited(self.rel_pos) == 0):
            self.cycle = False
            self.bombed = False
            
        if (self.moved(bumper, teleported)):
            self.map.update_visited(self.rel_pos)
        
        self.updateMap(sensor_data, compass)
        
        self.updateBatt()
           
        if (sensor_data != None):
            self.batt = sensor_data["battery"]

            
        #----------------------------------------------------------------------#
        #               SCAN_LOGIC
        #----------------------------------------------------------------------#
            
        # nur scannen wenn wir hier noch nicht waren oder wir irgendwo anstossen
        if (self.cmd != Command.Sense) and (self.map.get_visited(self.rel_pos) < 2) or (bumper):
            self.cmd = Command.Sense
            
            self.time2 = time.time()
            self.printLog(sensor_data, bumper)
            self.turn += 1
            return self.cmd
            
        # wenn wir nicht scannen
        # holen wir uns die nötigen informationen aus der gemappten umgebung
        if sensor_data == None:
            sensor_data = self.map.get_env(self.rel_pos, self.heading + 1)
        
        else:
            # Batterie updaten
            self.batt = sensor_data["battery"]
            
            # Wenn unsere Map schlauer ist, Werte aus dem Map nehmen
            tmp = self.map.get_env(self.rel_pos, self.heading + 1)
            
            if(tmp['front'] == 255):
                sensor_data['front'] = tmp['front']
                
            if(tmp['right'] == 255):
                sensor_data['right'] = tmp['right']
                
            if(tmp['back'] == 255):
                sensor_data['back'] = tmp['back']
                
            if(tmp['left'] == 255):
                sensor_data['left'] = tmp['left']
               
        
        #----------------------------------------------------------------------#
        #               PATH_LOGIC
        #----------------------------------------------------------------------#        
        if (self.batt == 0):
            self.cmd = Command.Stay
        # Auf jeden Fall in das Ziel lenken.
        elif (sensor_data['front'] == 192):
            self.mv()
        elif (sensor_data['right'] == 192):
            self.rt()
        elif (sensor_data['left'] == 192):
            self.lt()
      
        # Kurvenlicht
        elif (self.turned) and not(self.cycle):
            if (self.free("front", sensor_data)):
                self.mv()
            
        elif (self.cycle) and (self.free("back", sensor_data)) and (self.bombs > 0) and (self.map.get_visited(self.rel_pos) >= 3) and not (self.bombed):
            # Bombe legen
            self.db()

            # Bombe liegt hinter uns
            if (self.heading == self.North):
                self.bomb_pos = (self.rel_pos[0], self.rel_pos[1] - 1)
            elif (self.heading == self.East):
                self.bomb_pos = (self.rel_pos[0] - 1, self.rel_pos[1])
            elif (self.heading == self.South):
                self.bomb_pos = (self.rel_pos[0], self.rel_pos[1] + 1)
            elif (self.heading == self.West):
                self.bomb_pos = (self.rel_pos[0] + 1, self.rel_pos[1])
                
            # Update map
            env = {"front" : 0, "left" : 0, "back" : 0, "right" : 0}
            
            self.map.update(self.bomb_pos, self.heading, env, None)
            
            self.bombed = True
            self.bombs -= 1

        
        # Cycle Detect   
        elif (self.wasHere() and self.moved(bumper, teleported) and self.turn != 2 and not self.turned) or (self.cycle):
            # Deadlock -Erkennung und -Behebung bei Rechte-Hand Strategie
   
            self.cycle = True
            
            # Besuche das Feld mit den geringsten Besuchen
            vis = self.map.get_vis_env(self.rel_pos, self.heading + 1)

            minimum = 100
            min_index = 0
            
            if (self.free("front", sensor_data) and vis["front"] < minimum):
                min_index = 0
                minimum = vis["front"]
                
            if (self.free("right", sensor_data) and vis["right"] < minimum):
                min_index = 1
                minimum = vis["right"]
                
            if (self.free("back", sensor_data) and vis["back"] < minimum):
                min_index = 2
                minimum = vis["back"]
                
            if (self.free("left", sensor_data) and vis["left"] < minimum):
                min_index = 3
                minimum = vis["left"]
            

            
            if (min_index == 0):
                self.mv()
                
            elif (min_index == 1):
                self.rt()
                self.turned = True
                
            elif (min_index == 2):
                self.rt()
                
            elif (min_index == 3):
                self.lt()
                self.turned = True
            
            else:
                self.rightHand(sensor_data)
                       
        # Kompass
        elif (self.free("front", sensor_data)) and (self.free("right", sensor_data)) and (self.free("left", sensor_data)): 
            self.compassNav(compass)
                
        # Righthand
        else:
            self.rightHand(sensor_data)
        
        if (self.cmd != Command.Sense) and (self.last_pos != None):
            self.map.update_head(self.last_pos, self.heading + 1)
            
        self.last_pos = self.rel_pos
        
        # Logging
        self.time2 = time.time()
        self.printLog(sensor_data, bumper)
        self.turn += 1
          
        return self.cmd
        
    ##
    # @brief Definiert das Verhalten nach Kompass-Daten
    #
    #
    def compassNav(self, compass):
        if(compass >= 0) and (compass < 3):
            self.mv()
        elif (compass >= 3) and (compass <= 4):
            self.rt()
        elif (compass >= 6) and (compass <= 7):
            self.lt()
        else:
            self.rt()
            self.turned = False
        
    ##
    # @brief Definiert das Verhalten bei rechter-Hand-Regel
    #
    #
    def rightHand(self, env): 
        if self.free("right", env):
            self.rt()

        elif self.free("front", env):
            self.mv()
                
        elif self.free("left", env):
            self.lt()
               
        elif self.free("back", env):
            self.rt()
            self.turned = False
    ##
    # @brief Gibt zurück ob ein Feld frei ist
    #
    #           
    def free(self, direction, env):
        tmp = env[direction]
        if (tmp == 0) or (tmp == 128)  or (tmp == 192):
            return True
        else:
            return False
    
    ##
    # @brief Gibt zurück ob Feld schon besucht wurde
    #
    #       
    def visited(self, pos):
        return self.map.get_visited(pos) > 0
    
    ##
    # @brief Gibt zurück ob aktuelles Feld schon in aktueller Richtung
    #        besucht wurde
    #   
    def wasHere(self):
        return self.map.get_head(self.rel_pos, self.heading + 1)       
        
    ##
    # @brief Gibt zurück ob der Roboter sich im letzten Zug bewegt hat
    #
    #
    def moved(self, bumper, teleported):
        return (self.cmd == Command.MoveForward) and not bumper and (self.batt > 0) and not teleported
    
    ##
    # @brief Roboter eine Linkskurve machen lassen
    #
    #  
    def lt(self):
        self.cmd = Command.LeftTurn
        self.turned = True
        
    ##
    # @brief Roboter eine Rechtskurve machen lassen
    # 
    #
    def rt(self):
        self.cmd = Command.RightTurn
        self.turned = True
    
    ##
    # @brief Einen Schritt vor
    #
    #    
    def mv(self):
        self.cmd = Command.MoveForward
        self.turned = False
        
    ##
    # @brief Roboter Bombe fallen lassen.
    #
    #
    def db(self):
        self.cmd = Command.DropBomb
        
    ##
    # @brief Destructor - Karte zeichnen
    #
    #
    def __del__(self):
        self.map.printFile()
