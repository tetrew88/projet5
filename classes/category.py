class Category:
    """class designed a category by:
        -her name
        -her url"""

    def __init__(self, name):
        """constructor of the class category"""
        self.name = name
        self.url = 'https://fr.openfoodfacts.org/categorie/' + self.name


    def save_data(self, cursor):
        """méthode for save data in database"""

        cmd_sql = "SELECT * FROM Categories WHERE name = '{}'".format(self.name)

        cursor.execute(cmd_sql)

        reponse = cursor.fetchall()

        if len(reponse) == 0:
            category = (self.name, self.url)

            cursor.execute("INSERT INTO Categories (name, url)\
                    VALUES (%s, %s)", category)
            
            return True

        else:
            return False

