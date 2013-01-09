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
        self.cmd = -1
        self.batt = 100

        self.rel_pos = [0, 0]

        self.turned = False
        self.cycle = False
        self.bombed = False
        
        self.bomb_count = 0
        self.bomb_pos = None
        self.bombs = 1
        
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
                
            self.map.update_visited(self.rel_pos)
                
                
    def updateMap(self, sensor_data, compass):
        # Map the enviroment
        self.map.update(self.rel_pos, self.heading+1, sensor_data, compass)
            
    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        self.time1 = time.time()

        print "compass: ", compass
        if teleported:
            print "ups I was teleported"
            self.map = None
            self.map = mapping.mapping(self.map_size)
            self.rel_pos = [0, 0]
            
            self.map.write(self.rel_pos, 'enviro', 255)
            
            a = raw_input()

        self.updatePos(bumper, teleported)          
        
        self.updateMap(sensor_data, compass)
           
        if (sensor_data != None):
            self.batt = sensor_data["battery"]
            
            
        #----------------------------------------------------------------------#
        #               SCAN_LOGIC
        #----------------------------------------------------------------------#
            
        # nur alle zwei runden scannen und wenn das aktuelle
        # feld noch nicht besucht wurde
        if (self.cmd != Command.Sense) and (self.map.get_visited(self.rel_pos) < 2):
                
            self.cmd = Command.Sense
            
            self.time2 = time.time()
            self.printLog(sensor_data, bumper)
            self.turn += 1
            return self.cmd
            
        # wenn wir nicht jeden zweiten zug scannen
        # holen wir uns die nötigen informationen aus der gemappten umgebung
        if sensor_data == None:
            sensor_data = self.map.get_env(self.rel_pos, self.heading + 1)
        
        else:
            tmp = self.map.get_env(self.rel_pos, self.heading + 1)

            if(sensor_data['front'] != tmp['front']):
                print "front correction"
                sensor_data['front'] = tmp['front']
                
            if(sensor_data['right'] != tmp['right']):
                print "right correction"
                sensor_data['right'] = tmp['right']
                
            if(sensor_data['back'] != tmp['back']):
                print "back correction"
                sensor_data['back'] = tmp['back']
                
            if(sensor_data['left'] != tmp['left']):
                print "left correction"
                sensor_data['left'] = tmp['left']
        
        '''
        # Debug ------
        # Print Enviroment
        print "iam at ", self.rel_pos
        print "   %s" % (self.gv.FORMATTER[sensor_data["front"]]) 
        print " %s ^ %s" % (self.gv.FORMATTER[sensor_data["left"]],self.gv.FORMATTER[sensor_data["right"]])
        print "   %s" % (self.gv.FORMATTER[sensor_data["back"]])
        '''
        #a = raw_input()
               
        
        #----------------------------------------------------------------------#
        #               PATH_LOGIC
        #----------------------------------------------------------------------#
        
        # Auf jeden Fall in das Ziel lenken.
        if (sensor_data['front'] == 192):
            self.mv()
        elif (sensor_data['right'] == 192):
            self.rt()
        elif (sensor_data['left'] == 192):
            self.lt()
        
      
        # Kurvenlicht
        elif (self.turned) and not(self.cycle):
            if (self.free("front", sensor_data)):
                self.mv()
        
        # Bombe / Deadlock
        elif (self.cycle) and (self.map.get_visited(self.rel_pos) >= 3) and not (self.bombed) and (self.bombs > 0):
            self.bombed = True
            self.rightHand(sensor_data)
            
        elif (self.bombed) and (self.free("back", sensor_data)):
            # Bombe legen
            self.db()
            a = raw_input()
            # Bombe liegt hinter uns
            if (self.heading == self.North):
                self.bomb_pos = (self.rel_pos[0], self.rel_pos[1] - 1)
            elif (self.heading == self.East):
                self.bomb_pos = (self.rel_pos[0] -1 , self.rel_pos[1])
            elif (self.heading == self.South):
                self.bomb_pos = (self.rel_pos[0], self.rel_pos[1] + 1)
            elif (self.heading == self.West):
                self.bomb_pos = (self.rel_pos[0] + 1, self.rel_pos[1])
                
            # Update map
            env = {"front" : 0, "left" : 0, "back" : 0, "right" : 0}
            
            self.map.update(self.bomb_pos, self.heading, env, None)
            
            self.bombed = False
            self.bombs -= 1
            
            self.bomb_count = 0
            self.cycle = False
        
        # Cycle Detect   
        elif (self.wasHere() and self.moved(bumper, teleported) and self.turn != 2 and not self.turned) or (self.cycle):
            # Deadlock -Erkennung und -Behebung bei Rechte-Hand Strategie
            a = raw_input()
            if (not self.cycle):
                # Erster Punkt des cyclen
                self.cycle_pos = self.rel_pos
                self.cycle_begin = self.turn
                
            self.cycle = True
            
            if (self.free("front", sensor_data)) and (self.free("right", sensor_data)):
                # Wir können dem Deadlock Weiterfahren entkommen,
                # auch wenn wir rechts abbiegen müssten.
                self.mv()
                self.cycle = False
            elif (self.free("left", sensor_data)):
                # Wir können dem Deadlock durch eine Linkskurve entkommen
                self.lt()
                self.cycle = False
            else:
                self.rightHand(sensor_data)
        # Righthand
        else:
            self.rightHand(sensor_data)
          
        # Logging
        self.time2 = time.time()
        self.printLog(sensor_data, bumper)
        self.turn += 1
          
        return self.cmd
    
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
                
    def free(self, direction, env):
        tmp = env[direction]
        if (tmp == 0) or (tmp == 128)  or (tmp == 192):
            return True
        else:
            return False
    def visited(self, pos):
        return self.map.get_visited(pos) > 0
        
    def wasHere(self):
        return self.map.get_head(self.rel_pos, self.heading + 1)       
        
    def moved(self, bumper, teleported):
        return (self.cmd == Command.MoveForward) and not bumper and (self.batt > 0) and not teleported
        
    def lt(self):
        self.cmd = Command.LeftTurn
        self.turned = True
        
    def rt(self):
        self.cmd = Command.RightTurn
        self.turned = True
        
    def mv(self):
        self.cmd = Command.MoveForward
        self.turned = False
        
    def db(self):
        self.cmd = Command.DropBomb
        
    def __del__(self):
        self.map.printFile()
