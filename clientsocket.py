import socket
import hmac
import hashlib
import transacciones
from turtledemo.paint import switchupdown

import client_login

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    '''
    s.sendall(b"Hello, world")
    clave = b"clave secreta secretisima"
    mensaje = b"comprar pan"
    cifrado = hmac.new(clave, mensaje, hashlib.sha256).hexdigest()+"\n"
    cifrado = cifrado.encode()
    s.sendall(cifrado)
    s.sendall(mensaje)
    '''
    while True:
        input_user = input("Elige una opción:\n 0: Salir\n 1: Iniciar sesión\n 2: Registrar nuevo usuario\n")
        if input_user == "0":
            s.send("0".encode())
            print("Hasta pronto")
            break
        credentials = client_login.credentials()
        s.send((input_user + "," + credentials).encode())
        data = s.recv(1024).decode()

        print(data)
        if data != "No se ha podido iniciar sesión":

            if input_user == "1":
                input_user = input("Bienvenido. Seleccione una acción\n 0: Cerrar sesión \n 1: Hacer una transacción\n")
                if input_user == "1":
                    "TODO: Implementar transacciones para usuarios"
                    #primero habria que iniciar sesion

                    datos_transaccion = transacciones.crea_transaccion()
                    emisor = datos_transaccion[0] + '\n'
                    receptor = datos_transaccion[1] + '\n'
                    cantidad = datos_transaccion[2] + '\n'
                    s.sendall(emisor.encode())
                    s.sendall(receptor.encode())
                    s.sendall(cantidad.encode())

                    data = s.recv(1024).decode()
                elif input_user == "0":
                    print("Cerrando sesión")
                    s.send("0".encode())
    s.close()
#TODO: Hacer ataques de Fuerza bruta, man-in-the-middle, replay