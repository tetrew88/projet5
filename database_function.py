def check_existence_in_database(cursor, table, column, element_to_check):
    cmd_sql = "SELECT * FROM {} WHERE {} = {}".format(table, column, 
            element_to_check)

    cursor.execute(cmd_sql)
    reponse = cursor.fetchall()

    if len(reponse) == 0:
        return False
    elif len(reponse) > 1:
        return True
    else:
        return False

