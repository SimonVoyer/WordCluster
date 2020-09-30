
+=======================================================+					
|  Travail pratique 3					|
|  	par						|
|  		--> Hugo Bourcier			|
|  		--> Alexis Duval			|
|  		--> Simon Voyer-Poitras			|
+=======================================================+

------------------
Types d'arguments:
------------------

Modes:
-d: Mode "drop" -> pour détruire la base de données
-e: Mode entraînement -> pour insérer des données dans la base de données
-r: Mode recherche de cooccurrences -> pour questionner la base de données
-c: Mode recherche de type "clustering" -> pour faire des tests avec des centroïdes

Paramètres et options:
-t <int>: Taille de la fenêtre
--enc <String>: Encodage des fichiers textes (utf-8)
--chemin <String, [String,...]>: Chemin et nom du/des fichier(s) à analyser
--verbose: La durée de chaque étape sera affichée à l'écran

Options pour les clusters:
-n <int>: Nombre de mots à afficher par cluster
--nc <int>: Nombre de centroïdes qui seront dans l'algorithme
--mots: Les centroïdes seront des mots définis par l'utilisateur

---------
Exemples:
---------

[1.]
-> Exemple de réinitialisation:
main.py -d
-> La base de données sera détruite

[2.]
-> Exemple d'entraînement:
main.py -e -t 5 --chemin d:/texte1.txt --enc utf-8
-> Fenêtre de 5 mots
-> Un fichier txt à lire
-> Encodage utf-8
-> Les résultats seront insérés dans la base de données
-> NOTE: "-t", "--chemin" et "--enc" sont OBLIGATOIRES

[3.]
-> Exemple d'entraînement:
main.py -e -t 5 --chemin d:/texte1.txt --enc utf-8 --verbose
-> Fenêtre de 5 mots
-> Un fichier txt à lire
-> Encodage utf-8
-> Option VERBOSE
-> Les résultats seront insérés dans la base de données
-> La durée de chaque étape sera affichée
-> NOTE: "-t", "--chemin" et "--enc" sont OBLIGATOIRES

[4.]
-> Exemple d'entraînement:
main.py -e -t 7 --chemin d:/texte1.txt d:/texte2.txt --enc utf-8
-> Fenêtre de 7 mots
-> Deux fichiers txt à lire
-> Encodage utf-8
-> Les résultats seront insérés dans la base de données
-> NOTE: "-t", "--chemin" et "--enc" sont OBLIGATOIRES

[5.]
-> Exemple d'une recherche de coocurrences:
main.py -r -t 7
-> Concerne seulement les données qui avaient été insérées avec une fenêtre de 7
-> Il y aura des options à l'écran pour que l'usager puisse intéragir avec le logiciel
-> NOTE: "-t" est OBLIGATOIRE afin de trouver les données adéquates dans le contexte

[6.]
-> Exemple d'une recherche de type "clustering":
main.py -c -t 7 -n 10
-> Concerne seulement les données qui avaient été insérées avec une fenêtre de 7
-> Les résultats seront affichés à l'écran
-> Dans ce cas-ci, il y aura 10 centroïdes (valeur par défaut) initialisés aléatoirement
-> NOTE: "-t" est OBLIGATOIRE afin de trouver les données adéquates dans le contexte
-> NOTE: "-n" est OBLIGATOIRE afin de pouvoir afficher un résultat final

[7.]
-> Exemple d'une recherche de type "clustering":
main.py -c -t 7 -n 10 --nc 20
-> Concerne seulement les données qui avaient été insérées avec une fenêtre de 7
-> Les résultats seront affichés à l'écran
-> Dans ce cas-ci, il y aura 20 centroïdes (valeur choisie par l'usager) initialisés aléatoirement
-> NOTE: "-t" est OBLIGATOIRE afin de trouver les données adéquates dans le contexte
-> NOTE: "-n" est OBLIGATOIRE afin de pouvoir afficher un résultat final

[8.]
-> Exemple d'une recherche de type "clustering":
main.py -c -t 7 -n 10 --mots four patate tomate carotte poulet bouillon
-> Concerne seulement les données qui avaient été insérées avec une fenêtre de 7
-> Les résultats seront affichés à l'écran
-> Dans ce cas-ci, il y aura 6 centroïdes, c'est-à-dire les 6 mots choisis par l'usager
-> NOTE: "-t" est OBLIGATOIRE afin de trouver les données adéquates dans le contexte
-> NOTE: "-n" est OBLIGATOIRE afin de pouvoir afficher un résultat final













		
