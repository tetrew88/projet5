import function

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


    def select_a_category(cursor):
        """méthode used by user for select a category"""

        user_choice = 0
        list_of_id= []

        cmd_sql = "SELECT * FROM Categories"
        cursor.execute(cmd_sql)

        database = cursor.fetchall()


        for data in database:
            list_of_id.append(data[0])


        while user_choice not in list_of_id:
            print("Choix de la catégorie\n\n")
            
            for data in database:
                print("{}: {}".format(data[0], data[1]))

            user_choice = input("\nEntrer votre choix: ")
            function.clean_screen()

            try:
                user_choice = int(user_choice)
            except:
                user_choice = 0


        return user_choice
