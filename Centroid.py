# -*- coding: utf-8 -*-
'''
----------
 Centroid.py
----------
'''
import numpy as np

class Centroid:
    def __init__(self):
        self.coordinates = None
        self.tag = None
        
    def setNpArray(self, npArray):
        self.coordinates = npArray
        
    def setTag(self,tag):
        self.tag = tag
    
    def average(self, pointsList):
        if len(pointsList) is not 0 :
            accumulator = np.zeros(self.coordinates.shape[0])
            for point in pointsList:
                accumulator += point.coordinates
            self.move( accumulator * 1 / len(pointsList))
        
    def move(self, coordinates):
        self.coordinates = coordinates
        
        