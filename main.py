#!/usr/bin/python3

import function
import mysql.connector
import sys

from classes.category import *
from classes.product import *
from classes.favorite import *


host = "localhost"
user = "donovan"
password = "doni88650"
database = "OpenFoodFact"


menu_choice = 0

continuer = True

#connection to the database
connection = mysql.connector.connect(
        host=host,user=user, password = password, database = database)

cursor = connection.cursor()


function.clean_screen()

while continuer:
    menu_choice = 0
    function.clean_screen()

    while menu_choice < 1 or menu_choice > 3:
        print("Menu:\n\n")
        print("1.Quel aliment souhaitez-vous remplacer ?\n")
        print("2.Retrouver mes aliments substitués\n")
        print("3.Quitter\n\n")

        menu_choice = input("Entrer votre choix: ")
        function.clean_screen()

        try:
            menu_choice = int(menu_choice)
        except:
            menu_choice = 0


    if menu_choice == 1:
        category_choice = Category.select_a_category(cursor)
        if category_choice == False:
            print("Any data")
        else:
            product_choice = Product.select_a_product(cursor, category_choice)
            if product_choice == False:
                print("Any data")
            else:
                substitute_list = product_choice.find_substitute(cursor)

                substitute = Product.select_a_substitute(substitute_list)

                substitute.display()

                substitute.save_substitute(cursor, connection, product_choice)

    elif menu_choice == 2:
        favorites_list = Favorite.collecte_favorites_from_database(cursor)
        Favorite.display_favorites(favorites_list)

    else:
        quit()
