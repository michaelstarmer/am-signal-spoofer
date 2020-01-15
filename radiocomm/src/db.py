import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='facki', password='pass', database='facki')
cursor = mariadb_connection.cursor()

def query(query):
    try:
        cursor.execute(query)
        
        return cursor
    except mariadb.Error as e:
        print("Error: {}".format(error))

    