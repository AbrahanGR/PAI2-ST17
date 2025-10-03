import hashing
from hashing import contraseña

def credentials():
    usuario = input("Introduzca su usuario: ")
    contraseña = input("Introduzcas su contraseña: ")
    return usuario + "," + contraseña