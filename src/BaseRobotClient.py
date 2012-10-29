# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:24:48 2012

@author: DFKI-MARION-2
"""
class Command:
    LeftTurn, RightTurn,Stay, MoveForward, Sense, DropStone = range(6)
    names = ["LeftTurn", "RightTurn", "Stay", "MoveForward", "Sense", "DropStone"]

class BaseRobotClient(object):
    def __init__(self):
        pass
    
    def getNextCommand(self, sensor_data, bumper):
        print "robot got sensor_data: ", sensor_data
        pass

    def setGoal(self,goal):
        self.goal = goal
    
    def setStartPose(self, pose):
        self.start_pose = pose
    
if __name__ == "__main__":
    robot = BaseRobotClient()
    print Command.LeftTurn
