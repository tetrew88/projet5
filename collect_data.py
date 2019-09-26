#!/usr/bin/python3

import requests
import mysql.connector

from classes.product import *


host = "localhost"
user = "donovan"
password = "doni88650"
database = "OpenFoodFact"


categories_list = ['Snacks', 'Boissons', 'Viandes', 'Desserts', 'Sauces', 'Riz']
result = []

url = ""

#connection to the database
connection = mysql.connector.connect(
        host=host, user=user, password = password, database = database)

cursor = connection.cursor()


for category in categories_list:
    url = "https://fr.openfoodfacts.org/cgi/search.pl?categories={}&action=process&page_size=1000&json=1".format(category)

    result = requests.get(url)
    result = json.loads(result.text)

    result = result['products']

    for product in result:
        data = Product()
        
        if data.collect_data(product, category):
            if data.name != "NULL":
                data.save_data(cursor, connection)

cursor.close()
connection.close()


print("collect finised")
