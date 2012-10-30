# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:06:41 2012

@author: DFKI-MARION-2
"""

# colored terminal output also for Windows (untested)
from colorama import init, Back, Style

class GameVisualizerColorTerminal(object):
    FORMATTER = {0: ' ', 1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',
                 128:'E',129:'O',
                 150: '^', 151: '>', 152: 'v', 153: '<',
                 154: '^', 155: '>', 156: 'v', 157: '<',
                 158: '^', 159: '>', 160: 'v', 161: '<',
                 192: 'X', 255: ' '}
    
    COLORIZER = {0:Back.BLACK,  #@UndefinedVariable
                 1:Back.RED, 2:Back.RED, 3:Back.RED, 4:Back.RED, 5:Back.RED, 6:Back.RED, 7:Back.RED, 8:Back.RED, 9:Back.RED,  #@UndefinedVariable
                 128:Back.MAGENTA, 129:Back.CYAN, #@UndefinedVariable
                 150:Back.GREEN, 151:Back.GREEN, 152:Back.GREEN, 153:Back.GREEN, #@UndefinedVariable
                 154:Back.YELLOW, 155:Back.YELLOW, 156:Back.YELLOW, 157:Back.YELLOW, #@UndefinedVariable
                 158:Back.BLUE, 159:Back.BLUE, 160:Back.BLUE, 161:Back.BLUE, #@UndefinedVariable
                 192:Back.CYAN, 255:Back.WHITE} #@UndefinedVariable

    def __init__(self, maze):
        self._maze = maze
        init()

    def showState(self):
        # clear console
        print '\033[H\033[J'
        
        print Style.BRIGHT #@UndefinedVariable
        
        for row in self._maze.getGrid():
            # '\x1b[0m' = all attributes off
            # '\x1b[1m' = bold text
            print ''.join([GameVisualizerColorTerminal.COLORIZER[i] +
                           GameVisualizerColorTerminal.FORMATTER[i] + 
                           ' ' for i in row]) #@UndefinedVariable
        
        print Back.RESET + Style.RESET_ALL #@UndefinedVariable
