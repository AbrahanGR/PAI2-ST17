import hashlib
import os


def hash_password(contraseña):
    salt = os.urandom(24)
    contraseña_salt = salt + contraseña.encode("utf-8")
    return hashlib.sha256(contraseña_salt).hexdigest() + ":" + salt.hex()

def verify_password(contraseña_check, contraseña_salt):
    contraseña_hex, salt_hex = contraseña_salt.split(":") #Sacar hash y salt
    salt = bytes.fromhex(salt_hex)
    hash_check = hashlib.sha256(salt + contraseña_check.encode("utf-8")).hexdigest() #Hashear la contraseña introducida con el salt
    return hash_check == contraseña_hex #Comprobar si ambas contraseñas hasheadas con el mismo salt dan lo mismo

contraseña = "prueba"
contraseña_hash_salt = hash_password(contraseña)
print(verify_password(contraseña, contraseña_hash_salt))