import mysql.connector as mariadb

mariadb_connection = mariadb.connect(host='db.mstarmer.no', user='facki', password='f2w4ewfw42ww', database='facki')
cursor = mariadb_connection.cursor()

def query(query):
    try:
        cursor.execute(query)
        
        return cursor
    except mariadb.Error as e:
        print("Error: {}".format(error))