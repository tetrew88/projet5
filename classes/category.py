class Category:
    """class designed a category by:
        -her name
        -her url"""

    def __init__(self, name):
        """constructor of the class category"""
        self.name = name
        self.url = 'https://fr.openfoodfacts.org/categorie/' + self.name
