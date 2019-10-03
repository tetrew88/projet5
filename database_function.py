#!/usr/bin/python3

def check_existence_in_database(cursor, table, column, element_to_check):
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
