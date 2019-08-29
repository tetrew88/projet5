import platform
import os
 
def clean_screen():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")



def collecte_data_in_json_dictionnary(dictionnary, key):

    try:
        result = dictionnary[key]
    except KeyError:
        return False

    if result == "":
        result = "NULL"

    return result
        
