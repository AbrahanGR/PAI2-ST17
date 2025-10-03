import hashing
from hashing import contraseña

def credentials():
    usuario = input("Introduzca su usuario: ")
    contraseña = input("Introduzca su contraseña: ")
    return usuario + "," + contraseña