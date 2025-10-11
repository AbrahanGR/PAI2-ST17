import socket
import hmac
import hashlib
import os
import ssl

import mensajes

import client_login

HOST = "localhost"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

#Crear el socket primero para luego "envolverlo" con SSL
#TODO: ChipherSuite de TLSv1.3 o nuestra propia ChiperSuite
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

#TODO: quitar estas líneas, añadiendo que confie en nuestros certificados
ssl_context.check_hostname = False  # No verifica el nombre del host
ssl_context.verify_mode = ssl.CERT_NONE  # No verifica el certificado del servidor (solo para pruebas)

with ssl_context.wrap_socket(client_socket, server_hostname=HOST) as s:
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
                            input_user = input("Seleccione una acción:\n 0: Cerrar sesión \n 1: Enviar un mensaje al servidor\n")
                            if input_user == "1":


                                contenido_mensaje = mensajes.crea_mensaje(usuario)
                                mensaje = (input_user + "," + contenido_mensaje).encode()
                                s.send(mensaje)
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