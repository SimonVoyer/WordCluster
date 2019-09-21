# -*- coding: utf-8 -*-
'''
--------------
 OracleDAO.py
--------------
'''
from Constant import *
import sqlite3

class SqliteDAO():
    def __init__(self):
        self.connection = sqlite3.connect("synonymes.db")
        self.cursor = self.connection.cursor()
        
    def insertDictionary(self, textList):
        dict = {}
        result = self.cursor.execute(SELECT_DICTIONARY)
        for index, word in result:
            dict[word] = index
        newList = []
        for word in textList:
            if word not in dict:
                newList.append((len(dict), word))
                dict[word] = len(dict)
        self.cursor.executemany(INSERT_DICTIONARY, newList)
        self.connection.commit()
        return dict

    def saveMatrix(self, dataSet, windowSize):
        self.insertMatrix(dataSet, windowSize)
        self.updateMatrix(dataSet, windowSize)
        
    def insertMatrix(self, dict):
        listOfInserts = []
        listOfUpdates = []
        dictFromBD = self.constructDictFromMatrixBD()
        for key, score in dict.items():
            if key in dictFromBD:
                newScore = score + dictFromBD[key] 
                listOfUpdates.append((newScore, key[0], key[1], key[2]))
            else:
                listOfInserts.append((key[0], key[1], key[2], score))
        self.cursor.executemany(INSERT_MATRIX, listOfInserts)
        if listOfUpdates:
            self.cursor.executemany(UPDATE_MATRIX, listOfUpdates)
        self.connection.commit()

    def constructDictFromMatrixBD(self):
        dictFromBD ={}
        valuesFromMatrix = self.cursor.execute(SELECT_ALL_MATRIX).fetchall()
        for t in valuesFromMatrix:
            dictFromBD[(t[0], t[1], t[2])] = t[3]
        return dictFromBD
                
    def databaseToMatrix(self, window_size):
        data = []
        line = None
        column = None
        score = None
        rows = self.cursor.execute(SELECT_ALL_MATRIX_2, (window_size,))
        for row in rows:
            line = row[LINE_INDEX]
            column = row[COLUMN_INDEX]
            score = row[SCORE]
            data.append((line,column,score))
        return data
    
    def dropAndCreateTables(self):
        try:
            self.cursor.execute(DROP_WORDS)
            self.cursor.execute(DROP_MATRIX)
        except: 
            pass
        finally:
            self.cursor.execute(CREATE_WORDS)
            self.cursor.execute(CREATE_MATRIX)
            