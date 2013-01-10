# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:57:26 2012

@author: Stefan Stiene
"""
import sys
import math
from time import sleep

from Maze import *
from BaseRobotClient import *
#from GameVisualizerMatplotlib import GameVisualizerMatplotlib as GameVisualizer
from GameVisualizerRawTerminal import GameVisualizerRawTerminal as GameVisualizer
#from GameVisualizerColorTerminal import GameVisualizerColorTerminal
#from GameVisualizerImage import GameVisualizerImage
import traceback

class RobotState(object):
    def __init__(self):
        self.id = -1
        self.position = [0, 0]
        self.orientation = 0
        self.battery = 100
        self.stones = 3
        self.bombs = 3
        self.sense = False
        self.bumper = False
        self.teleported = False
    
    def getIndicees(self):
        """
        returns the indecees in the maze around the robot position

        0: vorne
        1: r
        2: h
        3: l
        """
        indicees = [[self.position[0], self.position[1] - 1],
                     [self.position[0] + 1, self.position[1]],
                     [self.position[0], self.position[1] + 1],
                     [self.position[0] - 1, self.position[1]]]
        return indicees[self.orientation:] + indicees[:self.orientation]
        
class GameMaster(object):
    def __init__(self):
        self.robot_clients = {}
        self.robot_states = {}
        self.maze = Maze('../data/maze3s.pgm')
        # don't use: self.visualizer = GameVisualizerImage(self.maze)
        self.visualizer = GameVisualizer(self.maze)
        #self.visualizer = GameVisualizerRawTerminal(self.maze)

    def addClient(self, clientName):
        
        print clientName
        module = __import__(clientName)
        if clientName in self.robot_clients.keys():
            clientName = clientName + str(len(self.robot_clients))

        self.robot_clients[clientName] = module.robot_team2()   # TODO get class name 
        self.robot_states[clientName] = RobotState()
        start_position = self.maze.getStartPosition()
        self.robot_states[clientName].id = start_position[0]        
        self.robot_states[clientName].position = start_position[1:3]
        self.robot_states[clientName].orientation = start_position[-1]

    def initGame(self):
        pass

    def gameFinished(self):
        goal = self.maze.getGoal()
        for state in self.robot_states.values():
            if goal == state.position:
                return True   
        return False
    
    def getCompass(self,robot_state):
        goal = self.maze.getGoal()
        position = robot_state.position
        angle = math.atan2( goal[1] - position[1] , goal[0] - position[0]) * 180.0 / math.pi + 90;
        compass = round(angle/45) - (robot_state.orientation * 2)
        if compass < 0:
            compass += 8
        return compass
        
        
        
    def startGame(self):
        i = 0 # just for testing
        self.maze.updateRobotStates(self.robot_states)
        while i < 40000 and not self.gameFinished(): # i < 10: #
            i += 1
            sleep(0.05)
            self.visualizer.showState()
            #a = raw_input()
            print "round",i
            for name, robot in self.robot_clients.items():
                sensor_data = None
                if self.robot_states[name].sense == True:
                    sensor_data = self.maze.getSensorData(self.robot_states[name])
                    sensor_data["battery"] = self.robot_states[name].battery
                    sensor_data["stones"] = self.robot_states[name].stones
                    sensor_data["bombs"] = self.robot_states[name].bombs
                    self.robot_states[name].sense = False
                compass = self.getCompass(self.robot_states[name])
                command = 0
                try:
                    command = robot.getNextCommand(sensor_data, self.robot_states[name].bumper, compass,self.robot_states[name].teleported)
                except Exception, e:
                    print "Couldn't do it: %s" % e
                    traceback.print_exc()
                    a = raw_input()
                print name, "command:", Command.names[command]
                print "battery: ", self.robot_states[name].battery

                self.robot_states[name].bumper = False
                self.robot_states[name].teleported = False
                if command == Command.RightTurn:
                    if self.robot_states[name].battery > 0:
                        self.robot_states[name].battery -= 1
                        self.robot_states[name].orientation = (self.robot_states[name].orientation + 1) % 4
                if command == Command.LeftTurn:
                    if self.robot_states[name].battery > 0:
                        self.robot_states[name].battery -= 1
                        self.robot_states[name].orientation = (self.robot_states[name].orientation - 1) % 4
                if command == Command.Sense:
                    self.robot_states[name].sense = True
                if command == Command.DropStone:
                    if self.robot_states[name].stones > 0:
                        position = self.robot_states[name].getIndicees()[2]
                        if self.maze.checkPositionFree(position) == True:
                            self.robot_states[name].stones -= 1
                            self.maze.setStone(position)
                if command == Command.DropBomb:  
                    if self.robot_states[name].bombs > 0:
                        position = self.robot_states[name].getIndicees()[2]
                        if self.maze.checkPositionFree(position) == True:
                            self.robot_states[name].bombs -= 1                            
                            self.maze.setBomb(position)                            
                if command == Command.MoveForward:
                    if self.robot_states[name].battery > 0:
                        self.robot_states[name].battery -= 1
                        position = self.robot_states[name].getIndicees()[0]
                        if self.maze.checkPositionFree(position) == True:
                            self.robot_states[name].position = position[:]
                            if self.maze.checkPortal(position) == True:                               
                                newPosition = self.maze.getFreePortal(self.robot_states)
                                if newPosition != None:
                                    self.robot_states[name].position = newPosition[:]
                                    self.robot_states[name].teleported = True
                        else:
                            self.robot_states[name].bumper = True
                
                if command == Command.Stay:
                    if self.robot_states[name].battery < 100:
                        if self.robot_states[name].position in self.maze.getLoadingStations():
                            self.robot_states[name].battery += 30
                        else:
                            self.robot_states[name].battery += 1
                        if self.robot_states[name].battery > 100:
                            self.robot_states[name].battery = 100
                self.maze.updateRobotStates(self.robot_states)
            self.maze.updateRound(self.robot_states)

if __name__ == "__main__":
    master = GameMaster()
    
    #for name in sys.argv:
    #    master.addClient(name)
    master.addClient("robot_team2")
    #master.addClient("robot_team2")
    #master.addClient("robot_team2")
    
    #master.addClient("TestClient")
    #master.addClient("TestClient")
    master.initGame()    
    master.startGame()
    #import cProfile
    #cProfile.run("master.startGame()")
