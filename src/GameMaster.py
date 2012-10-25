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
        self.pose = [0.0, 0.0, 0.0]
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

    def initGame(self):
        pass

    def gameFinished(self):
        pass

    def startGame(self):
        self.visualizer.showState()
        while not self.gameFinished():
            sleep(0.01)
            for name, robot in self.robot_clients.items():
                if self.robot_states[name].sense == True:
                    data = self.maze.getSensorData(self.robot_states[name].pose)
                    robot.setSensorData(data)
                command = robot.getNextCommand()

                if command == Command.RightTurn:
                    self.robot_states[name].pose[2] = (self.robot_states[name].pose[2] + 1) % 4
                if command == Command.LeftTurn:
                    self.robot_states[name].pose[2] = (self.robot_states[name].pose[2] - 1) % 4
                if command == Command.Sense:
                    self.robot_states[name].sense = True
                if command == Command.DropStone:
                    self.robot_states[name].stones -= 1
                    if self.robot_states[name].stones > 0:
                        self.maze.setStone(self.robot_states[name].pose)
                if command == Command.MoveForward:
                    position = [0, 0]
                    if self.robot_states[name].pose[2] == 0:
                        position[0] = self.robot_states[name].pose[0] + 1
                    if self.robot_states[name].pose[2] == 2:
                        position[0] = self.robot_states[name].pose[0] - 1
                    if self.robot_states[name].pose[2] == 1:
                        position[1] = self.robot_states[name].pose[1] + 1
                    if self.robot_states[name].pose[2] == 3:
                        position[1] = self.robot_states[name].pose[1] - 1
                    if self.maze.checkNewPosition(position) == True:
                        self.robot_states[name].pose[0] = position[0]
                        self.robot_states[name].pose[1] = position[1]
                    else:
                        self.robot_clients[name].setBumper()

if __name__ == "__main__":
    master = GameMaster()
    master.initGame()
    #for name in sys.argv:
    #    master.addClient(name)
    master.addClient("TestClient")
    master.startGame()
