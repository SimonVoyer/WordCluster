# -*- coding: utf-8 -*-
'''
-------------------
 commandParser.py
-------------------
types d'arguments:
    -e = entraînement
    -t = taille fenêtre
    --enc = encodage
    -r = rechercher synonyme
    --chemin = chemin et nom du fichier à lire
    --verbose = prints pour afficher le temps
    -d = drop et refait les tables
    -n = nb mots à afficher
    --nc = nb clusters
    -c = mode clustering
    --mots = liste de mots de l'utilisateur (optionnel)
'''

import re
from Constant import *

def parseCommandArguments(argumentVector, argDict):
    pathList = []
    userCentroidList = []
    pattern = re.compile("^-")

    findPath = False
    findCentroids = False
    del argumentVector[0]
    for i, argument in enumerate(argumentVector):
        if findPath or findCentroids:
            if pattern.match(argument):
                findPath = False
                findCentroids = False
            else:
                if findPath:
                    pathList.append(argument)
                else:
                    userCentroidList.append(argument)
        if not findPath and not findCentroids:
            if argument == "-e":
               if argDict["mode"] != None:
                   raise Exception(MODE_ERROR_MSG_1)
               else :
                   argDict["mode"] = "training"
            elif argument == "-r":
                if argDict["mode"] != None :
                   raise Exception(MODE_ERROR_MSG_1)
                else:
                    argDict["mode"] = "synonym"    
            elif argument == "--verbose":
               argDict["verbose"] = True
            elif argument == "-d":
                argDict["mode"] = "drop"
            elif argument =="-c":
                argDict["mode"] = "cluster"
            elif argument == "--enc":
               argDict["encoding"] = argumentVector[i+1]
            elif argument == "-t":
               argDict["window"] = int(argumentVector[i+1])
            elif argument == "-n": #nombre mot à afficher par centroïde
                argDict["wordCount"] = int(argumentVector[i+1])
            elif argument == "--nc": #nombre de centroïdes
                argDict["clusterCount"] = int(argumentVector[i+1])
            elif argument == "--chemin":
                findPath = True
            elif argument == "--mots":
                findCentroids = True
#     if argDict["mode"] == "training":
#         argDict["path"] = pathList
    if pathList:
        argDict["path"] = pathList
    elif userCentroidList:
        argDict["userCentroids"] = userCentroidList
    validateInputs(argDict) 
    return argDict
        
def validateInputs(argDict):
    if argDict["mode"] is not "drop":
        if argDict["clusterCount"] != None and argDict["userCentroids"] != None:
            raise Exception(MODE_ERROR_MSG_CUSTOM_CLUSTER)
        if argDict["mode"] == None:
            raise Exception(MODE_ERROR_MSG_2)
        if argDict["mode"] == "training":
            if argDict["encoding"] == None:
                raise Exception(ENCODING_ERROR_MSG)
            if argDict["path"] == [] or argDict["path"] == None:
                raise Exception(PATH_ERROR_MSG)
        if argDict["window"] == None or argDict["window"] < 1:
            raise Exception(WINDOW_SIZE_ERROR_MSG)
        if argDict["mode"] == "cluster":
            
            existWordCount = argDict["userCentroids"] != None
            existClusterCount = argDict["clusterCount"] != None
            noWindow = argDict["window"] == None

            if (existWordCount and existClusterCount) or noWindow:
                raise Exception(MODE_CLUSTER_ERROR)



