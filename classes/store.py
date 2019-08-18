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

        cmd_sql = "SELECT * FROM Store WHERE name = '{}'".format(self.name)

        cursor.execute(cmd_sql)

        reponse = cursor.fetchall()

        if len(reponse) == 0:
            store = (self.name, self.localisation)

            cursor.execute("INSERT INTO Store (name, localisation)\
                    VALUES (%s, %s)", store)

            return True

        else:
            return False


