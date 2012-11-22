# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:04:51 2012

@author: Stefan Stiene
"""
from BaseRobotClient import *
import random

class TestClient(BaseRobotClient):

    def __init__(self):
        super(TestClient, self).__init__()
        self.commands = [0,0,3, 3,0,3, 4]
        #test sensor_data self.commands = [3,4,0]        
        self.index = 0

    def getNextCommand(self, sensor_data, bumper, compass, teleported):
        #print sensor_data, bumper
        print "compass: ",compass
        if teleported:
            print "ups I was teleported"
        if sensor_data != None:
            print sensor_data
        
        cmd = self.commands[self.index]
        self.index += 1
        if self.index == len(self.commands):
            self.index = 0
        
        return cmd
        """     
        return random.randrange(0, 7, 1)
        """
