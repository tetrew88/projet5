from classes.product import *

class Favorite:
    """class designed a favorite by:
        -the main product
        -list of substitute of main product"""

    def __init__(self, id_number, main_product, substitute_list):
        self.in_number = id_number
        self.main_product = main_product
        self.substitute = substitute_list

    def collecte_favorites_from_database(cursor):
        favorites_list = []

        cursor.execute('SELECT * FROM Favorites')
        response = cursor.fetchall()

        for favorites in response:
            product = Product.collect_product_from_database(cursor, 'id', 
                    favorites[1])

            substitute = Product.collect_product_from_database(cursor, 'id',
                    favorites[2])

            favorites_list.append(Favorite(favorites[0], product, substitute))

        return favorites_list



    def display_favorites(favorites_list):
        main_product_list = []

        for favorites in favorites_list:
            if favorites.main_product.name not in main_product_list:
                main_product_list.append(favorites.main_product.name)

        for product in main_product_list:
            print(product)
            for favorites in favorites_list:
                if favorites.main_product.name == product:
                    print("    -" + favorites.substitute.name)
            print("\n\n")

        input("\nAppuyez sur entrer pour continuer\n")
