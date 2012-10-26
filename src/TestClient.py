# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:04:51 2012

@author: DFKI-MARION-2
"""
from BaseRobotClient import *
import random

class TestClient(BaseRobotClient):
    def __init__(self):
        super(TestClient, self).__init__()
    def getNextCommand(self):
        return 4
        #return random.randrange(0, 5, 1)
    
if __name__ == "__main__":
    robot = TestClient()
    robot.getNextCommand()
