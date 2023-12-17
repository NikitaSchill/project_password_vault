import mysql.connector
from mysql.connector import Error
import argparse

def create_server_connection(host_name, user_name, user_password, port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=port
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def create_database(connection, db_name):
    create_db_query = f"CREATE DATABASE {db_name}"
    cursor = connection.cursor()
    try:
        cursor.execute(create_db_query)
        print(f"Database {db_name} created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_table(connection, db_name, table_sql):
    connection.database = db_name
    cursor = connection.cursor()
    try:
        cursor.execute(table_sql)
        print("Table created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_pwdst_db(host, user, password, db_name, port, table_sql):
    connection = create_server_connection(host, user, password, port)
    create_database(connection, db_name)
    create_table(connection, db_name, table_sql)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MySQL database and table creation script.")
    parser.add_argument("--host", required=True, help="Host of the MySQL server")
    parser.add_argument("--user", required=True, help="Username for the MySQL server")
    parser.add_argument("--password", required=True, help="Password for the MySQL server")
    parser.add_argument("--port", type=int, default=3306, help="TCP port for the MySQL server")
    parser.add_argument("--db_name", required=True, help="Name of the database to create")
    parser.add_argument("--table_sql", required=True, help="SQL for creating the table")

    args = parser.parse_args()

    create_pwdst_db(args.host, args.user, args.password, args.db_name, args.port, args.table_sql)
