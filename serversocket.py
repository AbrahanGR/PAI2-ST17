# serversocket.py

import socket
import hmac
import hashlib
import ssl

import secrets

import psycopg2

import server_login
import mensajes

HOST = "0.0.0.0"
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)

#Certificado y clave
certfile = 'secrets/certs/server_crt.pem'  # Ruta al archivo del certificado SSL
keyfile = 'secrets/keys/server_key.pem'    # Ruta al archivo de la clave privada

# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Escuchar una conexión

# Envolver el socket con SSL
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

CONNECTION = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI2-ST17",
    user="server",
    password="server_PAI1-ST17"
)
CONNECTION.autocommit=True
with ssl_context.wrap_socket(server_socket, server_side=True) as s:
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        intentos = 5 #Evitar Bruteforce
        while intentos!=0: #Bucle de inicio de sesión
            data = conn.recv(1024).decode()

            if data == "0":
                break
            elif "," in data:
                #print(data)
                datos = data.split(',')
                print(f"recibido: {datos[1]}")

                usuario = datos[1]
                contraseña = datos[2]
                data_server = ""
                if datos[0] == "1":
                    if server_login.login_user(usuario, contraseña, CONNECTION):
                        data_server = "Inicio de sesión exitoso"
                        conn.send((data_server + "," + usuario).encode())
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

                                    res, mensaje = mensajes.comprueba_credenciales(receptor, cantidad, CONNECTION, nonce)

                                    if res:
                                        cifrado_comprobado = hmac.new("c14v3_p4r4_hm4c".encode(), data.encode(), hashlib.sha256).digest()
                                        if hmac.compare_digest(cifrado, cifrado_comprobado):
                                            mensajes.realiza_transaccion(usuario, receptor, cantidad, CONNECTION, nonce)
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