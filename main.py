#!/usr/bin/python3

import function
import mysql.connector
import sys

from classes.category import *
from classes.product import *
from classes.favorite import *

#identifiant for connection to the database
host = "localhost"
user = "****"
password = "****"
database = "OpenFoodFact"


menu_choice = 0

continuer = True

#connection to the database
connection = mysql.connector.connect(
        host=host,user=user, password = password, database = database)

cursor = connection.cursor()


function.clean_screen()

#main loop
while continuer:
    menu_choice = 0
    function.clean_screen()

    #main menu
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

    #if the user want substitute a product
    if menu_choice == 1:

        #the user choose an category
        category_choice = Category.select_a_category(cursor)

        #if any category was fund
        if category_choice == False:
            print("Any data")
        #else
        else:
            #the user choice a product ti substitute
            product_choice = Product.select_a_product(cursor, category_choice)
            
            #if any product was fund
            if product_choice == False:
                print("Any data")
            #else
            else:
                #searched many substitute for the product selected by the user
                substitute_list = product_choice.find_substitute(cursor)

                #the user select a substitute
                substitute = Product.select_a_substitute(substitute_list)

                #display the information of the substitute
                substitute.display()

                #ask to the user if he want save the substitute
                substitute.save_substitute(cursor, connection, product_choice)

    #if the user want show his substitute
    elif menu_choice == 2:
        #collect the favorites to the databse
        favorites_list = Favorite.collecte_favorites_from_database(cursor)
        #display the favorites
        Favorite.display_favorites(favorites_list)
    
    #if the user want quit the program
    else:
        quit()
