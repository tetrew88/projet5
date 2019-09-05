def check_existence_in_database(cursor, table, column, element_to_check):
    cmd_sql = ("SELECT * FROM {} WHERE {} = '{}'".format(table, column, 
            element_to_check))

    cursor.execute(cmd_sql)
    response = cursor.fetchall()

    if len(response) == 0:
        return False
    elif len(response) > 0:
        return response
    else:
        return False

