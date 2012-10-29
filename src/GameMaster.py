# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:57:26 2012

@author: DFKI-MARION-2
"""
import sys
from time import sleep

from Maze import *
from BaseRobotClient import *
from GameVisualizerRawTerminal import GameVisualizerRawTerminal
from GameVisualizerColorTerminal import GameVisualizerColorTerminal
from GameVisualizerImage import GameVisualizerImage

class RobotState(object):
    def __init__(self):
        self.id = -1
        self.pose = [0, 0, 0]
        self.battery = 100
        self.stones = 3
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
        indicees = [[self.pose[0], self.pose[1] - 1],
                     [self.pose[0] + 1, self.pose[1]],
                     [self.pose[0], self.pose[1] + 1],
                     [self.pose[0] - 1, self.pose[1]]]
        return indicees[self.pose[2]:] + indicees[:self.pose[2]]
        
class GameMaster(object):
    def __init__(self):
        self.robot_clients = {}
        self.robot_states = {}
        self.maze = Maze('../data/maze1.pgm')
        # don't use: self.visualizer = GameVisualizerImage(self.maze)
        # self.visualizer = GameVisualizerRawTerminal(self.maze)
        self.visualizer = GameVisualizerColorTerminal(self.maze)

    def addClient(self, clientName):
        print clientName
        module = __import__(clientName)
        print dir(module)
        self.robot_clients[clientName] = module.TestClient()
        self.robot_states[clientName] = RobotState()
        start_position = self.maze.getStartPosition()
        self.robot_states[clientName].id = start_position[0]        
        self.robot_states[clientName].pose = start_position[1:]

    def initGame(self):
        for name, robot in self.robot_clients.items():
            robot.setGoal(self.maze.getGoal())
            robot.setStartPose(self.robot_states[name].pose)
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
        while not self.gameFinished(): #i < 10: #
            i += 1
            sleep(0.2)
            self.visualizer.showState()
            
            for name, robot in self.robot_clients.items():
                sensor_data = None
                if self.robot_states[name].sense == True:
                    sensor_data = self.maze.getSensorData(self.robot_states[name])
                    self.robot_states[name].sense = False
                    
                command = robot.getNextCommand(sensor_data, self.robot_states[name].bumper)
                print "command:", Command.names[command]

                self.robot_states[name].bumper = False
                
                if command == Command.RightTurn:
                    if self.robot_states[name].battery > 0:
                        self.robot_states[name].battery -= 1
                        self.robot_states[name].pose[2] = (self.robot_states[name].pose[2] + 1) % 4
                if command == Command.LeftTurn:
                    if self.robot_states[name].battery > 0:
                        self.robot_states[name].battery -= 1
                        self.robot_states[name].pose[2] = (self.robot_states[name].pose[2] - 1) % 4
                if command == Command.Sense:
                    self.robot_states[name].sense = True
                if command == Command.DropStone:
                    self.robot_states[name].stones -= 1
                    if self.robot_states[name].stones > 0:
                        position = self.robot_states[name].getIndicees()[2]
                        if self.maze.checkPositionFree(position) == True:
                            self.maze.setStone(position)
                if command == Command.MoveForward:
                    if self.robot_states[name].battery > 0:
                        self.robot_states[name].battery -= 1
                        position = self.robot_states[name].getIndicees()[0]
                        if self.maze.checkPositionFree(position) == True:
                            print "update robot position"
                            self.robot_states[name].pose[0] = position[0]
                            self.robot_states[name].pose[1] = position[1]
                        else:
                            self.robot_states[name].bumper = True
                
                if command == Command.Stay:
                    if self.robot_states[name].battery < 100:
                        self.robot_states[name].battery += 1
                print "battery: ", self.robot_states[name].battery
                self.maze.updateRobotStates(self.robot_states)

if __name__ == "__main__":
    master = GameMaster()
    
    #for name in sys.argv:
    #    master.addClient(name)
    master.addClient("TestClient")
    master.initGame()    
    master.startGame()
