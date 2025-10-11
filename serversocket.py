# serversocket.py

import socket
import hmac
import hashlib
import secrets

import psycopg2

import server_login
import mensajes

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)
CONNECTION = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI1-ST17",
    user="server",
    password="server_PAI1-ST17"
)
CONNECTION.autocommit=True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        intentos = 5 #Evitar Bruteforce
        while intentos!=0: #Bucle de inicio de sesión
            data = conn.recv(1024).decode()
            '''
            if "," in data:
                datos = data.split(',')
                print(f"recibido: {datos[0]}")
                print(f"recibido: {datos[1]}")

                cifrado = datos[0]
                mensaje = datos[1].encode()
                comprobante = hmac.new(b"clave secreta secretisima", mensaje, hashlib.sha256).hexdigest()

                if hmac.compare_digest(cifrado, comprobante):
                    print("El mensaje es AUTENTICO")
                else:
                    print("El mensaje es FALSO")

            '''
            if data == "0":
                break
            elif "," in data:
                #print(data)
                datos = data.split(',')
                print(f"recibido: {datos[1]}")
                #print(f"recibido: {datos[2]}")

                usuario = datos[1]
                contraseña = datos[2]
                data_server = ""
                if datos[0] == "1":
                    if server_login.login_user(usuario, contraseña, CONNECTION):
                        data_server = "Inicio de sesión exitoso"
                        conn.send((data_server + "," + usuario).encode()) #MODIFICADO
                        print(data_server)
                        data_server = ""
                        while True: #Bucle de transacciones
                            data = conn.recv(1024).decode()
                            cifrado = conn.recv(1024)
                            print(data)
                            print(cifrado)
                            if data == "0":
                                print("Sesión cerrada")
                                break
                            elif "," in data:
                                datos = data.split(',')
                                try:
                                    emisor = datos[1]
                                    receptor = datos[2]
                                    cantidad = float(datos[3])
                                    nonce = datos[4]

                                    res, mensaje = transacciones.comprueba_credenciales(receptor, cantidad, CONNECTION, nonce)

                                    if res:
                                        cifrado_comprobado = hmac.new("c14v3_p4r4_hm4c".encode(), data.encode(), hashlib.sha256).digest()
                                        if hmac.compare_digest(cifrado, cifrado_comprobado):
                                            transacciones.realiza_transaccion(usuario, receptor, cantidad, CONNECTION, nonce)
                                            data_server = "Transaccion realizada correctamente: " + emisor + " -> " + str(cantidad) + " -> " + receptor

                                        else:
                                            data_server = "El mensaje es FALSO"
                                    else:
                                        data_server = mensaje
                                except ValueError:
                                    data_server = "El valor introducido no es un número"
                            print(data_server)
                            conn.send(data_server.encode())
                    else:
                        intentos -= 1
                        if intentos != 0:
                            if intentos == 1:
                                data_server = "Usuario o contraseña incorrecta incorrectos. Le quedan " + str(intentos) + " intento."
                            else:
                                data_server = "Usuario o contraseña incorrecta incorrectos. Le quedan " + str(intentos) + " intentos."
                        else:
                            print("El usuario ha sobrepasado los intentos")
                            data_server = "Ha agotado sus intentos"
                elif datos[0] == "2":
                    if server_login.store_new_user(usuario, contraseña, CONNECTION):
                        print("Usuario Registrado")
                        data_server = "Usuario registrado correctamente"
                    else:
                        data_server = "El usuario ya existe"
            if not data:
                break
            conn.sendall(data_server.encode())
    CONNECTION.close()
    s.close()