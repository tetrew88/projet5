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
            category = "", list_of_store = []):


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



    def collect_data(self, data, product_category):
        """method for collect the data from openfoodfact"""
        
        #collecte data in the main class
        self.name = function.collect_data_in_json_dictionnary(
                data, 'product_name')

        if self.name == 'NULL':
            return False
        
        self.url = function.collect_data_in_json_dictionnary(data, 'url')
        
        self.brand = function.collect_data_in_json_dictionnary(data,'brands')

        self.ingredients = function.collect_data_in_json_dictionnary(
                data, 'ingredients_text')

        self.labels = function.collect_data_in_json_dictionnary(data, 'labels')

        self.saturated_fat = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'saturated-fat')

        self.fat = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'fat')

        self.salt = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'salt')

        self.sugar = function.collect_data_in_json_dictionnary(
                data, 'nutrient_levels', 'sugars')        

        self.allergens = function.collect_data_in_json_dictionnary(
                data, 'ingredients_text_with_allergens')
            
        self.nutriscore = function.collect_data_in_json_dictionnary(
                data, 'nutriments', 'nutrition-score-fr')

        if self.nutriscore == 'NULL':
            return False


        self.category = Category(product_category)


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


            for store_data in self.stores:
                store_data.save_data(cursor, connexion)


            association = (self.category.id_number, self.id_number)
            
            cursor.execute("INSERT INTO Association_product_category\
                    (pfk_category_id, pfk_product_id)\
                    VALUES (%s, %s)", association)

            connexion.commit()
            
       
            for stores in self.stores:
                if stores.id_number != 0:
                    association = (stores.id_number, self.id_number)

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
        list_of_product = []


        try:
            cursor.execute("SELECT * FROM Product WHERE id IN\
                    (SELECT pfk_product_id FROM Association_product_category\
                    WHERE pfk_category_id = {})".format(category.id_number))

        except:
            return False

        list_of_product = cursor.fetchall()

        if len(list_of_product) > 0:
            
            while user_choice < 1 or user_choice > len(list_of_product) + 1:
                print("Choix du produit\n\n")
                
                x=0
                for product_data in list_of_product:
                    print("{}: {}".format(x+1, product_data[2]))
                    x+=1

                user_choice = input("\nEntrer votre hoix: ")
                
                try:
                    user_choice = int(user_choice)
                except:
                    user_choice = 0

                function.clean_screen()


        cursor.execute("SELECT * FROM Product WHERE id = {}".format(
            list_of_product[user_choice - 1][0]))
        
        data = cursor.fetchall()[0]

        return Product(data[0], data[1],  data[2], data[3],
                        data[4], data[5], data[6], data[7], data[8],
                        data[9], data[10], data[11], category)



    def find_substitute(self, cursor):
        response = list_of_substitute = list_of_store = []

        cursor.execute("SELECT * FROM Product WHERE id IN\
                (SELECT pfk_product_id FROM Association_product_category\
                WHERE pfk_category_id = {})".format(self.category.id_number))

        product_response = cursor.fetchall()


        for data in product_response:
            cursor.execute("SELECT * FROM Store\
                    WHERE id IN (SELECT pfk_store_id\
                    FROM Association_product_store\
                    WHERE pfk_product_id = {})".format(data[0]))

            store_response = cursor.fetchall()

                        
            for store_data in store_response:
                list_of_store.append(Store(store_data[0], store_data[1],
                    store_data[2]))
            print(list_of_substitute)

            substitute = Product(data[0], data[1],  data[2], data[3], 
                    data[4], data[5], data[6], data[7], data[8],
                    data[9], data[10], data[11],
                    self.category, 
                    list_of_store)


            if substitute.nutriscore >= self.nutriscore and\
                    substitute.id_number != self.id_number:
                        list_of_substitute.append(substitute)



        return list_of_substitute



    def select_a_substitute(substitute_list):
        user_choice = 0
      
        while user_choice < 1 or user_choise > len(substitute_list) + 1:
            print("Choix du substitut\n\n")
            
            x = 0
            for substitute in substitute_list:
                print("{}: {}".format(x+1, substitute.name))
                x+=1

            user_choice = input("\nEntrer votre choix: ")
            function.clean_screen()


            try:
                user_choice = int(user_choice)
            except:
                user_choice = 0

        user_choice = substitute_list[user_choice - 1]

        return user_choice


    def display(self):
        function.clean_screen()

        print("Nom: " + self.name)
        print("Url: " + self.url)
        print("\nMarque: " + self.brand)
        print("Ingrédient: " + self.ingredients)
        print("Labels: " + self.labels)
        print("Graisse saturé: " + self.saturated_fat)
        print("Graisse: " + self.fat)
        print("Sel: " + self.salt)
        print("Sucre: " + self.sugar)
        print("Allergène: " + self.allergens)
        print("Nutriscore: " + str(self.nutriscore))

        print("\n\ncatégorie:")
        self.category.display()
        
        print("\n\nPoint de vente:")
        print(self.stores)

