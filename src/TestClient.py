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
        self.commands = [3, 3, 4]
        self.index = 0

    def getNextCommand(self, sensor_data, bumper):
        """
        cmd = self.commands[self.index]
        self.index += 1
        if self.index == len(self.commands):
            self.index = 0
        return cmd
        """        
        return random.randrange(0, 5, 1)
    
if __name__ == "__main__":
    robot = TestClient()
    robot.getNextCommand()
