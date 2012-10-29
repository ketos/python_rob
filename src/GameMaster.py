# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:57:26 2012

@author: DFKI-MARION-2
"""
import sys
from time import sleep

from Maze import *
from BaseRobotClient import *
from GameVisualizer import GameVisualizer

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
    
    def getIndicees(self):
        """
        shifts robot position

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
        self.maze = Maze('../data/maze1.pgm')
        self.visualizer = GameVisualizer(self.maze)

    def addClient(self, clientName):
        print clientName
        module = __import__(clientName)
        if clientName in self.robot_clients.keys():
            clientName = clientName + str(len(self.robot_clients))
        self.robot_clients[clientName] = module.TestClient()
        self.robot_states[clientName] = RobotState()
        start_position = self.maze.getStartPosition()
        self.robot_states[clientName].id = start_position[0]        
        self.robot_states[clientName].position = start_position[1:3]
        self.robot_states[clientName].orientation = start_position[-1]

    def initGame(self):
        for name, robot in self.robot_clients.items():
            robot.setGoal(self.maze.getGoal())
            robot.setStartPose(self.robot_states[name].position,self.robot_states[name].orientation )
            #TODO robot.setLoadingStations(self.maze.getLoadingStations())

    def gameFinished(self):
        goal = self.maze.getGoal()
        for state in self.robot_states.values():
            if goal[0] == state.pose[0] and goal[1] == state.pose[1]:
                return True   
        return False

    def startGame(self):
        i = 0 # just for testing
        self.maze.updateRobotStates(self.robot_states)
        while i < 100: #
        #while not self.gameFinished(): #i < 10: #
            i += 1
            sleep(0.01)
            self.visualizer.showState()
            
            for name, robot in self.robot_clients.items():
                sensor_data = None
                if self.robot_states[name].sense == True:
                    sensor_data = self.maze.getSensorData(self.robot_states[name])
                    self.robot_states[name].sense = False
                    
                command = robot.getNextCommand(sensor_data, self.robot_states[name].bumper)
                print name, "command:", Command.names[command]
                print "battery: ", self.robot_states[name].battery

                self.robot_states[name].bumper = False
                
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
                            print "update robot position"
                            self.robot_states[name].position = position[:]
                        else:
                            self.robot_states[name].bumper = True
                
                if command == Command.Stay:
                    if self.robot_states[name].battery < 100:
                        self.robot_states[name].battery += 1
                self.maze.updateRobotStates(self.robot_states)
            self.maze.updateRound(self.robot_states)

if __name__ == "__main__":
    master = GameMaster()
    
    #for name in sys.argv:
    #    master.addClient(name)
    master.addClient("TestClient")
    master.addClient("TestClient")
    master.addClient("TestClient")
    master.initGame()    
    master.startGame()
