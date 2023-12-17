from db import connect_to_database
from registration import register_user, login_user, check_akey
import argparse
from symmetric import create_entry, read_entries, find_entry_by_name, update_entry
from create_db import create_pwdst_db
import time

def main(db_host, db_user, db_password, db_port, db_name):
    # right now our main code established connection to an existing db using a convenient function just for that purpose
    connection = None

    while connection is None:
        try:
            create_pwdst_db(db_host, db_user, db_password, db_name, db_port, "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL, password VARCHAR(255) NOT NULL, akey VARCHAR(255) NOT NULL); CREATE TABLE entries (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, user VARCHAR(255) NOT NULL, user_id INT NOT NULL, pass VARCHAR(255) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));")
            connection = connect_to_database(db_host, db_user, db_password, db_name, db_port)

            if connection is None:
                raise Exception("Failed to connect to database")

        except Exception as e:
            print(f"DB connection error: {e}, retrying in 500ms")
            time.sleep(0.5)

    # At this point, connection is established
  
    # Assuming create_pwdst_db handles its own errors and doesn't return None
    # (otherwise you'd need similar error handling here)

    user_record = None

    while True:
        
        if user_record is None:
            user_input = input("Register(1) or Login(2) (or 'quit' to exit): ")
        else:
            user_input = input("Password entries List(1), Add(2), Update(3), Search(4) (or 'quit' to exit): ")
            
        if user_input == 'quit':
            break
        
        if user_record is None:
            if user_input == "Register" or user_input == "1":
                user = input("Input user name")
                password = input("Input user pass")
                if register_user(connection, user, password):
                    print("User registered successfully")
                else:
                    print("User registration failed")
            elif user_input == "Login" or user_input == "2":
                user = input("Input user name")
                password = input("Input user pass")
                user_record = login_user(connection, user, password)
                if user_record is not None:
                    print("User login successfully")
                    print(user_record)
                else:
                    print("User login failed")
        else:
            key = input("Enter store key")
            if check_akey(connection, user_record['id'], key.encode()) is False:
                print("Invalid key")
                continue

            if user_input == "List" or user_input == "1":
                list = read_entries(connection, user_record['id'], key)
                if list is not None:
                    for entry in list:
                        name = entry["name"]
                        password = entry["password"]
                        user = entry["user"]
                        print(f"Entry: {name}, User: {user}, Password: {password}")
                else:
                    print("Error listing entries")
            elif user_input == "Add" or user_input == "2":
                name = input("Input description")
                username = input("Input user name")
                password = input("Input user pass")
                if create_entry(connection, name, username, password, key, user_record['id']):
                    print("Entry add success")
                else:
                    print("Entry add fail")
            elif user_input == "Update" or user_input == "3":
                name = input("Enter entry name to change")
                entry = find_entry_by_name(connection, name, key)
                if entry is None:
                    print("XXX2")
                    continue
                name = entry["name"]
                password = entry["password"]
                user = entry["user"]
                print(f"Entry: {name}, User: {user}, Password: {password}")
                res = input("Enter what to change: name (1), user(2), pass(3)")
                value = 0
                if res == "name" or res == "user" or res == "pass":
                    value = input("enter new value")
                else:
                    res = 0
                    print("Invalid input")

                if res == 0:
                    continue

                res = update_entry(connection, entry["id"], res, value, key)
                if res is not None:
                    print("Update success")
            elif user_input == "Search" or user_input == "4":
                name = input("Enter entry name")
                entry = find_entry_by_name(connection, name, key)
                if entry is None:
                    print("XXX2")
                    continue
                name = entry["name"]
                password = entry["password"]
                user = entry["user"]
                print(f"Entry: {name}, User: {user}, Password: {password}")
            

# why this if is here? i think it tells python to stat code from here instead of beginning of this file
if __name__ == "__main__":
    # argparse for quick argument parsing and help generation
    parser = argparse.ArgumentParser(description="MySQL database and table creation script.")
    parser.add_argument("--db_host", default="localhost", help="Host of the MySQL server")
    parser.add_argument("--db_user", default="root", help="Username for the MySQL server")
    parser.add_argument("--db_password", default="Xpconfig37", help="Password for the MySQL server")
    parser.add_argument("--db_port", type=int, default=3307, help="TCP port for the MySQL server")
    parser.add_argument("--db_name", default="passwdst", help="Name of the database to use")

    args = parser.parse_args()

    # a separate function to start work after entrypoint and argument parsing is common
    # it just happens to be called main. can be renamed
    main(args.db_host, args.db_user, args.db_password, args.db_port, args.db_name)