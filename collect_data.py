#!/usr/bin/python3

from classes.product import *

main_reference = 1
reference2 = 2

match_references = []

category_match = False

main_product_counter = same_category_counter = 0

while main_product_counter < 20:
    main_product = Product(str(main_reference))
   
    if main_product.collect_data() == True and \
            main_reference not in match_references:
        
        match_references.append(main_reference)

        reference2 = 7131
        same_category_counter = 1
        while same_category_counter < 5:
            product2 = Product(str(reference2))
            
            print("reference2: " + str(reference2))

            if product2.collect_data() == True:
                category_match = False
                #print("reference2: " + str(reference2))


                for category in main_product.list_of_category:
                    for category2 in product2.list_of_category:
                        if category.name == category2.name:
                            category_match = True
                            break

                    if category_match == True:
                        match_references.append(reference2)
                        same_category_counter += 1
                        print("y = " + str(same_category_counter))
                        break

            reference2 += 1
            
                        
    main_reference += 1
