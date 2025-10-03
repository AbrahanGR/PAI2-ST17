import psycopg2

import hashing

def store_new_user(usuario, contraseña, connection):
    contraseña_hash_salt = hashing.hash_password(contraseña)
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (usuario, contraseña_hash_salt))
    except psycopg2.errors.UniqueViolation:
        print("El usuario ya existe")
        return False
    cursor.close()
    return True

def login_user(usuario_check, contraseña_check, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (usuario_check,))
    contraseña_salt = cursor.fetchone()
    if contraseña_salt is None:
        print ("No se ha encontrado usuario")
        return False
    contraseña_salt = contraseña_salt[0]
    cursor.close()
    return hashing.verify_password(contraseña_check, contraseña_salt)