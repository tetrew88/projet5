from classes.store import *

class Favorite:
    """class designed a favorite by:
        -the main product
        -list of substitute of main product"""

    def __init__(self, main_product, substitute_list):
        self.main_product = main_product
        self.substitute_list = substitute_list

    def collecte_favorites_from_database(cursor):
        favorites_list = []

        cursor.execute('SELECT * FROM Favorites')
        favorites_list = cursor.fetchall()
        
        for favorites in favorites_list:
            favorites = Store(favorites[0], favorites[1], favorites[2])

        return favorites_list
