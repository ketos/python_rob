# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:24:48 2012

@author: Stefan Stiene
"""
class Command:
    LeftTurn, RightTurn, Stay, MoveForward, Sense, DropStone, DropBomb = range(7)
    names = ["LeftTurn", "RightTurn", "Stay", "MoveForward", "Sense", 
             "DropStone", "DropBomb"]

class BaseRobotClient(object):
    def __init__(self):
        pass
    
    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        """
        @param sensor_data (dict) a dict with the sensor data
        @param bumper (bool) if true last move command hits a wall or robot
        @param compass (int) direction to the goal 0 is front:
          7  0  1
          6  r  2
          5  6  3
        @param teleported (bool) if true the robot was teleported in the 
                                 last round
        """
        print "compass: ",compass
        if teleported:
            print "ups I was teleported"
        print "robot got sensor_data: ", sensor_data
        pass
    
if __name__ == "__main__":
    robot = BaseRobotClient()
    print Command.LeftTurn
