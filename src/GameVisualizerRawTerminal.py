# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:06:41 2012

@author: DFKI-MARION-2
"""

class GameVisualizerRawTerminal(object):
    FORMATTER = {0: ' ', 1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',
                 128:'E',129:'O',
                 150: '^', 151: '>', 152: 'v', 153: '<',
                 154: '^', 155: '>', 156: 'v', 157: '<',
                 158: '^', 159: '>', 160: 'v', 161: '<',
                 192: 'X', 255: '#'}
    
    def __init__(self, maze):
        self._maze = maze

    def showState(self):
        for row in self._maze.getGrid():
            print ' '.join([GameVisualizerRawTerminal.FORMATTER[i] for i in row])
