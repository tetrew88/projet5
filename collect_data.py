#!/usr/bin/python3

from classes.product import *
import mysql.connector

host = "localhost"
user = "donovan"
password = "doni88650"
database = "OpenFoodFact"


main_product_counter = same_category_counter = 0
main_reference = reference2 = 1

match_references = []

category_match = False


#connection to the database
connection = mysql.connector.connect(
        host=host, user=user, password = password, database = database)

cursor = connection.cursor()


#main loop(collect 20 product in off database)
while main_product_counter < 20:
    main_product = Product(str(main_reference))
   
    #collecte data of main product
    if main_product.collect_data() == True and\
            main_reference not in match_references:
        
        #add the reference product's in list match_references
        match_references.append(main_reference)

        #save data of the main product in database
        main_product.save_data(cursor)
        connection.commit()
        

        #searched product with less than one category in common 
        #with the main product
        reference2 = 1
        same_category_counter = 1
        
        while same_category_counter < 5:
            product2 = Product(str(reference2))
            print(reference2)

            #collect data of the product2
            if product2.collect_data() == True and\
                    reference2 not in match_references:
                
                category_match = False

                #search a same category in main_product's categories an product2                    categories
                for category in main_product.list_of_category:
                    for category2 in product2.list_of_category:
                        if category2.name == category.name:
                            category_match = True
                            break

                    if category_match == True:
                        #add the reference2 to match_reference list
                        match_references.append(reference2)
                        
                        #save the data of product2
                        product2.save_data(cursor)
                        connection.commit()

                        same_category_counter += 1
                        main_product_counter += 1
                        
                        #quit list path 
                        break

            reference2 += 1                   
    main_reference += 1
    
    print("nombre de produit ajouter: {}\n".format(main_product_counter))

#close connection to the database
cursor.close()
connection.close()


print("collect finished")
