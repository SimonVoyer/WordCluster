# -*- coding: utf-8 -*-
'''
----------
 ClusterAlgo.py
----------
'''
import numpy as np
from Centroid import *
from Point import *
from random import randint
from time import time
import math

class ClusterAlgo:
    def __init__(self, matrix, wordIndexes, nbWordsDisplay, centroidCount = None, userCentroids=None):
        
        self.nbWordsDisplay = nbWordsDisplay
        self.matrix = matrix
        self.wordIndexes = wordIndexes
        self.sizeOfMatrix = self.matrix.shape[0]
        self.centroidsList = []
        self.pointsList = []
        self.pointsTags = np.zeros(self.sizeOfMatrix)
        self.active = True
        self.chrono = time()
        self.pointsPerCluster = {}
        self.totalTime = 0
        self.userDefinedCentroids = None

        if userCentroids != None:
            self.userDefinedCentroids = userCentroids
            self.userDefinedCentroidsConstructor(userCentroids)
        else:
            self.centroidCountConstructor(centroidCount)
    
    def centroidCountConstructor(self, centroidCount):
        self.centroidCount = centroidCount
        if centroidCount == None:
            self.centroidCount = 10
        self.initializePoints()
        self.createCentroids()
        self.moveCentroids()
    
    def userDefinedCentroidsConstructor(self, userCentroids):
        self.centroidCount = len(userCentroids)
        self.userCentroids = userCentroids
        self.initializePoints()
        self.centroidsFromWords()
        self.setCentroidsTags()
    
    def process(self):

        count = 1
        self.printHeader()
        
        while self.active:
            tempTags = np.copy(self.pointsTags)
            for i in range(0, len(self.pointsList)):
                self.pointsTags[i] = self.pointsList[i].assignToCentroid(self.centroidsList)
            
            nbOfZeros = (np.equal(tempTags, self.pointsTags)== 0).sum()
            nbOfIdenticalPoints = self.pointsTags.size - nbOfZeros
            self.moveCentroids()
            if nbOfIdenticalPoints == self.pointsTags.size:
                self.active = False
            
            self.printTime(count)
            print("nb de modifications: ", nbOfZeros)
            self.printPointsPerCluster()
            count +=1 


        self.printWordsPerCluster()
     
    #----- INITIALIZE CENTROIDS -----#
        
    def createCentroids(self):
        for i in range(0, self.centroidCount):
            centroid = Centroid()
            centroid.setTag(i)
            centroid.setNpArray(np.zeros(self.sizeOfMatrix))
            self.centroidsList.append(centroid)
        
    def randomizeCentroids(self):
        for i in range(self.centroidCount):
            c = Centroid(self.randomizeCentroid())
            self.centroidsList.append(c)
    
    def centroidsFromWords(self):
        
        for i in self.userCentroids:
            c = Centroid()
            c.setNpArray(self.matrix[i])
            self.centroidsList.append(c)
        
    def setCentroidsTags(self):
        tagCount = 0
        for centroid in self.centroidsList:
            centroid.setTag(tagCount)
            tagCount += 1

    #----- INITIALIZE POINTS -----#
    def initializePoints(self):
        indexCount = 0
        for line in self.matrix:
            p = Point(line, indexCount)
            p.setTag(randint(0, self.centroidCount - 1))
            self.pointsList.append(p)
            self.pointsTags[indexCount] = p.tag
            indexCount+=1
    
    #----- ALGO PROCESS -----#        
    def assignPointsToCentroid(self):
        for point in self.pointsList:
            self.active = point.assignToCentroid(self.centroidsList)

    def moveCentroids(self):
        self.pointsPerCluster = self.pointChecker()
        
        for centroid in self.centroidsList:
            if centroid.tag in self.pointsPerCluster:
                centroid.average(self.pointsPerCluster[centroid.tag])
           
    def pointChecker(self):
        tempDict = {}
        for point in self.pointsList:
            if point.tag not in tempDict:
                tempDict[point.tag] = []
            tempDict[point.tag].append(point)
        return tempDict
    
    def printTime(self, step):
        print("-----------------------------------------------------------------")
        self.formatTime()
        print("\nItération no", step, ", temps d'exécution", round(time() - self.chrono), "secondes.\n")
        self.chrono = time()
    
    def formatTime(self):
        self.totalTime += time()-self.chrono
        duree = self.totalTime
        heures = duree // 3600
        minutes = (duree - (heures * 3600)) // 60
        secondes = math.floor(duree - (heures * 3600) - (minutes * 60))

        print("Temps écoulé : ", heures, "heures", minutes, "minutes", secondes, "secondes.")
            
    def printHeader(self):
        print ("\n\nCe test est effectué avec : ", self.centroidCount, "centroïdes.")
        flippedDict = {}
        for word, index in self.wordIndexes.items():
            flippedDict[index] = word

        if (self.userDefinedCentroids):
            print("Centroides définis par l'utilisateur. Voici la liste de mots choisis:")
            for c in self.userDefinedCentroids:
                print(flippedDict[c])
        else:
            print("Centroides déterminés au hasard.")
        
        print("================================================================\n")
            
    def printPointsPerCluster(self):
        for cluster, points in self.pointsPerCluster.items():
            print("Le cluster", cluster+1, "contient", len(points), "point(s)")

    def printWordsPerCluster(self):
        
        list = []
        invertedIndexes = {value : key for key,value in self.wordIndexes.items()}
        
        print ("---------------------------------------------")
        print()
        
        for c in self.centroidsList:
            list.append([point for point in self.pointsList if point.tag == c.tag])
            
        for l in list:
            if l != []:
                print("\nCentroid no.", l[0].tag+1, "\n")
            l.sort(key = lambda x : x.score) 
            for i in range(self.nbWordsDisplay):
                if i < len(l):
                    print(i+1,".", invertedIndexes[l[i].wordIndex], " : ", l[i].score)
