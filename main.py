from db import connect_to_database
from registration import register_user, login_user
import argparse
from symmetric import create_entry


def main(db_host, db_user, db_password, db_port, db_name, user, password, action, encrypt_key):
    # right now our main code established connection to an existing db using a convenient function just for that purpose
    connection = connect_to_database(db_host, db_user, db_password, db_name, db_port)
    
    if connection:
        if action == "register":
            if register_user(connection, user, password):
                print("User registered successfully")
            else:
                print("User registration failed")
        elif action == "login":
            if login_user(connection, user, password):
                print("User login success")
            else:
                print("Error on login")
        elif action == "adde":
            if create_entry(connection, "name", "user", "passwd", encrypt_key, 1):
                print("Entry added")
            else:
                print("Wrong key")
            

# why this if is here? i think it tells python to stat code from here instead of beginning of this file
if __name__ == "__main__":
    # argparse for quick argument parsing and help generation
    parser = argparse.ArgumentParser(description="MySQL database and table creation script.")
    parser.add_argument("--db_host", default="localhost", help="Host of the MySQL server")
    parser.add_argument("--db_user", default="root", help="Username for the MySQL server")
    parser.add_argument("--db_password", required=True, help="Password for the MySQL server")
    parser.add_argument("--db_port", type=int, default=3306, help="TCP port for the MySQL server")
    parser.add_argument("--db_name", default="passwdst", help="Name of the database to use")

    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)

    parser.add_argument("--action", default="login", help="Action to call")

    # parser.add_argument("--entry-name", default="myinfo")
    # parser.add_argument("--entry-user", default="user1")
    # parser.add_argument("--entry-pass", default="qwerty1Q")
    parser.add_argument("--entry_key", default=None)

    args = parser.parse_args()

    # a separate function to start work after entrypoint and argument parsing is common
    # it just happens to be called main. can be renamed
    main(args.db_host, args.db_user, args.db_password, args.db_port, args.db_name, args.user, args.password, args.action, args.entry_key)