import database_function

class Store:
    """class designed store by:
        -his localisation
        -his name"""

    def __init__(self,localisation, name, identifiant = 0):
        """constructor of the classe store"""
        self.id_number = identifiant
        self.localisation = localisation
        self.name = name


    def save_data(self, cursor, connection):
        """méthode for save data in database"""

        #check if the localisation is already in database
        response = database_function.check_existence_in_database(cursor,
                "Store",
                "localisation",
                self.localisation)

        #check if name of store is already in database
        response2 = database_function.check_existence_in_database(cursor,
                "Store",
                "name",
                self.name)


        #if at least one response is false
        if response == False or response2 == False:
            store = (self.name, self.localisation)

            #insertion request
            cursor.execute("INSERT INTO Store (name, localisation)\
                    VALUES (%s, %s)", store)

            #apply change
            connection.commit()

            #filling id
            self.id_number = cursor.lastrowid

        else:
            return False

    
    def display(self):
        #method for display informations of store

        print("    name: " + self.name)
        print("    localisation: " + self.localisation)


