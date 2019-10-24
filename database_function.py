#!/usr/bin/python3

#function for check the existence of an element in the database
def check_existence_in_database(cursor, table, column, element_to_check):

    #request
    cmd_sql = ("SELECT * FROM {} WHERE {} = '{}'".format(table, column, 
            element_to_check))

    try:    
        cursor.execute(cmd_sql)
        response = cursor.fetchall()
        
        if len(response) < 1:
            return False
        else:
            return True

    except:
        return False
