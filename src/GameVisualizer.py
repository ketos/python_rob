# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:06:41 2012

@author: DFKI-MARION-2
"""

#import Image
from numpy import array
from time import sleep

class GameVisualizer(object):
    FORMATTER = {0: ' ', 1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',
                 128:'E',129:'O',
                 150: '^', 151: '>', 152: 'v', 153: '<',
                 154: '^', 155: '>', 156: 'v', 157: '<',
                 158: '^', 159: '>', 160: 'v', 161: '<',
                 192: 'X', 255: '#'}
    #TODO add color to arrows
    def __init__(self, maze):
        self._maze = maze

    def showState(self):
        # show image window
        #inverted = GameVisualizer.invert(self._maze.getGrid())
        #im = Image.fromarray(array(inverted))
        #im = im.resize((im.size[0] * 20, im.size[1] * 20))
        #im.show()

        sleep(0.05)
        # print to console
        print '\033[H\033[J'
        for row in self._maze.getGrid():
            print ' '.join([GameVisualizer.FORMATTER[i] for i in row])
'''
    @staticmethod
    def invert(image):
        MAX_VAL = 255
        return [[(MAX_VAL - pixel) for pixel in row] for row in image]
'''
