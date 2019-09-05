#!/usr/bin/python3

import requests
import json

from classes.store import *
from classes.category import *
from classes.store import *

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



    def __init__(self, reference):
        self.reference = reference
        self.url = 'https://fr.openfoodfacts.org/api/v0/produit/{}.json'.format(
                self.reference)

        self.name = ""
        self.brand = ""
        self.ingredients = ""
        self.labels = ""
        self.saturated_fat = ""
        self.fat = ""
        self.salt = ""
        self.sugar = ""
        self.allergens = ""
        self.nutriscore = ""

        self.list_of_category = []
        self.list_of_store = []



    def collect_data(self):
        """method for collect the data from openfoodfact"""
        
        #load data in a dictionnary
        data = requests.get(self.url)
        data = json.loads(data.text)

        #if the product was not found in off database
        if data['status_verbose'] == 'product not found':
            return False

        data = data['product']


        #collecte data in the main class
        self.name = function.collect_data_in_json_dictionnary(
                data, 'product_name_fr')

        if self.name == False or self.name == 'NULL':
            self.name = function.collect_data_in_json_dictionnary(
                    data, 'product_name')
            if self.name == False or self.name == 'NULL':
                return False
            

        self.brand = function.collect_data_in_json_dictionnary(
                data,'brands')
        
        if self.brand == False:
            self.brand = 'NULL'


        self.ingredients = function.collect_data_in_json_dictionnary(
                data, 'ingredients_text')

        if self.ingredients == False:
            self.ingredients = 'NULL'


        self.labels = function.collect_data_in_json_dictionnary(
                data, 'labels')

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
            self.nutriscore = function.collect_data_in_json_dictionnary(
                    data, 'nutriments', 'nutrition-score-uk')
            if self.nutriscore == False or self.nutriscore == 'NULL':
                return False

        try:
            #for each category in categories
            for category in data['categories'].split(','):
                #check if the first element of the string was ' '
                if category[0] == " ":
                    #if it was, delete the first element
                    category = category[1:]

                #add each category to the list_of_category
                self.list_of_category.append(Category(category))
        except KeyError:
            return False

        try:
            #collect all the data of the store and purchase place
            for store in data['stores'].split(','):
                if data['purchase_places'] == "":
                    self.list_of_store.append(Store("NULL", store))

                elif data['purchase_places'] != "" and store != "":
                    self.list_of_store.append(Store(data['purchase_places'], 
                        store))
                
                elif data['purchase_places'] != "" and store == "":
                    self.list_of_store.append(Store(data['purchase_places'],
                        "NULL"))
                
                elif data['purchase_places'] == "" and store == "":
                    self.list_of_store.append(Store("NULL" ,"NULL"))
        except KeyError:
            return False


        return True



    def save_data(self, cursor):
        product_id = 0
        categories_id = []
        stores_id = []

        response = database_function.check_existence_in_database(cursor,
                "Product",
                "name",
                self.name)
        
        if response == False:
            product = (self.reference, self.url, self.name, self.brand, 
                    self.ingredients, self.labels, self.saturated_fat,
                    self.fat, self.salt, self.sugar, self.allergens,
                    self.nutriscore)


            cursor.execute("INSERT INTO Product(reference, url, name,brand,\
                    ingredients,labels, saturated_fat, fat,\
                    salt,sugar, allergens, nutriscore)\
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    product)
            
            product_id = cursor.lastrowid


            for category in self.list_of_category:
                 category.save_data(cursor)
                 categories_id.append(cursor.lastrowid)


            for store in self.list_of_store:
                store.save_data(cursor)
                stores_id.append(cursor.lastrowid)


            if len(categories_id) > 0:
                for category_id in categories_id:
                    association = (category_id, product_id)

                    cursor.execute("INSERT INTO Association_product_category\
                            (pfk_category_id, pfk_product_id)\
                            VALUES (%s, %s)", association)
            

            if len(stores_id) > 0:       
                for store_id in stores_id:
                    association = (store_id, product_id)

                    cursor.execute("INSERT INTO Association_product_store\
                            (pfk_store_id, pfk_product_id)\
                            VALUES (%s, %s)", association)

            
            print("product {} added to the database\n".format(self.name))


        else:
            return False


    def select_a_product(cursor, category):
        """méthode used by user for select a product"""

        user_choice = 0
        list_of_id= []

        cmd_sql = "SELECT * FROM Product WHERE id = \
                (SELECT pfk_product_id\
                FROM Association_product_category\
                WHERE pfk_category_id = {})".format(category)

        cursor.execute(cmd_sql)

        database = cursor.fetchall()

        if len(database) > 0:
            for data in database:
                list_of_id.append(data[0])


            while user_choice not in list_of_id:
                print("Choix du produit\n\n")

                for data in database:
                    print("{}: {}".format(data[0], data[3]))

                user_choice = input("\nEntrer votre choix: ")
                function.clean_screen()

                try:
                    user_choice = int(user_choice)
                except:
                    user_choice = 0

        else:
            return False


        return user_choice


    def find_a_substitute(category, nutriscore):
        pass
