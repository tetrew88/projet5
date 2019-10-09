import platform
import os
 
def clean_screen():
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")



def collect_data_in_json_dictionnary(dictionnary, key, key2 = "NULL"):

    try:
        if key2 == "NULL":
            result = dictionnary[key]
        else:
            result = dictionnary[key][key2]


        if result == "":
            result = "NULL"


    except KeyError:
        result = "NULL"

    return result
        
