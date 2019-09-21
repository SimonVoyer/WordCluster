# -*- coding: utf-8 -*-
'''
--------------
 Constant.py
--------------
'''
'''----------------------------------------------------------------
--> for algo.py '''
STOPLIST_PATH = "stopList.txt"

'''----------------------------------------------------------------
--> for commandParser.py '''
MODE_ERROR_MSG_1 = "On ne peut pas être en mode entraînement (-e) et en mode recherche de synonyme (-r) simultanément."
MODE_ERROR_MSG_2 = "Il faut obligatoirement choisir un mode, soit entraînement (-e), soit recherche de synonyme (-r)."
MODE_CLUSTER_ERROR = "En mode cluster, il faut obligatoirement un nombre de mots à afficher, un nombre de clusters et une taille de fenêtre."
MODE_ERROR_MSG_CUSTOM_CLUSTER = "Erreur: il faut soit fournir une liste de mots, soit fournir un nb de centroïdes"
ENCODING_ERROR_MSG = "En mode entraînement, il faut obligatoirement choisir un encodage avec la commande --enc."
PATH_ERROR_MSG = "En mode entraînement, il faut définir au moins un chemin vers un texte (--chemin)."
WINDOW_SIZE_ERROR_MSG = "Il faut définir une taille de fenêtre plus grande que 0 avec la commande -t."

'''----------------------------------------------------------------
--> for Controller.py '''
ASK_FOR_SEARCH_OPTIONS = "\n Entrez le mot à chercher, le nombre de résultats à afficher et la méthode.\n 1=produit scalaire, 2=least squares, 3=city-block\n Appuyez sur 'q' pour quitter.\n"
METHOD_ERROR_MSG_3 = "\n Le numéro de la méthode est invalide.\n"
NB_OF_RESULTS_ERROR_MSG = "\n Veuillez entrer un nombre de résultats inférieur ou égal à 100.\n"
KEY_ERROR_MSG = "\n Le mot choisi n'est pas contenu dans le ou les texte(s).\n"
INDEX_ERROR_MSG = "\nValeur(s) erronée(s)."

'''----------------------------------------------------------------
--> for OracleDAO.py '''
IDENTIFICATION = 'e0980234/BBBbbb222@'
HOST = 'delta'
PORT = 1521
SID = 'decinfo'
CREATE_WORDS ="CREATE TABLE IF NOT EXISTS words (word_index INT PRIMARY KEY, word TEXT)"
CREATE_MATRIX = """CREATE TABLE IF NOT EXISTS matrix ( line_index INT, column_index INT, window_size INT, score INT, 
                CONSTRAINT pk_matrix PRIMARY KEY (line_index, column_index, window_size), 
                FOREIGN KEY(line_index) REFERENCES words(word_index),
                FOREIGN KEY(column_index) REFERENCES words(word_index))"""
DROP_WORDS = "DROP TABLE words"
DROP_MATRIX = "DROP TABLE matrix"
INSERT_DICTIONARY = "INSERT INTO words VALUES (:1, :2)"
INSERT_MATRIX = "INSERT INTO matrix VALUES (:1, :2, :3, :4)"
SELECT_DICTIONARY = "SELECT word_index, word FROM words"
SELECT_VERIFY_DICTIONARY = "SELECT COUNT(word_index) FROM words WHERE word_index = :1"
SELECT_ALL_MATRIX_2 = "SELECT line_index, column_index, score FROM matrix WHERE window_size = :1"
SELECT_MATRIX = "SELECT COUNT(*) FROM matrix WHERE line_index = :1 AND column_index =:2 AND window_size = :3"
SELECT_SCORE = "SELECT score FROM matrix WHERE line_index = :1 AND column_index =:2 AND window_size = :3"
SELECT_ALL_MATRIX = "SELECT * FROM matrix"
SELECT_ALL_SCORE_MATRIX = "SELECT score FROM matrix"
LINE_INDEX = 0
COLUMN_INDEX = 1
INDEX = 0
WORD = 1
SCORE = 2
UPDATE_MATRIX = "UPDATE matrix SET score = :1 WHERE line_index = :2 AND column_index = :3 AND window_size = :4"



