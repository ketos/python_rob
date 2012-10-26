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
        self.pose = [0, 0, 0]
        self.battery = 100
        self.stones = 3
        self.sense = False

class GameMaster(object):
    def __init__(self):
        self.robot_clients = {}
        self.robot_states = {}
        self.maze = Maze('../data/maze1.pgm')
        self.visualizer = GameVisualizer(self.maze)

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
        pass

    def gameFinished(self):
        return False

    def startGame(self):
        i = 0 # just for testing
        self.maze.updateRobotStates(self.robot_states)
        while i < 15: #not self.gameFinished()
            i += 1
            sleep(0.01)
            self.visualizer.showState()
            
            for name, robot in self.robot_clients.items():
                if self.robot_states[name].sense == True:
                    data = self.maze.getSensorData(self.robot_states[name].pose)
                    robot.setSensorData(data)
                    self.robot_states[name].sense = False
                command = robot.getNextCommand()
                print command
                if command == Command.RightTurn:
                    self.robot_states[name].pose[2] = (self.robot_states[name].pose[2] + 1) % 4
                if command == Command.LeftTurn:
                    self.robot_states[name].pose[2] = (self.robot_states[name].pose[2] - 1) % 4
                if command == Command.Sense:
                    self.robot_states[name].sense = True
                if command == Command.DropStone:
                    self.robot_states[name].stones -= 1
                    if self.robot_states[name].stones > 0:
                        position = [self.robot_states[name].pose[0], self.robot_states[name].pose[1]]
                        if self.robot_states[name].pose[2] == 0:
                            position[1] += 1
                        if self.robot_states[name].pose[2] == 2:
                            position[1] -= 1
                        if self.robot_states[name].pose[2] == 1:
                            position[0] += 1
                        if self.robot_states[name].pose[2] == 3:
                            position[0] -= 1
                        if self.maze.checkPositionFree(position) == True:
                            self.maze.setStone(position)
                if command == Command.MoveForward:
                    position = [self.robot_states[name].pose[0], self.robot_states[name].pose[1]]
                    if self.robot_states[name].pose[2] == 0:
                        position[1] -= 1
                    if self.robot_states[name].pose[2] == 2:
                        position[1] += 1
                    if self.robot_states[name].pose[2] == 1:
                        position[0] -= 1
                    if self.robot_states[name].pose[2] == 3:
                        position[0] += 1
                    if self.maze.checkPositionFree(position) == True:
                        print "update robot position"
                        self.robot_states[name].pose[0] = position[0]
                        self.robot_states[name].pose[1] = position[1]
                    else:
                        print "bumper"
                        self.robot_clients[name].setBumper()
                
                self.maze.updateRobotStates(self.robot_states)

if __name__ == "__main__":
    #hier weiter startposition passt nicht es wird Ziel ersetzt
    #und es wird nicht nachher wieder auf 0 gesetzt
    #print '\033[1;31mRed like Radish\033[1;m'
    master = GameMaster()
    master.initGame()
    #for name in sys.argv:
    #    master.addClient(name)
    master.addClient("TestClient")
    master.startGame()
