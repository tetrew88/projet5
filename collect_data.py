#!/usr/bin/python3

import requests
import mysql.connector

from classes.product import *


host = "localhost"
user = "****"
password = "****"
database = "OpenFoodFact"

#list of category for the collect of data
categories_list = ['Snacks', 'Boissons', 'Viandes', 'Desserts', 'Sauces', 'Riz']

result = []

url = ""

#connection to the database
connection = mysql.connector.connect(
        host=host, user=user, password = password, database = database)

cursor = connection.cursor()


#main loop
for category in categories_list:
    url = "https://fr.openfoodfacts.org/cgi/search.pl?categories={}&action=process&page_size=100&json=1".format(category)

    #request
    result = requests.get(url)
    result = json.loads(result.text)

    result = result['products']

    for product in result:
        data = Product()
        
        #filling of the class
        if data.collect_data(product, category):
            if data.name != "NULL":
                #save data in database
                data.save_data(cursor, connection)

#close the connection to the database
cursor.close()
connection.close()


print("collect finised")
