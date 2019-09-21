# -*- coding: utf-8 -*-
'''
----------
 Point.py
----------
'''
import numpy as np
from Centroid import *
from algo import leastSquares

class Point(Centroid):
    def __init__(self, npArray, wordIndex):
        Centroid.__init__(self)
        self.wordIndex = wordIndex
        self.setNpArray(npArray)
        self.score = None

    def assignToCentroid(self, centroidsList):
        min = 0
        for centroid in centroidsList:
            score = leastSquares(self.coordinates, centroid.coordinates)
            if min == 0 or score < min:
                min = score
                self.tag = centroid.tag
                self.score = score
        return self.tag
        