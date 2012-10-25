# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:24:48 2012

@author: DFKI-MARION-2
"""
class Command:
    LeftTurn, RightTurn, MoveForward, Sense, DropStone = range(5)

class BaseRobotClient(object):
    def __init__(self):
        pass
    
    def getNextCommand(self):
        pass
    
    def setSensorDate(self, data):
        print "robot get data: ", data
        
    def setBumper(self):
        pass
    
if __name__ == "__main__":
    robot = BaseRobotClient()
    print Command.LeftTurn
