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


            for stores in self.stores:
                stores.save_data(cursor, connexion)


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


    def collect_product_from_database(cursor, column = "NULL", value = "NULL"):
        if column != "NULL" and value != "NULL":
            try:
                cursor.execute('SELECT * FROM Product WHERE {} = {}'.format(
                    column, value))
            except:
                print("\nprobleme lors de la recuperation du produit\n")
                return False

            list_of_data = cursor.fetchall()

            #load product
            x = 0
            if len(list_of_data) > 0:
                for data in list_of_data:
                    product = Product(data[0], data[1], data[2], data[3], 
                            data[4], data[5], data[6], data[7], data[8], 
                            data[9], data[10],data[11], Category("", "") , [])

                #load category data
                try:
                    cursor.execute('SELECT * FROM Categories WHERE id =\
                            (SELECT pfk_category_id FROM\
                            Association_product_category\
                            WHERE pfk_product_id = {})'.format(
                                product.id_number))

                    category = cursor.fetchall()[0]
                except:
                    print("\nprobleme lors de la récupération de la\
                            categorie\n")
                    return False

                if len(category) > 0:
                    product.category = Category(category[1], category[2])
                    product.category.id_number = category[0]
                else:
                    print("\naucune category trouver pour ce produit\n")
                    return False


                #load store data
                store_list = []
                try:
                    cursor.execute('SELECT * FROM Store\
                            WHERE id IN (SELECT pfk_store_id\
                            FROM Association_product_store\
                            WHERE pfk_product_id = {})'.format(
                                product.id_number))
                    store_list = cursor.fetchall()

                except:
                    print("\nerreur lors de la récuperation des point de vente\
                            du produit\n")
                    return False

                if len(store_list) > 0:
                    for store in store_list:
                        product.stores.append(Store(store[2], store[1], store[0]
                            ))

                else:
                    product.stores.append(Store("NULL", "NULL", 0))

        else:
            print("\nproduit introuvable\n")
            return False

        return product




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
                for product in list_of_product:
                    print("{}: {}".format(x+1, product[2]))
                    x+=1

                user_choice = input("\nEntrer votre hoix: ")
                
                try:
                    user_choice = int(user_choice)
                except:
                    user_choice = 0

                function.clean_screen()


        product_choice = Product.collect_product_from_database(cursor,
                    'id', list_of_product[user_choice - 1][0])

        return product_choice



    def find_substitute(self, cursor):
        list_of_id = list_of_substitute = []

        cursor.execute("SELECT id FROM Product WHERE id IN\
                (SELECT pfk_product_id FROM Association_product_category\
                WHERE pfk_category_id = {})".format(self.category.id_number))

        list_of_id = cursor.fetchall()


        for id_number in list_of_id:
            substitute = Product.collect_product_from_database(cursor,
                    'id', id_number[0])


            if substitute.nutriscore >= self.nutriscore and\
                    substitute.id_number != self.id_number:
                        list_of_substitute.append(substitute)


        return list_of_substitute



    def select_a_substitute(substitute_list):
        user_choice = 0
      
        while user_choice < 1 or user_choice > len(substitute_list) + 1:
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

        print("Nom: " + str(self.name))
        print("Url: " + str(self.url))
        print("\nMarque: " + str(self.brand))
        print("Ingrédient: " + str(self.ingredients))
        print("Labels: " + str(self.labels))
        print("Graisse saturé: " + str(self.saturated_fat))
        print("Graisse: " + str(self.fat))
        print("Sel: " + str(self.salt))
        print("Sucre: " + str(self.sugar))
        
        print("\nAllergène: " + str(self.allergens))
        
        print("\nNutriscore: " + str(self.nutriscore))

        print("\n\ncatégorie:")
        self.category.display()
        
        print("\n\nPoint de vente:")
        for store in self.stores:
            store.display()
            print("\n")


    def save_substitute(self, cursor, connection, product):
        user_choice = 0
        association = (product.id_number, self.id_number)

        while user_choice < 1 or user_choice > 2:
            print("voulez vous enregistrer le substitut ?\n")
            print("1.Oui")
            print("2.Non\n")

            user_choice = input("Entrer votre choix: ")

            try:
                user_choice = int(user_choice)
            except:
                user_choice = 0
        
        if user_choice == 1:
            response = database_function.check_existence_in_database(cursor,
                "Favorites",
                "pfk_product_id",
                product.id_number)

            response2 = database_function.check_existence_in_database(cursor,
                "Favorites",
                "pfk_substitute_id",
                self.id_number)

            if response == False or response2 == False:
                try:
                    cursor.execute("INSERT INTO Favorites\
                            (pfk_product_id, pfk_substitute_id)\
                            VALUES (%s, %s)", association)
                    connection.commit()
                    print("\nFavori ajouter avec succes\n")
            
                except:
                    print("\nErreur lors de l'enregistrement\n")
                    return False

            else:
                print("\nLe favori existe déja\n")

