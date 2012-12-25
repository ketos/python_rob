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
            
    def updatePos(self, bumper):
        # Update heading of robot
        if(self.cmd == Command.LeftTurn):
            self.heading = (self.heading - 1) % 4
        elif(self.cmd == Command.RightTurn):
            self.heading = (self.heading + 1) % 4
        
        # If moved update position    
        elif (self.moved(bumper)):
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
        
        # set field as visited with heading
        self.map.update(self.rel_pos, self.heading+1, sensor_data, compass)
            


    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        self.time1 = time.time()

        print "compass: ",compass
        if teleported:
            print "ups I was teleported"
            # create new submap
            #self.map.newSubmap()

        self.updatePos(bumper)          
               
        if (sensor_data != None):
            self.batt = sensor_data["battery"]
            self.updateMap(sensor_data, compass)
            
        #----------------------------------------------------------------------#
        #               SCAN_LOGIC
        #----------------------------------------------------------------------#
            
        # nur alle zwei runden scannen und wenn das aktuelle
        # feld noch nicht besucht wurde
        if (self.turn % 2) and not(self.wasHere()):
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
            # print sensor_data
            # print tmp
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
                
        # Debug ------
        # Print Enviroment
        '''
        print "   %s" % (self.gv.FORMATTER[sensor_data["front"]]) 
        print " %s ^ %s" % (self.gv.FORMATTER[sensor_data["left"]],self.gv.FORMATTER[sensor_data["right"]])
        print "   %s" % (self.gv.FORMATTER[sensor_data["back"]])
        #a = raw_input()
        '''
        #----------------------------------------------------------------------#
        #               PATH_LOGIC
        #----------------------------------------------------------------------#
        
        if (self.turned) and not(self.cycle):
            if (self.free("front", sensor_data)):
                self.mv()
    
        elif (self.wasHere() and self.moved(bumper) and self.turn != 2 and not self.turned) or (self.cycle):
            # Deadlock -Erkennung und -Behebung bei Rechte-Hand Strategie
            self.cycle = True
            if (self.free("left", sensor_data)):
                # Wir können dem Deadlock durch eine Linkskurve entkommen
                self.lt()
                self.cycle = False
            elif (self.free("front", sensor_data)) and (self.free("right", sensor_data)):
                # Wir können dem Deadlock Weiterfahren entkommen,
                # auch wenn wir rechts abbiegen müssten.
                self.mv()
                self.cycle = False
            else:
                self.rightHand(sensor_data)

        else:
            self.rightHand(sensor_data)        
          
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
        if (env[direction] == -1) or (env[direction] == 255):
            return False
        else:
            return True
        
    def wasHere(self):
        return self.map.get_head(self.rel_pos) == self.heading + 1       
        
    def moved(self, bumper):
        return (self.cmd == Command.MoveForward) and not bumper and (self.batt > 0)
        
    def lt(self):
        self.cmd = Command.LeftTurn
        self.turned = True
        
    def rt(self):
        self.cmd = Command.RightTurn
        self.turned = True
        
    def mv(self):
        self.cmd = Command.MoveForward
        self.turned = False
    
    def __del__(self):
        self.map.printFile()      
