# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:24:15 2012

@author: DFKI-MARION-2
"""

import sys
from copy import deepcopy
    
class Maze(object):
    start_index = 0
    def __init__(self, filename):
        self._grid = Maze._loadGrid(filename)
        self._start_positions = []
        self._stones = []
        self.robot_states = {}
        for y, row in enumerate(self._grid):
            for x, value in enumerate(row):
                if value >= 150 and value <= 153:
                    self._start_positions += [[150, x,y,value%4]]
                    self._grid[y][x] = 0
                if value >= 154 and value <= 157:
                    self._start_positions += [[154, x,y,value%4]]
                    self._grid[y][x] = 0
                if value >= 158 and value <= 161:
                    self._start_positions += [[158, x,y,value%4]]
                    self._grid[y][x] = 0                
                    
        print self._start_positions
    
    def getSensorData(self, pose):       # pose as (x,y,theta) tuple
        data = {}
        
        #TODO orientierung berücksichtigen!
        if pose[2] == 0:
            data[(0,1)] = self._grid[pose[0] + 1][pose[1]]
            data[(0,-1)] = self._grid[pose[0] - 1][pose[1]]
            data[(1,0)] = self._grid[pose[0]][pose[1]+1]
            data[(-1,0)] = self._grid[pose[0]][pose[1]-1]
        elif pose[2] == 2:
            data[(0,1)] = self._grid[pose[0] - 1][pose[1]]
            data[(0,-1)] = self._grid[pose[0] + 1][pose[1]]
            data[(1,0)] = self._grid[pose[0]][pose[1]-1]
            data[(-1,0)] = self._grid[pose[0]][pose[1]+1]
        elif pose[2] == 1:
            data[(0,1)] = self._grid[pose[0] ][pose[1]+ 1]
            data[(0,-1)] = self._grid[pose[0] ][pose[1]- 1]
            data[(1,0)] = self._grid[pose[0]+1][pose[1]]
            data[(-1,0)] = self._grid[pose[0]-1][pose[1]]
        elif pose[2] == 3:
            data[(0,1)] = self._grid[pose[0] ][pose[1] - 1]
            data[(0,-1)] = self._grid[pose[0] ][pose[1]+ 1]
            data[(1,0)] = self._grid[pose[0]-1][pose[1]]
            data[(-1,0)] = self._grid[pose[0]+1][pose[1]]


        return data
    
    def checkPositionFree(self, position):   # test if a new position is valid
        print self._grid[position[1]][position[0]]
        if self._grid[position[1]][position[0]] == 0:
            return True            
        else:
            return False

    def setStone(self, position):
        self._stones += [position]
        self._grid[position[1]][position[0]] = 10
    
    def getGrid(self):
        return self._grid
        
    def updateRobotStates(self, robot_states):
        for name, state in self.robot_states.items():
            self._grid[state.pose[1]][state.pose[0]] = 0
            print "setting ",state.pose," to zero"
        self.robot_states = deepcopy(robot_states)
        for name, state in self.robot_states.items():
            print "update state: ",state.pose
            self._grid[state.pose[1]][state.pose[0]] = state.id + state.pose[2]
        for index, position in enumerate(self._stones[:]):
            self._grid[position[1]][position[0]] -= 1            
            if self._grid[position[1]][position[0]] == 0:
                self._stones.pop(index)
                
                
    def getStartPosition(self):
        Maze.start_index += 1
        print "setting start position",self._start_positions[Maze.start_index -1]
        return self._start_positions[Maze.start_index -1]
    
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
    
