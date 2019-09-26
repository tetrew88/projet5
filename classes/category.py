import database_function
import function

class Category:
    """class designed a category by:
        -her name
        -her url"""

    def __init__(self, name, identifiant = 0):
        """constructor of the class category"""
        self.id_number = identifiant
        self.name = name
        self.url = 'https://fr.openfoodfacts.org/categorie/' + self.name


    def save_data(self, cursor, connection):
        """méthode for save data in database"""
        
        response = database_function.check_existence_in_database(cursor,
                "Categories",
                "name",
                self.name)


        if response == False:
            category = (self.name, self.url)

            cursor.execute("INSERT INTO Categories (name, url)\
                    VALUES (%s, %s)", category)

            connection.commit() 
            self.id_number = cursor.lastrowid


        else:
            cursor.execute("SELECT id FROM Categories\
                    WHERE name = '{}'".format(self.name))

            self.id_number = cursor.fetchall()[0][0]


    def select_a_category(cursor):
        """méthode used by user for select a category"""

        user_choice = 0
        list_of_id= []

        cmd_sql = "SELECT * FROM Categories"
        cursor.execute(cmd_sql)

        database = cursor.fetchall()

        if len(database) > 0:
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

        else:
            return False

        cursor.execute("SELECT * FROM Categories WHERE id = {}".format(
            user_choice))

        data = cursor.fetchall()[0]
        print(data)

        return Category(data[1], data[0])


    def display(self):
        print("    nom: " + self.name)
        print("    url: " + self.url)
