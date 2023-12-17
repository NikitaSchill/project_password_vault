import mysql.connector
from mysql.connector import Error

def connect_to_database(host, user, password, database, port):
    try:
        connection = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password, 
            database=database, 
            port=port
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None