#!/usr/bin/python3

from classes.store import *
from classes.category import *
from classes.store import *

import json

import database_function
import function


class Product:
    """class designed a product by:
	-his reference
	-his name
	-his brand
	-his ingredient
	-his label
	-his saturated fat
	-his fat
	-his salt
	-his sugar
	-his allergen
        -his nutriscore
	-his url
        
        -his category
        -the store where his sale"""



    def __init__(self, identifiant = 0, url = "", name = "", brand = "", 
            ingredients = "", labels = "", saturated_fat = "", fat = "", 
            salt = "", sugar = "", allergens = "", nutriscore = 0, 
            category = "", list_of_store = ""):

        self.id_number = identifiant
        self.url = url
        self.name = name
        self.brand = brand
        self.ingredients = ingredients
        self.labels = labels
        self.saturated_fat = saturated_fat
        self.fat = fat
        self.salt = salt
        self.sugar = sugar
        self.allergens = allergens
        self.nutriscore = nutriscore

        self.category = category
        self.stores = list_of_store



    def collect_data(self, data):
        """method for collect the data from openfoodfact"""
        
        #collecte data in the main class
        self.name = function.collect_data_in_json_dictionnary(
                data, 'product_name')
        if self.name == False or self.name == 'NULL':
            return False
        
        self.url = function.collect_data_in_json_dictionnary(
                data, 'url')    
        if self.url == False:
            self.url = "NULL"

        self.brand = function.collect_data_in_json_dictionnary(data,'brands')
        if self.brand == False:
            self.brand = 'NULL'


        self.ingredients = function.collect_data_in_json_dictionnary(
                data, 'ingredients_text')
        if self.ingredients == False:
            self.ingredients = 'NULL'


        self.labels = function.collect_data_in_json_dictionnary(data, 'labels')
        if self.labels == False:
            self.labels = "NULL"


        self.saturated_fat = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'saturated-fat')
        
        if self.saturated_fat == False:
            saturated_fat = 'NULL'


        self.fat = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'fat')
        if self.fat == False:
            self.fat = 'NULL'


        self.salt = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'salt')
        if self.salt == False:
            self.salt = 'NULL'

        self.sugar = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'sugars')        
        if self.sugar == False:
            self.sugar = 'NULL'

        self.allergens = function.collect_data_in_json_dictionnary(
                data, 'ingredients_text_with_allergens')
        if self.allergens == False:
            self.allergens = 'NULL'
            
        self.nutriscore = function.collect_data_in_json_dictionnary(
                data, 'nutriments', 'nutrition-score-fr')
        if self.nutriscore == False or self.nutriscore == 'NULL':
            return False

        try:
            if data['purchase_places'] != "":
                purchase_places_list = []
                purchase_place_list = data['purchase_places'].split(",")
            else:
                purchase_places_list =  ["NULL"]

        except KeyError:
            purchase_places_list =  ["NULL"]

        try:
            if data['stores'] != "":
                stores_list = []
                stores_list = data['stores'].split(",")
            else:
                stores_list = ['NULL']
        
        except KeyError:
            stores_list = ['NULL']

        for purchase_places in purchase_places_list:
            for stores in stores_list:
                if purchase_places[0:1] == " ":
                    purchase_places = purchase_places[1:len(purchase_places)]

                if stores[0:1] == " ":
                    stores = stores[1:len(stores)]

                self.stores.append(Store(purchase_places, stores))

        return True


    def save_data(self, cursor, connexion):
        product_id = 0
        category_id = []
        stores_id = []

        response = database_function.check_existence_in_database(cursor,
                "Product",
                "name",
                self.name)
        
        if response == False:
            product = (self.url, self.name, self.brand, 
                    self.ingredients, self.labels, self.saturated_fat,
                    self.fat, self.salt, self.sugar, self.allergens,
                    self.nutriscore)


            cursor.execute("INSERT INTO Product(url, name, brand,\
                    ingredients, labels, saturated_fat, fat,\
                    salt, sugar, allergens, nutriscore)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    product)
            
            connexion.commit()
            self.id_number = cursor.lastrowid


            self.category.save_data(cursor, connexion)


            for store in self.stores:
                store.save_data(cursor, connexion)


            association = (self.category.id_number, self.id_number)
            
            cursor.execute("INSERT INTO Association_product_category\
                    (pfk_category_id, pfk_product_id)\
                    VALUES (%s, %s)", association)
            connexion.commit()
            

            if len(stores_id) > 0:       
                for store in selfs.stores:
                    association = (store.id_number, self.id_number)

                    cursor.execute("INSERT INTO Association_product_store\
                            (pfk_store_id, pfk_product_id)\
                            VALUES (%s, %s)", association)
                    connexion.commit()

            
            print("product {} added to the database\n".format(self.name))


        else:
            return False


    def select_a_product(cursor, category):
        """méthode used by user for select a product"""

        user_choice = 0
        response = database = list_of_product = []


        cursor.execute("SELECT * FROM Product WHERE id IN\
                (SELECT pfk_product_id FROM Association_product_category\
                WHERE pfk_category_id = {})".format(category.id_number))

        database = cursor.fetchall()
        print(database)

        if len(database) > 0:
            for response in database:
                list_of_product.append(response[0])

            while user_choice not in list_of_product:
                function.clean_screen()

                print("Choix du produit\n\n")

                for data in database:
                    print("{}: {}\n".format(data[0], data[2]))

                user_choice = input("\nEntrer votre choix: ")

                try:
                    user_choice = int(user_choice)
                except:
                    user_choice = 0

        else:
            return False

        cursor.execute("SELECT * FROM Product WHERE id = {}".format(
            user_choice))
        
        data = cursor.fetchall()[0]

        return Product(data[0], data[1],  data[2], data[3],
                        data[4], data[5], data[6], data[7], data[8],
                        data[9], data[10], data[11], category)


    def find_a_substitute(self, cursor):
        response = list_of_substitute = list_of_store = []

        cursor.execute("SELECT * FROM Product WHERE id IN\
                (SELECT pfk_product_id FROM Association_product_category\
                WHERE pfk_category_id = {})".format(self.category.id_number))

        response = cursor.fetchall()

        for data in response:
            if data[0] != self.id_number and data[11] > self.nutriscore:
                cursor.execute("SELECT pfk_store_id\
                        FROM Association_product_store\
                        WHERE pfk_product_id = {}".format(self.id_number))

                response = cursor.fetchall()

                for element in response:
                    cursor.execute("SELECT * FROM Store\
                        WHERE id IN (SELECT pfk_store_id\
                        FROM Association_product_store\
                        WHERE pfk_product_id = {}".format(self.id_number))
                        
                    list_of_store.append(Store(element[0], element[1],
                        element[2]))

                list_of_substitute.append(
                    Product(data[0], data[1],  data[2], data[3], 
                        data[4], data[5], data[6], data[7], data[8],
                        data[9], data[10], data[11],
                        self.category, 
                        list_of_store))

        return list_of_substitute
