import socket
import hmac
import hashlib
import os
import mensajes

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
        elif input_user == "1" or input_user == "2":
            credentials = client_login.credentials()
            s.send((input_user + "," + credentials).encode())
            data = s.recv(1024).decode()
            #print(data)
            if "," in data:
                datos = data.split(',')
                usuario = datos[1]
                if datos[0] == "Inicio de sesión exitoso":
                    print("Bienvenido.")
                    if input_user == "1":
                        while True:
                            input_user = input("Seleccione una acción:\n 0: Cerrar sesión \n 1: Hacer una transacción\n")
                            if input_user == "1":

                                nonce = os.urandom(16).hex() #genera nonce de 128 bits (16 Bytes)


                                datos_transaccion = transacciones.crea_mensaje(usuario)
                                mensaje = (input_user + "," + datos_transaccion + "," + nonce).encode()
                                s.send(mensaje)
                                cifrado = hmac.new("c14v3_p4r4_hm4c".encode(), mensaje, hashlib.sha256).digest()
                                s.send(cifrado)
                                #emisor = datos_transaccion[0] + '\n'
                                #receptor = datos_transaccion[1] + '\n'
                                #cantidad = datos_transaccion[2] + '\n'
                                #s.sendall(emisor.encode())
                                #s.sendall(receptor.encode())
                                #s.sendall(cantidad.encode())

                                data = s.recv(1024).decode()
                                print(data)
                            elif input_user == "0":
                                print("Cerrando sesión")
                                s.send("0".encode())
                                break
                            else:
                                print("Elija una opción válida")
            elif data == "Ha agotado sus intentos":
                print("Ha agotado sus intentos. Inténtelo de nuevo más tarde.")
                break
            else:
                print("Error: " + data)
        else:
            print("Elija una opción válida")
    s.close()
#TODO: Hacer ataques de Fuerza bruta, man-in-the-middle, replay