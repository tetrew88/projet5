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
	

    def __init__(self, login):
        self.login = login
        self.url = 'https://fr.openfoodfacts.org/api/v0/produit/'+login+'.json'
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
        pass
