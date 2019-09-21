# -*- coding: utf-8 -*-
'''
----------
 algo.py
----------
'''
from Constant import *
import numpy as np
import time

def getStopList():
    with open(STOPLIST_PATH, mode='r', encoding = "UTF-8") as handler:
        return handler.read().split(",")

def getAlgoDict():
    return {1:scalaire, 2:leastSquares, 3:cityBlocks}

def runAlgo(matrix, dictWordToIndex, wordIndex, nbResults, method):
    scoreDict = {} # mot : score
    algoDict = getAlgoDict()
    dictIndexToWords = {value:key for key, value in dictWordToIndex.items()}
    for i in range(matrix.shape[0]):
        if i != wordIndex:
            scoreDict[dictIndexToWords[i]] = algoDict[method](matrix[i], matrix[wordIndex])
    return getResults(nbResults, sortScores(True if method is 1 else False, scoreDict))

def scalaire(t1, t2):
    return np.dot(t1, t2)

def leastSquares(t1, t2):
    return np.sum(np.square(np.subtract(t1, t2)))
    
def cityBlocks(t1, t2):
    return np.sum(np.absolute(np.subtract(t1,t2)))

def checkStopList(word):
    ''' Gérer manuellement certaines exceptions + passer la stop list '''
    test = True
    if word in getStopList() \
    or word.endswith("ait") \
    or word.endswith("ais") \
    or word.endswith("aient") \
    or len(word) < 2:
        test = False
    return test
 
def sortScores(rev, scoreDict):
    return sorted(scoreDict.items(), key=lambda k: k[1], reverse=rev) 

def getResults(nbResults, scores):
    listResults = []
    j = i = 0
    while j <= nbResults:
        if checkStopList(scores[i][0]):
            listResults.append([scores[i][0], scores[i][1]])
            j += 1
        i+=1
    return listResults  

def getData(method, word, nbResults, matrix, indexes):
    result = runAlgo(matrix, indexes, indexes[word], nbResults, method)
    return result
