#!/usr/bin/python3

import function
import mysql.connector

from classes.category import *
from classes.product import *

host = "localhost"
user = "donovan"
password = "doni88650"
database = "OpenFoodFact"


menu_choice = 0

#connection to the database
connection = mysql.connector.connect(
        host=host,user=user, password = password, database = database)

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
    category_choice = Category.select_a_category(cursor)
    if category_choice == False:
        print("Any data")
    else:
        product_choice = Product.select_a_product(cursor, category_choice)
        if product_choice == False:
            print("Any data")
        else:
            Product.find_a_substitute(cursor, category_choice, product_choice)

elif menu_choice == 2:
    pass

else:
    quit()
