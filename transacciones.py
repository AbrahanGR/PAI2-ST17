import hashlib

def crea_transaccion():
    emisor = input("Usuario del emisor: ")
    receptor = input("Usuario al que le quieres hacer la transaccion: ")
    cantidad = input("Cantidad que quieres transferir: ")

    return [emisor, receptor, cantidad]