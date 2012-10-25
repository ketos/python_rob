# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:06:41 2012

@author: DFKI-MARION-2
"""

class GameVisualizer(object):
    FORMATTER = {0: ' ', 150: '1', 151: '2', 152: '3', 192: 'X', 255: '#'}

    def __init__(self, maze):
        self._maze = maze
        
    def showState(self):
        for row in self._maze.getGrid():
            print ' '.join([GameVisualizer.FORMATTER[i] for i in row])        
