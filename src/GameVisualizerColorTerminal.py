# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:06:41 2012

@author: DFKI-MARION-2
"""

class GameVisualizerColorTerminal(object):
    FORMATTER = {0:' ', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9',
                 150:'\x1b[48;5;1m' +'^', 151:'\x1b[48;5;1m' +'>', 152:'\x1b[48;5;1m' +'v', 153:'\x1b[48;5;1m' +'<',
                 154:'\x1b[48;5;2m' +'^', 155:'\x1b[48;5;2m' +'>', 156:'\x1b[48;5;2m' +'v', 157:'\x1b[48;5;2m' +'<',
                 158:'\x1b[48;5;4m' +'^', 159:'\x1b[48;5;4m' +'>', 160:'\x1b[48;5;4m' +'v', 161:'\x1b[48;5;4m' +'<',
                 192:'\x1b[38;5;1m' +'X', 255:'\x1b[48;5;255m' +'#'}

    def __init__(self, maze):
        self._maze = maze

    def showState(self):
        # clear console
        print '\033[H\033[J'
        
        for row in self._maze.getGrid():
            # '\x1b[0m' = all attributes off
            # '\x1b[1m' = bold text
            print ''.join(['\x1b[1m' + GameVisualizerColorTerminal.FORMATTER[i] + ' '  + '\x1b[0m' for i in row])
        
        # color off
        print '\x1b[0m'
