#!/usr/bin/python3

from classes.product import *

main_reference = reference2 = 1

match_references = []

category_match = False

main_product_counter = same_category_counter = 0

#main loop
#collect 20 product of off database
while main_product_counter < 20:

    #create main product
    main_product = Product(str(main_reference))
   
    #collecte data of main product
    #if the collect of data is a succes and his reference is not already used
    if main_product.collect_data() == True and \
            main_reference not in match_references:
        
        #add the reference product's in list match_references
        match_references.append(main_reference)

        #save data of the main product in database
        main_product.save_data()

        
        reference2 = 7131
        same_category_counter = 1

        #search 4 product with at least once same category of main product
        while same_category_counter < 5:

            #create product2
            product2 = Product(str(reference2))
            
            #if the collect data of product2 is a succes and the product is not                 already used
            if product2.collect_data() == True and\
                    reference2 not in match_references:
                
                #booleen used to indicate if a category of the main product has                     been found
                category_match = False


                #search a same category in main_product's categories an product2                    categories
                for category in main_product.list_of_category:
                    for category2 in product2.list_of_category:
                        if category.name == category2.name:
                            category_match = True
                            break

                    #if a correspondence was fund
                    if category_match == True:

                        #add the reference to match_reference list
                        match_references.append(reference2)
                        
                        #save the data of product2
                        product2.save_data()

                        #add 1 to the counter of the loop same category and main                            counter loop
                        same_category_counter += 1
                        main_product_counter += 1

                        #quit list path 
                        break

            #add 1 to the reference2
            reference2 += 1

    #add 1 to the main_reference                    
    main_reference += 1
    
    print("nombre de produit ajouter: {}\n".format(main_product_counter))


print("collect finish")
