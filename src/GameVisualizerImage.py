# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:06:41 2012

@author: DFKI-MARION-2
"""

import Image
from numpy import array

class GameVisualizerImage(object):
    def __init__(self, maze):
        self._maze = maze

    def showState(self):
        # WARNING: this won't destroy the image window, so don't use this class
        # yet. If this should really be used at some time, one will have to
        # wrap this into a tkinter window.

        # show image window
        inverted = GameVisualizerImage.invert(self._maze.getGrid())
        im = Image.fromarray(array(inverted))
        im = im.resize((im.size[0] * 20, im.size[1] * 20))
        im.show()

    @staticmethod
    def invert(image):
        MAX_VAL = 255
        return [[(MAX_VAL - pixel) for pixel in row] for row in image]

