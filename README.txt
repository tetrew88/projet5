Projet5

Excercice pour la formation dévellopeur d'application python sur openclassroom.

liens du site: https://openclassrooms.com/
liens de la formation: https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python
liens de l'excercice: https://openclassrooms.com/fr/projects/157/assignment

créateur:
  Maurice Donovan(tetrew88)
  
Avancé du projet:
  -Terminé

Langages utilisés:
  -Python
  -MySql
  
Librairies:
  -requests
  -mysqlConnector
  
 Description:
  Programme permettant dans un premier temp de récupérer différents produit allimentaire sur le site openfoodfact(https://fr.openfoodfacts.org) et les stockers dans une base de donnée MySql.
  L'utilisateur pourra enssuite utiliser le programme affin de trouver un substitut plus saint a un de ces alliment favori.
    
    
Classe composant le programme:
  -Produit
  -Catégorie
  -Magasin
  -Favori
  
  
Composition du projet:
  -collect_data.py: Script permettant de récuperer des aliments sur openfoodfact(100 par catégorie de produit) et les stocker dans une base de donnée mySql.
  
  -main.py: Script permettant a l'utilisateur de trouver un substitut plus saint a un de ses produit favori via divers menu de selection,
            l'utilisateur peut aussi enregistrer un substitut qui lui plait dans la base de donnée mySql affin de pouvoir le retrouver plus tard.
            
  -creation_off.sql: Script de création de la base de donnée.          
