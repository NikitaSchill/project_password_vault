import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

# Function to generate and return a Fernet key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt the entry
def encrypt_entry(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Function to decrypt the entry
def decrypt_entry(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Function to add a new entry
def create_entry(connection, name, username, password, key, user_id):
    encrypted_password = encrypt_entry(password, key)
    insert_query = "INSERT INTO entries (name, user, pass, user_id) VALUES (%s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query, (name, username, encrypted_password, user_id))
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False

# Function to read all entries for a user
def read_entries(connection, user_id, key):
    select_query = "SELECT name, pass, user_id, user FROM entries WHERE user_id = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(select_query, (user_id,))
        entries = cursor.fetchall()
        decrypted_entries = [{ "name": entry[0], "password": decrypt_entry(entry[1], key), "user": entry[3] } for entry in entries]
        return decrypted_entries
    except Error as e:
        print(f"Error: {e}")
        return None

def find_entry_by_name(connection, name, key):
    select_query = "SELECT name, pass, user_id, user, id FROM entries WHERE name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(select_query, (name,))
        entries = cursor.fetchall()
        decrypted_entries = [{ "name": entry[0], "password": decrypt_entry(entry[1], key), "user": entry[3], "id": entry[4] } for entry in entries]
        return decrypted_entries[0]
    except Error as e:
        print(f"Error: {e}")
        return None
    
def update_entry(connection, id, col, val, key):
    if col == "pass":
        val = encrypt_entry(col, key)
    update_query = "UPDATE entries SET " + col + "='" + val + "' WHERE id = " + str(id)
    print(update_query)
    cursor = connection.cursor()
    try:
        cursor.execute(update_query)
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
