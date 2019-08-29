from database_function import *

class Store:
    """class designed store by:
        -his city
        -his state
        -his name"""

    def __init__(self, localisation, name):
        """constructor of the classe store"""

        self.localisation = localisation
        self.name = name


    def save_data(self, cursor):
        """méthode for save data in database"""

        response = database_function.check_existence_in_database(cursor,
                "Product",
                "name",
                self.name)

        if response == False:
            store = (self.name, self.localisation)

            cursor.execute("INSERT INTO Store (name, localisation)\
                    VALUES (%s, %s)", store)

            return True

        else:
            return False


