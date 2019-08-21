#!/usr/bin/python3

import requests
import json

from classes.store import *
from classes.category import *
from classes.store import *

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
        self.url = 'https://fr.openfoodfacts.org/api/v0/produit/'+\
                reference+'.json'

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


        #collecte au data in the main class 
        try:
            #try to find name in french primaly
            try:
                self.name = data['product_name_fr']
            #else collect general product name
            except KeyError:
                self.name = data['product_name']


            if data['brands'] == "":
                self.brand = "NULL"
            else:
                self.brand = data['brands']
            

            #try to collect ingredient in french primaly
            try:
                if data['ingredients_text_fr'] == "":
                    self.ingredients = "NULL"
                else:
                    self.ingredients = data['ingredients_text_fr']

            #else collecte general ingredients
            except KeyError:
                if data['ingredients_text'] == "":
                    self.ingredients = "NULL"
                else:
                    self.ingredients = data['ingredients_text']
           

            if data['labels'] == '':
                self.labels = "NULL"
            else:
                self.labels = data['labels']
            
            if data['nutrient_levels']['saturated-fat'] == "":
                self.saturated_fat = "NULL"
            else:
                self.satured_fat = data['nutrient_levels']['saturated-fat']
            
            if data['nutrient_levels']['fat'] == "":
                self.fat = "NULL"
            else:
                self.fat = data['nutrient_levels']['fat']

            if data['nutrient_levels']['salt'] == "":
                self.salt = "NULL"
            else:
                self.salt = data['nutrient_levels']['salt']
            
            if data['nutrient_levels']['sugars'] == '':
                self.sugar = 'NULL'
            else:
                self.sugar = data['nutrient_levels']['sugars']
            
            if data['ingredients_text_with_allergens'] == '':
                self.allergens = "NULL"
            else:
                self.allergens = data['ingredients_text_with_allergens']
            
            if data['nutriments']['nutrition-score-fr'] == '':
                return False
            else:
                self.nutriscore = data['nutriments']['nutrition-score-fr']

            
            #for each category in categories
            for category in data['categories'].split(','):
                #check if the first element of the string was ' '
                if category[0] == " ":
                    #if it was, delete the first element
                    category = category[1:]

                #add each category to the list_of_category
                self.list_of_category.append(Category(category))

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

        print("Add {} to the database\n".format(self.name))

        cmd_sql = "SELECT * FROM Product WHERE reference = " + self.reference

        cursor.execute(cmd_sql)

        reponse = cursor.fetchall()
        if len(reponse) == 0:
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
                if category.save_data(cursor) == True:
                    categories_id.append(cursor.lastrowid)

            for store in self.list_of_store:
                if store.save_data(cursor) == True:
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
            print('data already in database')


    def select_product(cursor):
        """méthode used by user for select a product"""

        user_choice = 0
        list_of_id= []

        cmd_sql = "SELECT * FROM Product"
        cursor.execute(cmd_sql)

        database = cursor.fetchall()


        for data in database:
            list_of_id.append(data[0])


        while user_choice not in list_of_id:
            print("Choix du produit\n\n")

            for data in database:
                print("{}: {}".format(data[0], data[1]))

            user_choice = input("\nEntrer votre choix: ")
            function.clean_screen()

            try:
                user_choice = int(user_choice)
            except:
                user_choice = 0


        return user_choice
