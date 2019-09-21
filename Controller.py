# -*- coding: utf-8 -*-
'''
----------------
 Controller.py
----------------
'''
import sys
from time import time
import gc # garbage collector
import textReader as TextReader
import algo as Algo
import commandParser as cp
from SqliteDAO import *
import numpy as np
from Constant import *
from ClusterAlgo import *

class Controller:
    def __init__(self, argList):
        self.argDict = dict.fromkeys(["verbose", "mode", "window", "encoding", "path", "drop", "clusterCount", "wordCount", "userCentroids"])
        self.arguments = argList
        self.database = SqliteDAO()
        self.argDict["verbose"] = False

        self.wordList = None
        self.matrix = None
        self.indexes = None
        self.chrono = None
    
    def process(self):
        cp.parseCommandArguments(self.arguments, self.argDict)
        self.printWelcomeMsg()
        if self.argDict["mode"] == "drop":
            self.database.dropAndCreateTables()
        if self.argDict["verbose"]:
            self.chrono = time()
        if self.argDict["mode"] == "training":
            self.training()
        elif self.argDict["mode"] == "synonym":
            self.research()
        elif self.argDict["mode"] == "cluster":
            self.cluster()
            
    def training(self):
        self.wordList = TextReader.getWordList(self.argDict["window"], self.argDict["encoding"], self.argDict["path"])
        self.printTime("lecture")
        self.indexes = self.database.insertDictionary(self.wordList)
        self.printTime("insertions d'index")
        self.database.insertMatrix(self.findCooccurences())
        self.printTime("insertion de scores")
        self.printGoodbyeMsg()
        
    def research(self):
        self.indexes = self.database.insertDictionary([])
        self.printTime("obtenir dictionnaire")
        self.buildMatrix()
        self.printTime("bâtir la matrice")
        self.ask()
        
    def cluster(self):
        self.indexes = self.database.insertDictionary([])
        self.printTime("obtenir dictionnaire")
        self.buildMatrix()
        self.printTime("bâtir la matrice")
        if (self.argDict["clusterCount"]):
            c = ClusterAlgo(self.matrix, self.indexes, self.argDict["wordCount"], self.argDict["clusterCount"])
        elif (self.argDict["userCentroids"]) :
            centroidsIndexes = self.validateUserDefinedCentroids()
            if len(centroidsIndexes) == len(self.argDict["userCentroids"]):
                c = ClusterAlgo(self.matrix, self.indexes, self.argDict["wordCount"], None, centroidsIndexes)
            else:
                raise Exception("Un des mots choisis comme centroïdes est invalide.")
        else :
            c = ClusterAlgo(self.matrix, self.indexes, self.argDict["wordCount"])
        c.process()

    def validateUserDefinedCentroids(self):
        
        return [ self.indexes[word] for word in self.argDict["userCentroids"] if word in self.indexes ]

    def findCooccurences(self):
        dict = {}
        tempWindowSize = self.argDict["window"]//2
        for i in range(len(self.wordList)):
            wordIndex = self.indexes[self.wordList[i]]
            for j in range(1, tempWindowSize):
                if j != wordIndex:
                    try:
                        tempIndex = self.indexes[self.wordList[i+j]] 
                        if tempIndex <= wordIndex:
                            key = (tempIndex, wordIndex, self.argDict["window"])
                            if key not in dict:
                                dict[key] = 1
                            else:
                                dict[key] = dict[key] + 1
                        tempIndex = self.indexes[self.wordList[i-j]]
                        if tempIndex <= wordIndex:
                            key = (tempIndex, wordIndex, self.argDict["window"])
                            if key not in dict:
                                dict[key] = 1
                            else:
                                dict[key] = dict[key] + 1
                    except IndexError:pass
        return dict
    
    def saveData(self):
        self.database.insertDictionary(self.indexes)
        data = []
        validIndexes = np.transpose(self.matrix.nonzero())
        for line, column in validIndexes:
            line = line.item()
            column = column.item()
            score = self.matrix[line][column].item()
            data.append([line, column, score])
        self.database.saveMatrix(data, self.argDict["window"])
    
    def buildMatrix(self):
        matrixSize = len(self.indexes) 
        tempMatrix = np.zeros((matrixSize, matrixSize))
        reducedMatrix = self.database.databaseToMatrix(self.argDict["window"])
        for line, column, score in reducedMatrix:
            tempMatrix[line][column] = score
            tempMatrix[column][line] = score
        self.matrix = tempMatrix
        
    def printTime(self, step):
        if self.argDict["verbose"]:
            print("Pour étape: ", step, ", temps d'exécution: ", round(time() - self.chrono, 2), " secondes. \n")
            self.chrono = time()
    
    def printWelcomeMsg(self):
        print("Vous êtes en mode " + self.argDict["mode"] + ".")
        print("Taille de la fenêtre : ", self.argDict["window"])

    def printGoodbyeMsg(self):
        print("Exécution terminée avec succès.")
        
    def ask(self):
        choice = input(ASK_FOR_SEARCH_OPTIONS)
        if choice == 'q':
            sys.exit()
        else:
            try:
                list = choice.split()
                word = list[0].lower()
                nbResults = int(list[1])
                method = int(list[2])
                if method > 3:
                    print(METHOD_ERROR_MSG_3)
                elif nbResults > 100:
                    print(NB_OF_RESULTS_ERROR_MSG)
                else:
                    if self.argDict["verbose"]:
                        self.chrono = time()
                    results = Algo.getData(method, word, nbResults, self.matrix, self.indexes)
                    for i in range(nbResults):
                        print(i+1, " : ", results[i][0], ", score = ", results[i][1])
                    print("")
                    self.printTime("demander")
                    gc.enable()
            except KeyError as e:
                    print(e)
                    print(KEY_ERROR_MSG)
            except IndexError as e:
                    print(e)
                    print(INDEX_ERROR_MSG)
            self.ask()
