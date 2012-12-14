# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:56:09 2012

@author: tim
"""

from BaseRobotClient import Command, BaseRobotClient

from logic import mapping
from dbg import logger

import time


class robot_team2(BaseRobotClient):
    
    North, East, South, West = range(4)
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
        
        #Logging
        self.logger = logger.logger()
        
        # construct map with map_size full of 0
        self.map = mapping.mapping(self.map_size)
        
        # define init heading of robot as north
        self.heading = self.North
        
    def printLog(self, sensor_data, bumper):
        self.logger.info("%4i: %-11s in %f sec c:%s" % (self.turn, Command.names[self.cmd], self.time2 - self.time1, self.cycle))
        
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
        elif(self.cmd == Command.MoveForward) and (bumper == False) and (self.batt > 0):
            if(self.heading == self.North):
                self.rel_pos[1] += 1
            elif(self.heading == self.East):
                self.rel_pos[0] += 1
            elif(self.heading == self.South):
                self.rel_pos[1] -= 1
            else:
                self.rel_pos[0] -= 1
                
                
    def updateMap(self, sensor_data):
        # Map the enviroment
        
        # set field as visited with heading
        self.map.update(self.rel_pos, self.heading, sensor_data)
            


    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        self.time1 = time.time()

        print "compass: ",compass
        if teleported:
            print "ups I was teleported"

        self.updatePos(bumper)
               
        if (sensor_data != None):
            self.batt = sensor_data["battery"]
            
        #----------------------------------------------------------------------#
        #               SCAN_LOGIC
        #----------------------------------------------------------------------#
            
        # nur alle zwei runden scannen und wenn das aktuelle
        # feld noch nicht besucht wurde
        if (self.turn % 2) and not(self.wasHere()):
            self.cmd = Command.Sense
            self.turn += 1
            return self.cmd
        # wenn wir nicht jeden zweiten zug scannen
        # holen wir uns die nötigen informationen aus der gemappten umgebung
        elif (self.cycle) or (self.wasHere()):
            sensor_data = self.map.envAt(self.rel_pos, self.heading)
        
        #----------------------------------------------------------------------#
        #               PATH_LOGIC
        #----------------------------------------------------------------------#
        
        if (self.turned) and not(self.cycle):
            if (sensor_data["front"] < 255):
                self.mv()
    
        elif (self.wasHere() and self.turn != 2 and not self.turned) or (self.cycle):
            # Deadlock -Erkennung und -Behebung bei Rechte-Hand Strategie
            self.cycle = True
            if (sensor_data["left"] < 255):
                # Wir können dem Deadlock durch eine Linkskurve entkommen
                self.lt()
                self.cycle = False
            elif (sensor_data["front"] < 255) and (sensor_data["right"] < 255):
                # Wir können dem Deadlock Weiterfahren entkommen,
                # auch wenn wir rechts abbiegen müssten.
                self.mv()
                self.cycle = False
            else:
                self.rightHand(sensor_data)

        else:
            self.rightHand(sensor_data)        
         

        self.updateMap(sensor_data)
          
        self.time2 = time.time()
        self.printLog(sensor_data, bumper)
        self.turn += 1
          
        return self.cmd
    
    def rightHand(self, env):
        if env["right"] < 255:
            self.rt()

        elif env["front"] < 255:
            self.mv()
                
        elif env["left"] < 255:
            self.lt()
                
        elif env["back"] < 255:
            self.rt()
            self.turned = False
            
    def wasHere(self):
        return self.map.look(self.rel_pos) == self.heading
        
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
        
        
        
        
        
        
        
