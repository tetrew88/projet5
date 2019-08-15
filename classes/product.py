#!/usr/bin/python3

import requests
import json
import mysql.connector

from classes.store import *
from classes.category import *
from classes.store import *

class Product:
    """class designed a product by:
	-his login
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
        self.url = 'https://fr.openfoodfacts.org/api/v0/produit/'+reference+'.json'
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
        
        data = requests.get(self.url)
        data = json.loads(data.text)

        if data['status_verbose'] == 'product not found':
            return False

        data = data['product']

        try:
            try:
                self.name = data['product_name_fr']
            except KeyError:
                self.name = data['product_name']

            self.brand = data['brands']
            
            try:
                self.ingredients = data['ingredients_text_fr']
            except KeyError:
                self.ingredients = data['ingredients_text']
            
            self.labels = data['labels']
            self.satured_fat = data['nutrient_levels']['saturated-fat']
            self.fat = data['nutrient_levels']['fat']
            self.salt = data['nutrient_levels']['salt']
            self.sugar = data['nutrient_levels']['sugars']
            self.allergens = data['ingredients_text_with_allergens']
            self.nutriscore = data['nutriments']['nutrition-score-fr']


            for category in data['categories'].split(','):
                if category[0] == " ":
                    category = category[1:]

                self.list_of_category.append(Category(category))


            for purchase_place in data['purchase_places'].split(','):
                for store in data['stores'].split(','):
                    self.list_of_store.append(Store(purchase_place, store))

        except KeyError:
            return False

        return True


    def save_data(self):
        product_id = 0
        categories_id = []
        stores_id = []

        connection = mysql.connector.connect(
                host="localhost", 
                user="donovan", password = "doni88650",
                database = "OpenFoodFact")

        cursor = connection.cursor()
        
        print("connection a la base de donnée éffectuer\n")

        product = (self.reference, self.url, self.name, self.brand, 
                self.ingredients, self.labels, self.saturated_fat,
                self.fat, self.salt, self.sugar, self.allergens, self.nutriscore
                )
        
        product_insertion = "INSERT INTO Product(reference, url, name,brand,\
                        ingredients,labels, saturated_fat, fat,salt,sugar,\
                        allergens, nutriscore)\
                        VALUES\
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        cursor.execute(product_insertion, product)

        product_id = cursor.lastrowid

        for element in self.list_of_category:
            category = (element.name, element.url)

            cursor.execute("""INSERT INTO Categories (name, url)\
                    VALUES (%s, %s)""", category)
            
            categories_id.append(cursor.lastrowid)

        for element in self.list_of_store:
            store = (element.name, element.localisation)
            
            cursor.execute("""INSERT INTO Store (name, localisation)\
                    VALUES (%s, %s)""", store)

            stores_id.append(cursor.lastrowid)


        for category_id in categories_id:
            association = (category_id, product_id)

            cursor.execute("""INSERT INTO Association_product_category\
                    (pfk_category_id, pfk_product_id)\
                    VALUES (%s, %s)""", association)

        for store_id in stores_id:
            association = (store_id, product_id)

            cursor.execute("""INSERT INTO Association_product_store\
                    (pfk_store_id, pfk_product_id)\
                    VALUES (%s, %s)""", association)

        connection.commit()
        cursor.close()
        connection.close()


        print("product {} added to the database\n".format(self.name))
