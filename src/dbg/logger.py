# -*- coding: utf-8 -*-
'''
Created on 29.11.2012

@author: tim
'''
import logging

class logger(object):
    ##
    # @brief konstruktor
    #
    #
    def __init__(self):
        self.logger = logging.getLogger('Robot_Team2')
        self.flog = logging.FileHandler('./flog.log')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s\t%(message)s')
        self.flog.setFormatter(self.formatter)
        self.logger.addHandler(self.flog)
        self.logger.setLevel(logging.INFO)
        
    ##
    # @brief logt den info string
    #
    #
    def info(self, value):
        self.logger.info(value)

