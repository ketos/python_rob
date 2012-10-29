# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:24:15 2012

@author: DFKI-MARION-2
"""

import sys
from copy import deepcopy

def neighbors(p):
    neighbors = [(p[0], p[1] - 1),(p[0] + 1, p[1]),
                 (p[0], p[1] + 1),(p[0] - 1, p[1])]
    for t in neighbors:
        yield t
        
class Stone(object):
    def __init__(self,counter, position):
        self.counter = counter
        self.position = position        

class Bomb(object):
    def __init__(self,counter, position):
        self.counter = counter
        self.position = position    
        
class Maze(object):
    start_index = 0
    def __init__(self, filename):
        self._grid = Maze._loadGrid(filename)
        self._start_positions = []
        self._loading_stations = []
        self._portals = []
        self._stones = []
        self._bombs = []
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
                if value == 192:
                    self._goal = (y,x)
                if value == 128:
                    self._loading_stations += [(y,x)]
                if value == 129:
                    self._portals += [(y,x)]
                    
                    
        print self._start_positions
    
    def getSensorData(self, state):       # pose as (x,y,theta) tuple
        data = {}
        indicees = state.getIndicees()
        #print "getSensorData: ",indicees
        data["front"] = self._grid[indicees[0][1]][indicees[0][0]]
        data["right"] = self._grid[indicees[1][1]][indicees[1][0]]
        data["back"] = self._grid[indicees[2][1]][indicees[2][0]]
        data["left"] = self._grid[indicees[3][1]][indicees[3][0]]
        return data
        
    def getGoal(self):
        return self._goal
    
    def checkPositionFree(self, position):   # test if a new position is valid
        if self._grid[position[1]][position[0]] == 0:
            return True            
        else:
            return False

    def setStone(self, position):
        counter = 10
        self._stones += [Stone(counter,position)]
        #self._grid[position[1]][position[0]] = 10
        
    def setBomb(self, position):
        counter = 3
        self._bombs += [Bomb(counter, position)]
        #self._grid[position[1]][position[0]] = 3
    
    
    def getGrid(self):
        return self._grid
        
    def updateRobotStates(self, robot_states):
        for name, state in self.robot_states.items():
            self._grid[state.position[1]][state.position[0]] = 0
            #print "setting ",state.pose," to zero"
        self.robot_states = deepcopy(robot_states)
        for position in self._loading_stations:
            self._grid[position[1]][position[0]] = 128 
        for y,x in self._portals:
            self._grid[y][x] = 129
            
        for name, state in self.robot_states.items():
            #print "update state: ",state.pose
            self._grid[state.position[1]][state.position[0]] = state.id + state.orientation

    def updateRound(self, robot_states):
        for index, stone in reversed(list(enumerate(self._stones[:]))):
            stone.counter -= 1
            self._grid[stone.position[1]][stone.position[0]] = stone.counter            
            if stone.counter == 0:
                self._stones.pop(index)
        for index, bomb in reversed(list(enumerate(self._bombs[:]))):
            bomb.counter -= 1            
            self._grid[bomb.position[1]][bomb.position[0]] = bomb.counter
            if bomb.counter == 0:
                for x,y in neighbors(bomb.position):
                    self._grid[y][x] = 0
                    for robot in robot_states.values():
                        if robot.position[0] == x and robot.position[1] == y:
                            robot.battery = 0
                            self._grid[y][x] = robot.id + robot.orientation
                print self._bombs, index
                self._bombs.pop(index)
                
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
    
