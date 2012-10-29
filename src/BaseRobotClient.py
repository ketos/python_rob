# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:24:48 2012

@author: DFKI-MARION-2
"""
class Command:
    LeftTurn, RightTurn,Stay, MoveForward, Sense, DropStone, DropBomb = range(7)
    names = ["LeftTurn", "RightTurn", "Stay", "MoveForward", "Sense", 
             "DropStone", "DropBomb"]

class BaseRobotClient(object):
    def __init__(self):
        pass
    
    def getNextCommand(self, sensor_data, bumper):
        print "robot got sensor_data: ", sensor_data
        pass

    def setGoal(self,goal):
        self.goal = goal
    
    def setStartPose(self, position, orientation):
        self._position = position
        self._orientation = orientation
    
if __name__ == "__main__":
    robot = BaseRobotClient()
    print Command.LeftTurn
