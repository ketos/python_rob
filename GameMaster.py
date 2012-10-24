# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:57:26 2012

@author: DFKI-MARION-2
"""
import sys

class GameMaster(object):
    def __init__(self):
        pass
    def addClient(self,clientName):
        pass
    def initGame(self):
        pass
    def startGame(self):
        pass
    
if __name__ == "__main__":
    master = GameMaster()
    master.initGame()
    for name in sys.argv:
        master.addClient(name)
    master.startGame()