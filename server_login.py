import hashing

def store_new_user(usuario, contraseña, connection):
    contraseña_hash_salt = hashing.hash_password(contraseña)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (usuario, contraseña_hash_salt))
    cursor.close()

def login_user(usuario_check, contraseña_check, connection):
    cursor = connection.cursor()
    contraseña_salt = cursor.execute("SELECT password FROM users WHERE username = %s", (usuario_check,))
    if contraseña_salt is None:
        print ("No se ha encontrado usuario")
        return False
    cursor.close()
    return hashing.verify_password(contraseña_check, contraseña_salt)