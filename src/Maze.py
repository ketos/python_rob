# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:24:15 2012

@author: DFKI-MARION-2
"""

import sys
    
class Maze(object):
    def __init__(self, filename):
        self._grid = Maze._loadGrid(filename)
    
    def getSensorData(self, Pose):       # pose as (x,y,theta) tuple
        pass
    
    def checkNewPosition(self, position):   # test if a new position is valid
        pass

    def setStone(self, pose):
        pass
    
    def getGrid(self):
        return self._grid
    
    @staticmethod
    def _loadGrid(filename):
        items = []
        for line in open(filename, 'r'):
            comment_index = line.find('#')
            if comment_index != -1:
                line = line[:comment_index]
        
            items.extend(line.split())
        
        if items[0] != 'P2':
            print "Error: PGM file must start with 'P2'"
            sys.exit(-1)
        
        width = int(items[1])
        height = int(items[2])
        
        # items[3]: max value of "colors"; ignore
        
        items = items[4:]
        
        grid = [[int(items[j * width + i]) for i in range(width)] for j in range(height)]
            
        return grid    
    
