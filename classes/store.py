import database_function

class Store:
    """class designed store by:
        -his city
        -his state
        -his name"""

    def __init__(self,localisation, name, identifiant = 0):
        """constructor of the classe store"""
        self.id_number = identifiant
        self.localisation = localisation
        self.name = name


    def save_data(self, cursor, connection):
        """méthode for save data in database"""

        response = database_function.check_existence_in_database(cursor,
                "Store",
                "localisation",
                self.localisation)

        response2 = database_function.check_existence_in_database(cursor,
                "Store",
                "name",
                self.name)


        if response == False or response2 == False:
            store = (self.localisation, self.name)

            cursor.execute("INSERT INTO Store (name, localisation)\
                    VALUES (%s, %s)", store)

            connection.commit()

            self.id_number = cursor.lastrowid

        else:
            return False


