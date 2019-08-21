#!/usr/bin/python3

import function
import mysql.connector

from classes.category import *


menu_choice = 0

print("Bienvenu dans eatBetter")

#connection to the database
connection = mysql.connector.connect(
        host="localhost",
        user="donovan", password = "doni88650",
        database = "OpenFoodFact")

cursor = connection.cursor()


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
    Category.select_a_category(cursor)
    pass

elif menu_choice == 2:
    pass

else:
    quit()
