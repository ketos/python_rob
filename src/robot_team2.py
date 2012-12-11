# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:56:09 2012
möp
@author: tim
"""

from BaseRobotClient import Command, BaseRobotClient

from logic import mapping
from dbg import logger

import time


class robot_team2(BaseRobotClient):
    
    North, East, South, West = range(4)
    heading_names = ("North", "East", "South", "West")
    look_names = ("front", "right", "back", "left")
    
    map_size = 201
    
    # Constants for the Mapping Chars 
    visited = 2
    startpoint = 1
    void = -1
    
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

    def __init__(self):
        super(robot_team2, self).__init__()  
        self.index = 0
        self.turn = 1
        self.cmd = -1
        self.batt = 100
        self.sens_tmp = None
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
        self.logger.info("%4i: %-11s in %f sec" % (self.turn, Command.names[self.cmd], self.time2 - self.time1))
        
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
        half_size = (self.map_size/2)
        
        x = half_size + self.rel_pos[0] 
        y = half_size - self.rel_pos[1] 
        
        # set field as visited
        self.map.update(x, y, self.heading + 100)
        
        if sensor_data != None:
            # For each look direction (front, right, back, left)
            # save enviroment in map
            for i in range(4):
                if(sensor_data[self.look_names[i]] > 0):
                    self.map.update((x + self.n[self.heading][i][1]),
                                    (y + self.n[self.heading][i][0]),
                                     sensor_data[self.look_names[i]])


    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        self.time1 = time.time()

        print "compass: ",compass
        if teleported:
            print "ups I was teleported"

        self.updatePos(bumper)

        #-------------------------------------------------------------------------#          

        # Scan jeden zweiten schritt
        if self.turn % 2:
            self.cmd = Command.Sense

        elif (self.turned) and self.cycle == False:
            if (sensor_data["front"] < 255):
                self.cmd = Command.MoveForward
                self.turned = False
    
        elif (self.map.map[(self.map_size/2) + self.rel_pos[1]][(self.map_size/2) - self.rel_pos[0]] == self.heading + 100 and self.turn != 2) or self.cycle == True:
            self.cycle = True
            if (sensor_data["left"] < 255):
                self.cmd = Command.LeftTurn
                self.turned = True
                self.cycle = False
            else:
                self.rightHand(sensor_data)

        else:
            # If our Batt-Value is wrong correct it.
            self.batt = sensor_data["battery"]
    
            self.rightHand(sensor_data)
        
            self.sens_tmp = sensor_data
        
        
        # Map enviroment
        self.updateMap(sensor_data)  
          
        self.time2 = time.time()
        self.printLog(sensor_data, bumper)
        self.turn += 1
          
        return self.cmd
    
    def rightHand(self, sensor_data):
        if (sensor_data["right"] < 255) and (sensor_data["left"] < 255):
            #More Possibilitis to turn
            self.cmd = Command.RightTurn
            self.turned = True
                
        elif sensor_data["right"] < 255:
            self.cmd = Command.RightTurn
            self.turned = True

        elif sensor_data["front"] < 255:
            self.cmd = Command.MoveForward
            self.turned = False
                
        elif sensor_data["left"] < 255:
            self.cmd = Command.LeftTurn
            self.turned = True
                
        elif sensor_data["back"] < 255:
            self.cmd = Command.RightTurn
            self.turned = False
    
    def __del__(self):
        self.map.printFile()
        
        
        
        
        
        
        
