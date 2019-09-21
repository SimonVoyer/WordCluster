# -*- coding: utf-8 -*-
'''
----------------
 textReader.py 
----------------
'''
import numpy as np
import re
import math
import time
from SqliteDAO import *

def uploadFiles(pathList, enc):
    list = []
    for path in pathList:
        file = open(path, mode='r', encoding = enc)
        list.append(file)
    return list
 
def readTexts(filesList):
    wordList = []
    for file in filesList:
        for line in file.readlines():
            words = line.split()
            for word in words:
                word = normalize(word)
                if word is not "":
                    wordList.append(word)
    return wordList

def normalize(word):
    word = word.lower() # Mettre en minuscule
    word = re.sub('.*\'', '', word) # Enlever ce qui vient avec un apostrophe
    word = word.translate({ord(c): None for c in ".,!?:;«»"}) # Retirer ponctuation ou caractère spécial
    return word

def constructRegex(word):
    expression = r"\b{}s?.?,?\b"
    return re.compile(expression.format(re.escape(word)))
      
def getWordList(windowSize, encoding, pathList):
    wordList = readTexts(uploadFiles(pathList, encoding))
    return wordList
