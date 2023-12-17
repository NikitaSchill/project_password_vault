from mysql.connector import Error
import hashlib
from symmetric import generate_key

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_key(key):
    return hashlib.sha256(key).hexdigest()

def register_user(connection, username, password):
    hashed_password = hash_password(password)
    insert_query = "INSERT INTO users (username, password, akey) VALUES (%s, %s, %s)"
    cursor = connection.cursor()
    try:
        key = generate_key()
        print("Encryption/Decryption key: ", key)
        hashed_key = hash_key(key)
        cursor.execute(insert_query, (username, hashed_password, hashed_key))
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False

# task 7 login

def login_user(connection, username, password):
    hashed_password = hash_password(password)
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (username, hashed_password))
    user_record = cursor.fetchone()
    return user_record

def check_akey(connection, user_id, key):
    hashed_key = hash_key(key)
    query = "SELECT * FROM users WHERE id = %s AND akey = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (user_id, hashed_key))
    user_record = cursor.fetchone()
    return user_record is not None
